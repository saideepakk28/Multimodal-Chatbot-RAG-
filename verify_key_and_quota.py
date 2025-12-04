import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print(f"Testing API Key: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    print("ERROR: GOOGLE_API_KEY not found in .env")
    sys.exit(1)

print("\n--- 1. Testing Embeddings (RAG Dependency) ---")
try:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vec = embeddings.embed_query("test")
    print("SUCCESS: Embeddings generated.")
except Exception as e:
    print(f"FAILURE: Embeddings failed. Error: {e}")

print("\n--- 2. Testing LLM (Chat Dependency) ---")
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
    resp = llm.invoke([HumanMessage(content="Hello")])
    print(f"SUCCESS: LLM responded: {resp.content}")
except Exception as e:
    print(f"FAILURE: LLM failed. Error: {e}")
