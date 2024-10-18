import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import main
from app.database import Base

DATABASE_URL = "sqlite:///./testing.db"

# Create a new SQLAlchemy engine for the test database
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Create a test client
client = TestClient(main.app)

@pytest.fixture(scope="function")
def db_session():
    # Create a new database session for a test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_register_new_user(db_session):
    user_data = {
        "username": "testuser",  # Corrected username
        "email": "te@example.com",
        "password": "testpassword"
    }

    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]

    # Try to register the same user again
    response = client.post("/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_login_user(db_session):
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/login", json=user_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful!"
    wrong_user_data = {
        "username": "wronguser",
        "password": "testpassword"
    }
    response = client.post("/login", json=wrong_user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid username or password"
    wrong_password_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post("/login", json=wrong_password_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid password"
