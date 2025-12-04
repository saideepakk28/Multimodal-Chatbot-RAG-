import os
import sys
# Add project root to sys.path to resolve 'backend' package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import shutil
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.rag import ingest_document, rag_init_error
from backend.chat import process_chat, chat_init_error
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("frontend/index.html")

# Models
class ChatRequest(BaseModel):
    message: str
    history: List[dict] # List of {"role": "user"|"assistant", "content": "..."}
    image: Optional[str] = None # Base64 string

class ChatResponse(BaseModel):
    response: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Use /tmp on Vercel, otherwise use data/
        if os.environ.get("VERCEL"):
            upload_dir = "/tmp"
        else:
            upload_dir = "data"
            os.makedirs(upload_dir, exist_ok=True)
            
        file_location = f"{upload_dir}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        
        result = ingest_document(file_location)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Check for System Initialization Errors
    if rag_init_error:
        return {"response": f"System Error (RAG): {rag_init_error}"}
    if chat_init_error:
        return {"response": f"System Error (Chat): {chat_init_error}"}

    try:
        # Convert history to LangChain format
        lc_history = []
        for msg in request.history:
            if msg["role"] == "user":
                lc_history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_history.append(AIMessage(content=msg["content"]))
        
        response = process_chat(request.message, lc_history, request.image)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
