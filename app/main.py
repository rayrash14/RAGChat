from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router
from app.db.database import create_tables

# app/main.py
from dotenv import load_dotenv
load_dotenv()

# Create a FastAPI app instance with metadata like title, description, and version
app = FastAPI(
    title="RAGChat: Chatbot with RAG",
    description="Upload  PDFs and ask context-aware questions using Mistral LLM",
    version="1.0.0"
)

# Enable CORS(Cross-Origin Resource Sharing) for frontend usage
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin (for development, it can be restrictive for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers in the request
)

# Initialize DB tables
@app.on_event("startup")
def startup():
    create_tables()

# Include API endpoints
app.include_router(api_router)
