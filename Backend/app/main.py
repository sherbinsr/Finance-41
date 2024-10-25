from builtins import list

from fastapi import FastAPI, Depends, HTTPException,Request
from sqlalchemy.orm import Session
import logging
import  requests
from app.config import secrets
from  app.dto import  schemas
from .services import articleservice, service, resourceservice
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

app = FastAPI(title="Finance 41 API'S",
              description="The AI Powered Financial Advisor is a solution aimed at addressing the critical challenges users face with traditional financial advisory services. It aims to provide affordable, accessible, and personalized financial advice through a tailored chatbot interface. By leveraging artificial intelligence, the product will automate financial analysis",
              version="1.0.0",
              contact={
                  "name": "Sherbin S",
                  "email": "sherbinsyles31@gmail.com",
              },

              )

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
    redirect_uri='https://finance-41-1081098542602.us-central1.run.app/proxy/8000/auth',
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
        if db_user:
            # If the user exists, redirect to 404 page
            return RedirectResponse(url="https://finance-41-1081098542602.us-central1.run.app/proxy/3000/404")

        # If user doesn't exist, create a new one
        db_user = service.create_user(db, schemas.UserCreate(username=name, email=email, password=at_hash))
        return RedirectResponse(url="https://finance-41-1081098542602.us-central1.run.app/proxy/3000/")

    except ValueError as ve:
        logger.error(f"ValueError: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return RedirectResponse(url="https://finance-41-1081098542602.us-central1.run.app/proxy/3000/404")
        raise HTTPException(status_code=500, detail="Authentication failed user already exists")



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
    return articleservice.create_article(db=db,article=article)

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
        data = await service.market_details()
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

# Api to fetch Informations about particular stocks
@app.get("/stock")
def get_stock(name: str):
    try:
        stock_info = service.get_stock_info(name)
        return stock_info
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=http_err.response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

# Api to analyze portfolio
@app.post("/analyze")
def analyze_portfolio(portfolio: schemas.Portfolio):
    total_value = 0
    portfolio_data = {
        "portfolio": []
    }

    # Prepare portfolio data using the existing schema
    for item in portfolio.items:
        total_value += item.quantity * item.price
        portfolio_data["portfolio"].append({
            "symbol": item.symbol,
            "quantity": item.quantity,
            "price": item.price
        })

    # Use the GroqService to analyze portfolio risk
    try:
        risk_analysis = service.analyze_portfolio(portfolio_data)
    except Exception as e:
        return {"error": f"Error analyzing portfolio: {str(e)}"}

    analysis = {
        "total_value": total_value,
        "total_items": len(portfolio.items),
        "risk_analysis": risk_analysis
    }

    return analysis

# Endpoint to get educational resources
@app.get("/educational_resources", response_model=list[schemas.EducationalResourceResponse])
async def get_educational_resources(db: Session = Depends(get_db)):
    resources = resourceservice.get_all_resources(db=db)
    return resources

# Endpoint to create a new educational resource
@app.post("/educational_resources", response_model=schemas.EducationalResourceCreate)
async def create_educational_resource(resource: schemas.EducationalResourceCreate, db: Session = Depends(get_db)):
  logger.debug("adding new educational resource")
  return resourceservice.create_resource(db=db, resource=resource)
