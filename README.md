# RAG Chatbot: A Retrieval-Augmented Generation (RAG) Pipeline

This project implements a **Retrieval-Augmented Generation (RAG) pipeline** that allows users to upload documents and ask context-aware questions based on their content. The system uses a vector database for efficient document retrieval and an LLM (Large Language Model) API for generating relevant answers.

---

## Features

- **Document Upload**: Users can upload documents (PDF format) to be processed by the system.
- **Text Chunking**: Documents are chunked into smaller pieces for efficient retrieval.
- **Query Handling**: Users can ask context-aware questions based on the uploaded documents.
- **Metadata Retrieval**: Retrieve metadata like file name, number of pages, and chunks for each uploaded document.
- **Dockerized Application**: The application is containerized using Docker for easy deployment on both local and cloud environments.
- **Testing**: Comprehensive unit and integration tests for document retrieval and query handling.

---

## Table of Contents

1. [Setup and Installation Instructions](#setup-and-installation-instructions)
2. [API Endpoints](#api-endpoints)
3. [Docker Setup and Usage](#docker-setup-and-usage)
4. [Testing](#testing)
5. [Postman Collection](#postman-collection)
6. [License](#license)

---

## Setup and Installation Instructions

### Prerequisites

- Python 3.8+
- Docker
- Git
- Hugging Face Token (`HF_TOKEN`)
- SQLite or similar database for metadata storage

### Steps to Run the Application Locally

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/chatbot-rag.git
    cd chatbot-rag
    ```

2. **Create a virtual environment (Optional)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory with the following content:
    ```env
    HF_TOKEN=your_hugging_face_token
    HUGGING_FACE_REPO_ID=mistralai/Mistral-7B-Instruct-v0.3
    SQLITE_DB_PATH=path_to_your_db
    ```

  - ***SQLITE_DB_PATH:*** The path to the SQLite database file.

    - By default, this is set to `app/db/metadata.db`, meaning the database will be stored inside the `app/db/` directory in the project.
  
    - If you'd like to store the database in a different location, update this path to reflect your desired directory (e.g., `/path/to/database/metadata.db`).

5. **Run the FastAPI application locally**:
    ```bash
    uvicorn app.main:app --reload
    ```

    The application will be available at `http://127.0.0.1:8000`.

---

## API Endpoints

1. **POST /upload**:
    - **Purpose**: Upload PDF documents.
    - **Parameters**: Accepts a list of PDF files (maximum 20 files).
    - **Validations**:
        - Only PDF files are allowed.
        - Maximum of 1000 pages per file.
    - **Example Request**: 
        - Upload PDF file via Postman or cURL.

2. **POST /query**:
    - **Purpose**: Submit a question in JSON format.
    - **Example Request Body**:
    ```json
    {
        "question": "What is the purpose of RAG in NLP?"
    }
    ```
    - **Response**:
        - Returns a context-aware answer based on the uploaded documents.

3. **GET /metadata**:
    - **Purpose**: Retrieve metadata for uploaded documents.
    - **Response**: Returns metadata like filename, number of pages, and number of chunks for each document.

---

## Docker Setup and Usage

1. **Build the Docker images**:
    ```bash
    docker-compose build
    ```

2. **Run the Docker containers**:
    ```bash
    docker-compose up
    ```

    The FastAPI application will be accessible via Swagger UI at Swagger UI: http://localhost:8000/docs

---

## Testing

The project includes unit and integration tests for document upload, query handling, and metadata retrieval. To run the tests:

1. **Install testing dependencies**:
    ```bash
    pip install pytest
    ```

2. **Run the tests**:
    ```bash
    pytest tests/
    ```

### Tests Included:

1. **Document Upload**:
    - Accepts PDF files only.
    - Rejects more than 20 files.
    - Rejects PDFs with more than 1000 pages.

2. **Query Handling**:
    - Accepts valid JSON body and returns relevant answers.

3. **Metadata Retrieval**:
    - Returns a list of uploaded document metadata.



---

## Postman Collection

- The project includes a Postman collection to test the API endpoints.
- You can import the provided `.json` file into Postman and test the endpoints directly.

### Steps to Use Postman:
1. Download the Postman collection `.json` file.
2. Open Postman and import the collection.
3. Test the **/upload**, **/query**, and **/metadata** endpoints by uploading PDF files, submitting queries, and retrieving metadata.

---

## License

This project is licensed under the MIT License.

---

This version of the `README.md` provides a detailed overview of the project, including setup instructions, API usage, testing, and Postman collection information. It's designed for easy use and clarity for anyone who would like to set up, run, and test the application.
