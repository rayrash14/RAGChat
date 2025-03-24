from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# (Use .env later, for now define DB path)
# Define the path to the SQLite database. The path can be set using an environment variable.
# If no environment variable is found, it defaults to 'app/db/metadata.db'.
DB_PATH = os.getenv("SQLITE_DB_PATH", "app/db/metadata.db")

# Create the database engine using the SQLite database path
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Function to create tables for all models in the database.
# This will use the 'Base' metadata to create tables defined by models like 'DocumentMetadata'.
def create_tables():
    from .models import DocumentMetadata
    Base.metadata.create_all(bind=engine)

# Dependency to get a session for interacting with the database
# This will yield a database session which can be used within a request to interact with the database.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
