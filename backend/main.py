import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai
from supabase import create_client
from unstructured_ingest.v2.pipeline.pipeline import Pipeline
from unstructured_ingest.v2.interfaces import ProcessorConfig
from unstructured_ingest.v2.processes.connectors.local import (
    LocalIndexerConfig,
    LocalDownloaderConfig,
    LocalConnectionConfig,
    LocalUploaderConfig
)
from unstructured_ingest.v2.processes.partitioner import PartitionerConfig

# Load environment variables from .env file
load_dotenv()

# Configure directories
UPLOAD_DIRECTORY = "./uploaded_documents"
OUTPUT_DIRECTORY = "./output"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# Configure unstructured.io
UNSTRUCTUREDIO_API_KEY = os.getenv("UNSTRUCTUREDIO_API_KEY")
UNSTRUCTUREDIO_ENDPOINT = "https://api.unstructuredapp.io/general/v0/general"

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Set Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize FastAPI
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.111.128:3000"],  # Adjust to your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize document storage
documents_db = {}

class DocumentQuery(BaseModel):
    document_id: str
    query: str

def process_document_with_unstructured(file_path: str) -> str:
    """Process document using unstructured.io pipeline"""
    try:
        Pipeline.from_configs(
            context=ProcessorConfig(),
            indexer_config=LocalIndexerConfig(input_path=UPLOAD_DIRECTORY),
            downloader_config=LocalDownloaderConfig(),
            source_connection_config=LocalConnectionConfig(),
            partitioner_config=PartitionerConfig(
                partition_by_api=True,
                api_key=UNSTRUCTUREDIO_API_KEY,
                partition_endpoint=UNSTRUCTUREDIO_ENDPOINT,
                strategy="hi_res",
                additional_partition_args={
                    "split_pdf_page": True,
                    "split_pdf_allow_failed": True,
                    "split_pdf_concurrency_level": 15
                }
            ),
            uploader_config=LocalUploaderConfig(output_dir=OUTPUT_DIRECTORY)
        ).run()
        
        # Read the processed output
        output_file = os.path.join(OUTPUT_DIRECTORY, os.path.basename(file_path)) + '.json'
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    except Exception as e:
        raise Exception(f"Error processing document: {str(e)}")

def query_document_with_gemini(document_content: str, query: str) -> str:
    """Process query using Gemini model"""
    try:
        prompt = f"""
        Based on the following document content, please answer the question.
        
        Document content:
        {document_content}
        
        Question: {query}
        
        Please provide a concise and accurate answer based only on the information provided in the document.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Error processing query with Gemini: {str(e)}")

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIRECTORY, f"{file_id}_{file.filename}")
    
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        processed_content = process_document_with_unstructured(file_path)
        
        documents_db[file_id] = {
            "file_name": file.filename,
            "file_path": file_path,
            "content": processed_content,
        }
        
        return JSONResponse(content={
            "message": "Document uploaded and processed successfully",
            "document_id": file_id
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(query: DocumentQuery):
    """Ask a question about a specific document"""
    if query.document_id not in documents_db:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        document_content = documents_db[query.document_id]["content"]
        response = query_document_with_gemini(document_content, query.query)
        
        return JSONResponse(content={
            "query": query.query,
            "response": response,
            "document": documents_db[query.document_id]["file_name"]
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    return [{
        "document_id": doc_id,
        "file_name": info["file_name"]
    } for doc_id, info in documents_db.items()]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
