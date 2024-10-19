from fastapi import FastAPI, Depends, HTTPException,Request
from sqlalchemy.orm import Session
import logging
from . import models, schemas, service,articleservice
from .database import engine, Base, get_db
from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from .exceptions import ChatServiceException
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv



# Load environment variables from the .env file
load_dotenv()

# Recreate the articles table with the new structure
Base.metadata.create_all(bind=engine)

app = FastAPI()

logger = logging.getLogger(__name__)

app = FastAPI()


# Initialize OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:8000/auth',
    client_kwargs={'scope': 'openid email profile'}
)


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
    redirect_uri = 'http://127.0.0.1:8000/auth'  # The URL to redirect to after login
    return await oauth.google.authorize_redirect(request, redirect_uri)

# Google SSO Callback
@app.route('/auth')
async def auth(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)

    # Check if user exists in your database
    db_user = service.get_user_by_username(db, user_info['email'])

    if not db_user:
        # If user doesn't exist, create a new user
        db_user = service.create_user(db, schemas.UserCreate(username=user_info['email'], password="oauth2"))  # Placeholder password

    logger.info("Google SSO login successful")
    return {"message": "Login successful!", "id": db_user.id}

# API for send batch jobs
@app.get("/send_market_trends")
async def send_market_trends_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(service.send_trends_task())
    service.schedule_task()
    asyncio.get_event_loop().run_forever()
    return JSONResponse(content={"message": "Market trends are being sent to users."})

# API route for chatbot interaction
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

# Route to add a new article
@app.post("/addarticle", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    logger.debug("adding a new article to database")
    return articleservice.create_article(db=db, article=article)

# Route to get all articles
@app.get("/getarticles", response_model=list[schemas.Article])
def get_articles(db: Session = Depends(get_db)):
    try:
        logger.debug("getting all article from database")
        return articleservice.get_articles(db=db)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="unable to fetch articles trends")
# Route Api for market-trends
@app.get("/market-trends")
def get_market_trends():
    try:
        data = service.fetch_market_trends()
        return data
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Error fetching market trends")

@app.get("/getlatestarticles", response_model=list[schemas.Article])
def get_articles(db: Session = Depends(get_db)):
    try:
        logger.debug("Getting the top 10 latest articles from the database")
        articles = service.get_latest_articles(db=db)  # No limit parameter
        return articles
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Unable to fetch article trends")