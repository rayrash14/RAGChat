# Import necessary modules from SQLAlchemy to define database columns and their types
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

# Define the 'DocumentMetadata' model which will be mapped to the 'document_metadata' table in the database
class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    num_pages = Column(Integer)
    num_chunks = Column(Integer)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
