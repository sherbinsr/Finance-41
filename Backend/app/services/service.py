import asyncio
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from  app.dto import  schemas
from app.entity import models
import logging
import  requests
import aiosqlite
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import List
import os
from dotenv import load_dotenv
from groq import Groq
from fastapi import HTTPException
from sqlalchemy import  func
import spacy

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Intializing Logger
logger = logging.getLogger(__name__)

DATABASE = "finance.db"

# Load environment variables from the .env file
load_dotenv()

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # For TLS
SMTP_USER = os.environ.get("EMAIL_USER")
SMTP_PASSWORD = os.environ.get("EMAIL_PASSWORD")

# Groq client with your API key from the environment variable
client = Groq(
    api_key=os.environ.get("GROK_API_KEY"),
)

# Load  NLP model
nlp = spacy.load("en_core_web_sm")

# Function to hash the password
def get_password_hash(password: str):
    logger.debug("Hashing the password %s",password)
    return pwd_context.hash(password)
    logger.info("password hashed successfully")

# Funtion creating new User
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Function get user by username
def get_user_by_username(db: Session, username: str):
    logger.info("getting the user by username")
    return db.query(models.User).filter(models.User.username == username).first()

# Function to verify password
def verify_password(plain_password, hashed_password):
    logger.info("Attempting to verify password")
    return pwd_context.verify(plain_password, hashed_password)

# Function to Market Trends
async def market_trends():
    # API URL
    url = "https://indian-stock-exchange-api2.p.rapidapi.com/trending"

    headers = {
        "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY"),
        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com"
    }

    logger.debug("getting market trends")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        top_gainers = data.get("trending_stocks", {}).get("top_gainers", [])
    logger.info("Returning Top Gainers")
    return top_gainers

# Function to get user emails
async def get_users():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT email FROM users") as cursor:
            logger.info("getting Emails from Database")
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

# Function to Send emails for batch jobs
async def send_email(recipient: str, trends: List[dict]):
    subject = "Latest Market Trends"
    # Format the Dict to a readable string
    body_lines = []
    for trend in trends:
        body_lines.append(f"Company: {trend['company_name']}, Price: {trend['price']}, Change: {trend['percent_change']}%")
    body = "\n".join(body_lines)
    logger.debug(f"Email body constructed: {body}")

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if not SMTP_USER or not SMTP_PASSWORD:
        logger.error("SMTP_USER or SMTP_PASSWORD is not set.")
        raise ValueError("SMTP credentials are missing!")

    try:
        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, recipient, msg.as_string())
        logger.info(f"Email sent to {recipient}")
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"Failed to authenticate with SMTP server: {e}")
        raise
    except Exception as BatchJobException:
        logger.error(f"Failed to send email: {BatchJobException}")
        raise  BatchJobException("unable to stop batch jobs")

# Batch Function to send batch jobs
async def send_market_trends(trends: List[dict]):
    users = await get_users()
    for user in users:
        await send_email(user, trends)

# Background task to run the batch job
async def send_trends_task():
    trends = await market_trends()
    logger.info("Sending Market Information to Users")
    await send_market_trends(trends)

# Task scheduler for batch jobs
def schedule_task():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: asyncio.create_task(send_trends_task()), 'cron', hour=11, minute=00)
    scheduler.start()
    logger.info("Scheduling the task")

# function to generate Chat
def generate_advice(user_input: str) -> str:

    try:
        # Check if the user input is financial
        if not is_financial_query(user_input):
            return "I'm here to help with financial questions. Please ask me about budgeting, saving, investing, retirement planning, taxes, or debt management."


        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial advisor AI. Your responses must be simple and no longer than 3 lines. Only provide advice on personal finance topics such as budgeting, saving, investing, retirement planning, taxes, and debt management. Do not answer questions that are not related to finance. Always ensure your advice is practical, easy to understand, and tailored to individual needs. Provide strategies for both short-term and long-term financial goals."
                },
                {
                    "role": "user",  # User message containing the query
                    "content": user_input,
                }
            ]
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Error details: {str(e)}")  # Log the error for debugging
        raise HTTPException(status_code=500, detail="Error fetching response from Groq API")

# Function to Check the does the query is related to Finance
def is_financial_query(query: str) -> bool:
    financial_keywords = [
        "budget", "saving", "investing", "retirement", "tax", "debt", "finance",
        "interest", "loan", "wealth", "credit", "savings", "mortgage", "insurance",
        "capital", "expense", "income", "liability", "asset", "equity", "bond",
        "dividend", "portfolio", "stock", "mutual fund", "ETF", "real estate",
        "cash flow", "ROI", "yield", "appreciation", "depreciation", "bankruptcy",
        "inflation", "recession", "subsidy", "forex", "derivatives", "liquidity",
        "capital gains", "annuities", "hedging", "index fund", "pension", "treasury",
        "futures", "commodities", "microfinance", "payment", "transaction",
        "currency", "financial planning", "trust fund", "brokerage", "private equity",
        "venture capital", "diversification", "risk management", "tax shelter",
        "credit score", "credit card", "debit card", "sinking fund", "escrow",
        "cash reserve", "money market", "fixed income", "variable rate",
        "payroll", "audit", "fundraising", "crowdfunding"
    ]
    doc = nlp(query.lower())
    for token in doc:
        if token.text in financial_keywords:
            return True

    return False


# Function to sort out the latest news
def get_latest_articles(db: Session):
    return db.query(models.Article).order_by(models.Article.created_at.desc()).limit(10).all()

# Function to get user active count from database
def get_user_count_from_db(db: Session):
    user_count = db.query(func.count(models.User.id)).scalar()
    return user_count

# Function to fetch Market details
async def market_details():
    # API URL
    url = "https://indian-stock-exchange-api2.p.rapidapi.com/trending"

    headers = {
        "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY"),
        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com"
    }

    logger.debug("getting market details")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
    logger.info("Returning Top Gainers")
    return data

# function to get stock information
def get_stock_info(name: str):
    url = "https://indian-stock-exchange-api2.p.rapidapi.com/stock"
    headers = {
        "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY"),
        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com"
    }

    querystring = {"name": name}
    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()
    return response.json()