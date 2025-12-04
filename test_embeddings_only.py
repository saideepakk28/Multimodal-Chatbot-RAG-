import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key present: {bool(api_key)}")

try:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )
    vec = embeddings.embed_query("Hello world")
    print(f"Embedding successful. Vector length: {len(vec)}")
except Exception as e:
    print("Embeddings Failed:", e)
