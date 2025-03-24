# This file tests the functionality of embedding creation using FAISS.
# It verifies that the save_to_faiss_store function correctly processes document chunks and creates a valid FAISS database.

from app.core.embedding import save_to_faiss_store
from langchain_core.documents import Document

def test_faiss_embedding_creation():
    chunks = [Document(page_content="Test embedding")]
    db = save_to_faiss_store(chunks)
    assert db is not None
