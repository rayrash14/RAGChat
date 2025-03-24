from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# Function to load a PDF file and split it into text chunks
def load_pdf_and_split_chunks(file_path: str, chunk_size: int = 500, chunk_overlap: int = 50):
    """
    This function loads a PDF file, splits its content into smaller chunks, 
    and returns both the entire documents and the split text chunks.
    
    Args:
        file_path (str): The path to the PDF file to be loaded.
        chunk_size (int): The size of each text chunk (default is 500 characters).
        chunk_overlap (int): The number of characters that overlap between chunks (default is 50).
        
    Returns:
        tuple: A tuple containing:
            - documents (list): The entire content of the loaded PDF.
            - text_chunks (list): A list of text chunks generated from the document.
    """
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Initialize the text splitter with the specified chunk size and overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,  # Maximum size of each chunk
        chunk_overlap=chunk_overlap  # Number of characters to overlap between chunks
    )
    # Split the loaded documents into smaller chunks
    text_chunks = text_splitter.split_documents(documents)

    return documents, text_chunks
