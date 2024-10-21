from fastapi import FastAPI, Depends, HTTPException,Request
from sqlalchemy.orm import Session
import logging
from app.config import secrets
from  app.dto import  schemas
from .services import articleservice, service
from .database import engine, Base, get_db
from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from .exceptions import ChatServiceException,BatchJobException
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler


# Load environment variables from the .env file
load_dotenv()

# Recreate the articles table with the new structure
Base.metadata.create_all(bind=engine)

app = FastAPI()

logger = logging.getLogger(__name__)


# Initialize OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    project_id='finance-41-1729262432725',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    refresh_token_url=None,
    auth_provider_x509_cert_url='https://www.googleapis.com/oauth2/v1/certs',
    jwks_uri = 'https://www.googleapis.com/oauth2/v3/certs',
    redirect_uri='http://127.0.0.1:8000/auth',
    client_kwargs={'scope': 'openid email profile'}
)
secret_key = secrets.genrate_secret_key()
app.add_middleware(SessionMiddleware, secret_key=secret_key)

class Query(BaseModel):
    message: str

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Register User
@app.post("/register", response_model=schemas.ShowUser)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info("In register function")
    db_user = service.get_user_by_username(db, user.username)
    if db_user:
        logger.warning("User already exists")
        raise HTTPException(status_code=400, detail="Username already registered")
    return service.create_user(db, user)

# Login User
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    logger.info("In login function")
    db_user = service.get_user_by_username(db, user.username)
    if not db_user:
        logger.error("Invalid credentials")
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not service.verify_password(user.password, db_user.hashed_password):
        logger.error("Invalid password")
        raise HTTPException(status_code=400, detail="Invalid password")

    logger.info("Login successful!!!")
    service.fetch_market_trends()
    return {"message": "Login successful!", "id": db_user.id}

# Google SSO Login
@app.get("/sso-login")
async def google_login(request: Request):
    redirect_uri = request.url_for("auth")
    logger.debug(f"Redirect URI: {redirect_uri}")
    return await oauth.google.authorize_redirect(request, redirect_uri)
# API for google sso-auth
@app.get("/auth")
async def auth(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        userinfo = token.get('userinfo')
        if userinfo:
            email = userinfo.get('email')
            name = userinfo.get('name')
            at_hash = userinfo.get('at_hash')
        else:
            print("Userinfo not found in token.")
            logger.info(f"Token: {token}")

        if not token:
            raise ValueError("Token not generated")

        # Check if user exists in the database
        db_user = service.get_user_by_username(db, email)
        if not db_user:
            db_user = service.create_user(db, schemas.UserCreate(username=name, email=email, password=at_hash))

        return RedirectResponse(url="http://localhost:3000/")


    except ValueError as ve:
        logger.error(f"ValueError: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Authentication failed")

# API for send batch jobs
@app.get("/send_market_trends")
async def send_market_trends_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(service.send_trends_task)  # Pass the function reference, not the call
    service.schedule_task()  # Schedule future tasks
    return JSONResponse(content={"message": "Market trends are being sent to users."})

# API for terminating batch jobs
@app.get("/stop_batch")
async def stop_batch_jobs():
    logger.debug("stop sending batch jobs")
    try:
        asyncio.get_event_loop().stop()
        scheduler = AsyncIOScheduler()
        scheduler.shutdown()
        logger.info("Batch job stoped")
        return {"message": "stopped scheduling batch jobs"}
    except Exception as BatchJobException:
        raise BatchJobException("unable to stop batch jobs")
# API for chatbot interaction
@app.post("/chat")
async def chat(query: Query):
    logger.debug("Generating response from grok API")
    try:
        response = service.generate_advice(query.message)
        logger.info("Generated response from grok API")
        return {"response": response}
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise ChatServiceException(detail="Failed to generate chat response")

# API to add a new article
@app.post("/addarticle", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    logger.debug("adding a new article to database")
    return articleservice.create_article(db=db, article=article)

# API to get all articles
@app.get("/getarticles", response_model=list[schemas.Article])
def get_articles(db: Session = Depends(get_db)):
    try:
        logger.debug("getting all article from database")
        return articleservice.get_articles(db=db)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="unable to fetch articles trends")

# Api for market-trends
@app.get("/market-trends")
async def get_market_trends():
    try:
        data = await service.fetch_market_trends()
        return data
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Error fetching market trends")

#API to get the latestArticles
@app.get("/getlatestarticles", response_model=list[schemas.Article])
def get_articles(db: Session = Depends(get_db)):
    try:
        logger.debug("Getting the top 10 latest articles from the database")
        articles = service.get_latest_articles(db=db)  # No limit parameter
        return articles
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Unable to fetch article trends")

#API to get user activity
@app.get("/user-count", response_model=schemas.UserCountResponse)
async def get_user_count(db: Session = Depends(get_db)):
    user_count = service.get_user_count_from_db(db=db)
    return {"user_count": user_count}