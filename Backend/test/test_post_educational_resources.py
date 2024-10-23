from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app


client = TestClient(app)

# educational resource  for testing
sample_resource = {
    "title": "Understanding Market Cycles",
    "content": "This guide explains the different phases of market cycles and how to invest accordingly.",
    "video_url": "https://www.youtube.com/watch?v=jgV9XtdgXeg",
    "created_at": "2024-10-23T12:30:00Z"
}

# Mock response
mock_created_resource = {
    "title": "Understanding Market Cycles",
    "content": "This guide explains the different phases of market cycles and how to invest accordingly.",
    "video_url": "https://www.youtube.com/watch?v=jgV9XtdgXeg",
    "created_at": "2024-10-23T12:30:00Z"
}

# Test case for successful creation of an educational resource
@patch("app.services.resourceservice.create_resource")
def test_create_educational_resource_success(mock_create_resource):
    mock_create_resource.return_value = mock_created_resource
    response = client.post("/educational_resources", json=sample_resource)
    assert response.status_code == 200
    print("Response JSON:", response.json())
    json_response = response.json()
    assert json_response["title"] == sample_resource["title"]
    assert json_response["content"] == sample_resource["content"]
    assert json_response["video_url"] == sample_resource["video_url"]

    if "created_at" in json_response:
        assert json_response["created_at"] == mock_created_resource["created_at"]
    print("Mock called with:", mock_create_resource.call_args)
    mock_create_resource.assert_called_once()