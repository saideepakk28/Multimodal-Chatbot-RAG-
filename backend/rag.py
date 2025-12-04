import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document

# Initialize Embeddings
# Using Google Gemini Embeddings for lightweight deployment
# Switched to text-embedding-004 as embedding-001 is hitting quota/deprecation limits
# Explicitly passing API key to avoid DefaultCredentialsError on Vercel
from dotenv import load_dotenv
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    # This print will show up in Vercel logs
    print("CRITICAL ERROR: GOOGLE_API_KEY is missing from environment variables!")
    # We can try to proceed (it will fail) or raise a custom error
    raise ValueError("GOOGLE_API_KEY not found. Please add it to Vercel Environment Variables.")

embedding_function = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=google_api_key
)

# Initialize Vector Store
# Using InMemoryVectorStore for Vercel (ephemeral)
vectorstore = InMemoryVectorStore(embedding_function)

def ingest_document(file_path: str) -> str:
    """Ingests a document (PDF or Text) into the vector store."""
    try:
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
        else:
            return "Unsupported file format. Please upload .pdf or .txt files."

        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(documents)
        
        vectorstore.add_documents(splits)
        return f"Successfully ingested {len(splits)} chunks from {os.path.basename(file_path)}."
    except Exception as e:
        return f"Error ingesting document: {str(e)}"

def retrieve_documents(query: str, k: int = 3) -> List[Document]:
    """Retrieves relevant documents for a given query."""
    return vectorstore.similarity_search(query, k=k)
