import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

# Initialize Embeddings
# Using Google Gemini Embeddings for lightweight deployment
embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

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
