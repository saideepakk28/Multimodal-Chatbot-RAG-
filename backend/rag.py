import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Initialize Embeddings
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize Vector Store
if os.environ.get("VERCEL"):
    PERSIST_DIRECTORY = "/tmp/chroma_db"
else:
    PERSIST_DIRECTORY = "./data/chroma_db"
vectorstore = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=embedding_function
)

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
