from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

def get_embedding_model():
    """
    This function initializes and returns a pre-trained HuggingFace model for generating embeddings.
    The model 'sentence-transformers/all-MiniLM-L6-v2' is used for creating sentence-level embeddings.
    """
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

def save_to_faiss_store(chunks, db_path="app/vectorstore/db_faiss"):
    """
    This function saves document chunks into a FAISS vector store.
    
    Args:
        chunks (list): List of document chunks to be embedded and saved.
        db_path (str): Path where the FAISS database will be stored (default is 'app/vectorstore/db_faiss').
        
    Returns:
        FAISS: The FAISS database object.
    """
    embedding_model = get_embedding_model()
    db = FAISS.from_documents(chunks, embedding_model)  # Convert document chunks into vectors and store them in FAISS
    db.save_local(db_path)
    return db

def load_faiss_store(db_path="app/vectorstore/db_faiss"):
    """
    This function loads the FAISS vector store from a given path.
    
    Args:
        db_path (str): Path to the saved FAISS vector store (default is 'app/vectorstore/db_faiss').
        
    Returns:
        FAISS: The loaded FAISS database object.
    """
    embedding_model = get_embedding_model()
    return FAISS.load_local(db_path, embedding_model, allow_dangerous_deserialization=True)
