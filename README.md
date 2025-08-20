# RAG Document Retrieval System

## Overview
This project implements a document retrieval system using Retrieval-Augmented Generation (RAG) and the LangChain framework. The system allows users to ingest documents and query them efficiently through a FastAPI application.

## Project Structure
```
rag_app

├── app
│   ├── api.py          # FastAPI application with endpoints for ingestion and querying
│   ├── engine.py       # Core logic for document ingestion and retrieval
├── main.py             # Entry point for the application         # Configuration settings for the application
│   ├── schemas.py      # Data models for request and response validation
├── requirements.txt         # Project dependencies
```

## Installation
To set up the project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/shubhamRaut-41/rag_test.git
cd rag_test
python 3.10
pip install -r requirements.txt
```
## create .env file also for the values
    HF_TOKEN = ""
    PERSIST_DIRECTORY = "chroma_db"
    CHROMA_HOST = "localhost"
    CHROMA_PORT = 8080  
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL = "google/flan-t5-base"

## Usage
To run the FastAPI application, execute the following command:

```bash
uvicorn app.api:app --reload
```

You can access the API documentation at `http://localhost:8000/api/docs`.

## API Endpoints
- **POST /ingest**: Ingest PDF files into the vector store.
- **POST /query**: Query the ingested documents based on a question.
- **POST /reset**: Reset the document store.


## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.
