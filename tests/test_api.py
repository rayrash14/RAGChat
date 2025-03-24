# This file contains tests for the FastAPI application endpoints.
# It tests the functionality of the /upload endpoint to ensure it accepts PDF files correctly,
# and the /query endpoint to check if a valid question returns a proper response from the system.

from dotenv import load_dotenv
load_dotenv()

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_and_query():
    # Upload
    with open("tests/sample.pdf", "rb") as f:
        response = client.post("/upload", files={"files": ("sample.pdf", f, "application/pdf")})
        assert response.status_code == 200

    # Query (fix here)
    response = client.post("/query", json={"question": "What is health?"})
    print("Query Response:", response.json())
    assert response.status_code == 200

