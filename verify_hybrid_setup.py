import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

google_key = os.getenv("GOOGLE_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

print(f"Google Key present: {bool(google_key)}")
print(f"Groq Key present: {bool(groq_key)}")

if not google_key or not groq_key:
    print("ERROR: Missing one or more API keys in .env")
    sys.exit(1)

print("\n--- 1. Testing Google Embeddings (text-embedding-004) ---")
try:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=google_key
    )
    vec = embeddings.embed_query("test query")
    print(f"SUCCESS: Embeddings generated. Vector length: {len(vec)}")
except Exception as e:
    print(f"FAILURE: Embeddings failed. Error: {e}")
    sys.exit(1)

print("\n--- 2. Testing Groq LLM (llama-3.1-8b-instant) ---")
try:
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=groq_key
    )
    resp = llm.invoke([HumanMessage(content="Hello, are you working?")])
    print(f"SUCCESS: Groq responded: {resp.content}")
except Exception as e:
    print(f"FAILURE: Groq LLM failed. Error: {e}")
    sys.exit(1)

print("\n--- Hybrid Setup Verified Successfully ---")
