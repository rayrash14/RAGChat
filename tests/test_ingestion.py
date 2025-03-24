# This file tests the ingestion process of PDF documents.
# It ensures that the load_pdf_and_split_chunks function correctly loads a PDF, splits it into chunks, 
# and processes the documents as expected by verifying the number of documents and chunks.

from app.core.ingestion import load_pdf_and_split_chunks
import os

def test_load_pdf_and_split_chunks():
    file_path = "tests/sample.pdf"
    documents, chunks = load_pdf_and_split_chunks(file_path)
    assert len(documents) > 0
    assert len(chunks) > 0
