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

embedding_function = None
vectorstore = None
rag_init_error = None

try:
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY is missing from environment variables.")

    embedding_function = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=google_api_key
    )

    # Initialize Vector Store
    # Using InMemoryVectorStore for Vercel (ephemeral)
    vectorstore = InMemoryVectorStore(embedding_function)

except Exception as e:
    rag_init_error = f"RAG Initialization Failed: {str(e)}"
    print(rag_init_error)

def ingest_document(file_path: str) -> str:
    """Ingests a document (PDF or Text) into the vector store."""
    if rag_init_error:
        return f"System Error: {rag_init_error}"
        
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
        
        if vectorstore:
            vectorstore.add_documents(splits)
            return f"Successfully ingested {len(splits)} chunks from {os.path.basename(file_path)}."
        else:
            return "Vector Store not initialized."
    except Exception as e:
        return f"Error ingesting document: {str(e)}"

def retrieve_documents(query: str, k: int = 3) -> List[Document]:
    """Retrieves relevant documents for a given query."""
    if rag_init_error or not vectorstore:
        print(f"Warning: Retrieval skipped due to error: {rag_init_error}")
        return []
    return vectorstore.similarity_search(query, k=k)
