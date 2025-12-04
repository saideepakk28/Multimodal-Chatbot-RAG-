import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("ERROR: GOOGLE_API_KEY not found")
    sys.exit(1)

models_to_test = [
    "gemini-1.5-flash",
    "gemini-pro",
    "gemini-1.0-pro",
    "gemini-1.5-pro"
]

print(f"Testing API Key: {api_key[:5]}...")

for model in models_to_test:
    print(f"\n--- Testing {model} ---")
    try:
        llm = ChatGoogleGenerativeAI(model=model, google_api_key=api_key)
        resp = llm.invoke([HumanMessage(content="Hello")])
        print(f"SUCCESS: {model} responded: {resp.content}")
    except Exception as e:
        print(f"FAILURE: {model} failed. Error: {e}")
