from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Body

from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from app.db.database import get_db
from app.db.models import DocumentMetadata
from app.core.ingestion import load_pdf_and_split_chunks
from app.core.embedding import save_to_faiss_store
from app.core.rag_chain import get_qa_chain

from pydantic import BaseModel, Field

# Initialize APIRouter for creating API endpoints
router = APIRouter()

# Define upload directory and create it if not exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Endpoint to upload documents (POST /upload)
@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    # Check if the number of files uploaded is more than 20
    if len(files) > 20:
        raise HTTPException(status_code=400, detail="You can upload up to 20 files only.")

    all_chunks = []  # List to store the document chunks
    uploaded_info = []  # List to store uploaded document information

    # Process each uploaded file
    for file in files:
        # Restrict upload to PDF files
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"Only PDF files are allowed. '{file.filename}' is not a PDF.")

        # Save the file to the uploads directory
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        # Split the PDF file into documents and text chunks
        documents, text_chunks = load_pdf_and_split_chunks(file_path)


        # Enforce max 1000 pages per file
        if len(documents) > 1000:
            raise HTTPException(
                status_code=400,
                detail=f"'{file.filename}' has {len(documents)} pages. Maximum allowed is 1000."
            )

        save_to_faiss_store(text_chunks)  # Save or append to FAISS

        #  Delete existing metadata entry with same filename (to avoid UNIQUE constraint error)
        existing_doc = db.query(DocumentMetadata).filter_by(filename=file.filename).first()
        if existing_doc:
            db.delete(existing_doc)
            db.commit()
        # Add fresh metadata entry
        metadata = DocumentMetadata(
            filename=file.filename,
            num_pages=len(documents),
            num_chunks=len(text_chunks)
        )
        db.add(metadata)
        db.commit()
        # Add the document details to the uploaded_info list
        uploaded_info.append({"filename": file.filename, "pages": len(documents), "chunks": len(text_chunks)})

    return {"status": "success", "uploaded": uploaded_info}

# Endpoint to query the system (POST /query)
@router.post("/query")
#async def query_system(question: str):

async def query_system(payload: dict = Body(...)): 
    # Extract the question from the payload
    question = payload.get("question")  
    
    # If no question is provided, raise an HTTP exception
    if not question:  
        raise HTTPException(status_code=400, detail="Missing 'question' in request body.")  

    try:
        qa_chain = get_qa_chain()  # Call the QA chain to get a response from the documents
        response = qa_chain.invoke({"query": question})
        # Return the answer along with the source documents
        return {
            "answer": response["result"],
            "source_documents": [doc.metadata["source"] if doc.metadata else "N/A" for doc in response["source_documents"]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to get metadata of uploaded documents (GET /metadata)
@router.get("/metadata")
def get_metadata(db: Session = Depends(get_db)):
    # Fetch all document metadata from the database
    docs = db.query(DocumentMetadata).all()
    return [
        {
            "filename": d.filename,
            "uploaded_at": d.uploaded_at,
            "num_pages": d.num_pages,
            "num_chunks": d.num_chunks
        }
        for d in docs
    ]
