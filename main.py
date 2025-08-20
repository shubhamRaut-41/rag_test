from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import app as api_app

app = FastAPI(title="RAG Document Retrieval System")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routes
app.mount("/api", api_app)

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG Document Retrieval System. Visit /api/docs for API documentation."}