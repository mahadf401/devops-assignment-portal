import pytest
from app import app, submissions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        submissions.clear()
        yield client

def test_valid_submission(client):
    """Test Case 1: Complete details & valid submission URL"""
    payload = {
        "student_name": "John Doe",
        "reg_num": "FA20-BCS-001",
        "title": "DevOps Assignment 1",
        "submission_url": "https://github.com/johndoe/devops-lab"
    }
    response = client.post('/submit', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert len(submissions) == 1

def test_missing_reg_num(client):
    """Test Case 2: Missing registration number"""
    payload = {
        "student_name": "Jane Smith",
        "reg_num": "",
        "title": "DevOps Assignment 1",
        "submission_url": "https://github.com/janesmith/devops"
    }
    response = client.post('/submit', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "Missing required fields" in data["message"]
    assert len(submissions) == 0

def test_invalid_url(client):
    """Test Case 3: Invalid submission URL"""
    payload = {
        "student_name": "Alex Johnson",
        "reg_num": "FA20-BCS-002",
        "title": "DevOps Assignment 1",
        "submission_url": "invalid-url-without-http"
    }
    response = client.post('/submit', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "error"
    assert "Invalid submission URL" in data["message"]
    assert len(submissions) == 0