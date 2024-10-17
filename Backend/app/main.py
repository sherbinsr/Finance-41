from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from . import models, schemas, service
from .database import engine, Base, get_db
from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio

Base.metadata.create_all(bind=engine)
app = FastAPI()

logger = logging.getLogger(__name__)

app = FastAPI()





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
@app.post("/register", response_model=schemas.ShowUser)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info("In register function")
    db_user = service.get_user_by_username(db, user.username)
    if db_user:
        logger.warning("User already exists")
        raise HTTPException(status_code=400, detail="Username already registered")
    return service.create_user(db, user)

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
    response =service.generate_advice(query.message)
    return {"response": response}