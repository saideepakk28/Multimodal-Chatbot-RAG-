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

print("\n--- 1. Testing Embeddings (models/embedding-001) ---")
try:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vec = embeddings.embed_query("test")
    print("SUCCESS: embedding-001 working.")
except Exception as e:
    print(f"FAILURE: embedding-001 failed. Error: {e}")

print("\n--- 2. Testing Embeddings (models/text-embedding-004) ---")
try:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)
    vec = embeddings.embed_query("test")
    print("SUCCESS: text-embedding-004 working.")
except Exception as e:
    print(f"FAILURE: text-embedding-004 failed. Error: {e}")

print("\n--- 3. Testing LLM (gemini-pro) ---")
try:
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
    resp = llm.invoke([HumanMessage(content="Hello")])
    print(f"SUCCESS: gemini-pro responded: {resp.content}")
except Exception as e:
    print(f"FAILURE: gemini-pro failed. Error: {e}")
