from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas
import logging
import  requests
import os
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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)

DATABASE = "test.db"

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # For TLS
SMTP_USER = os.environ.get("email_user")
SMTP_PASSWORD = os.environ.get("email_password")

# Load environment variables from the .env file
load_dotenv()

# Initialize the Groq client with your API key from the environment variable
client = Groq(
    api_key=os.environ.get("GROK_API_KEY"),
)


def get_password_hash(password: str):
    logger.debug("Hashing the password %s",password)
    return pwd_context.hash(password)
    logger.info("password hashed successfully")

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    logger.info("getting the user by username")
    return db.query(models.User).filter(models.User.username == username).first()

def verify_password(plain_password, hashed_password):
    logger.info("Attempting to verify password")
    return pwd_context.verify(plain_password, hashed_password)
def fetch_market_trends():
    # API URL
    url = "https://indian-stock-exchange-api2.p.rapidapi.com/trending"

    headers = {
        "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY"),
        "x-rapidapi-host": "indian-stock-exchange-api2.p.rapidapi.com"
    }

    logger.debug("getting market trends")
    # Sending GET request
    response = requests.get(url, headers=headers)

    # Checking for successful response
    if response.status_code == 200:
        data = response.json()
    logger.info("Returning Market Trends")
    return data
async def get_users():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT email FROM users") as cursor:
            logger.info("getting Emails from Database")
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

async def send_email(recipient: str, trends: List[str]):
    subject = "Latest Market Trends"
    body = "\n".join(trends)

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Upgrade to a secure connection
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, recipient, msg.as_string())

async def send_market_trends(trends: List[str]):
    users = await get_users()
    for user in users:
        await send_email(user, trends)

# Background task to run the batch job
async def send_trends_task():
    trends = await fetch_market_trends()
    logger.info("Sending Market Information to Users")
    await send_market_trends(trends)

# Task scheduler
def schedule_task():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_trends_task, 'cron', hour=11, minute=30)
    scheduler.start()
    logger.info("Scheduling the task")


def generate_advice(user_input: str) -> str:

    try:
        # Check if the user input is financial in nature
        if not is_financial_query(user_input):
            return "I'm here to help with financial questions. Please ask me about budgeting, saving, investing, retirement planning, taxes, or debt management."

        # Updated API call for chat completion
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",  # Ensure model name is correct
            messages=[
                {
                    "role": "system",  # System instructions to the assistant
                    "content": "You are a financial advisor AI. Your responses must be simple and no longer than 3 lines. Only provide advice on personal finance topics such as budgeting, saving, investing, retirement planning, taxes, and debt management. Do not answer questions that are not related to finance. Always ensure your advice is practical, easy to understand, and tailored to individual needs. Provide strategies for both short-term and long-term financial goals."
                },
                {
                    "role": "user",  # User message containing the query
                    "content": user_input,
                }
            ]
        )

        # Return the content of the first choice message
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Error details: {str(e)}")  # Log the error for debugging
        raise HTTPException(status_code=500, detail="Error fetching response from Groq API")

def is_financial_query(query: str) -> bool:
    # Simple check for financial keywords (can be improved using NLP libraries like spaCy)
    financial_keywords = [
        "budget", "saving", "investing", "retirement",
        "tax", "debt", "finance", "interest", "loan", "wealth", "credit", "savings"
    ]
    return any(keyword in query.lower() for keyword in financial_keywords)