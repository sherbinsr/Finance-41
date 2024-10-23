from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base
import pytest

# Create a temporary database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./testing.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Create the database schema for testing
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the database schema after tests
    Base.metadata.drop_all(bind=engine)

# Initialize the TestClient
client = TestClient(app)

def test_create_article(setup_database):
    article_data = {
        "title": "Stock Market Crash 2024",
        "content": "The global stock markets have taken a nosedive due to unprecedented inflation...",
    }
    response = client.post("/addarticle", json=article_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == article_data["title"]
    assert data["content"] == article_data["content"]
    assert "created_at" in data

def test_get_articles(setup_database):
    # Send a GET request to retrieve all articles
    response = client.get("/getarticles")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
