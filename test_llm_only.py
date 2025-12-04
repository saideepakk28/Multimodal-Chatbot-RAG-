import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key present: {bool(api_key)}")

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        api_key=api_key
    )
    msg = [HumanMessage(content="Hello, are you working?")]
    response = llm.invoke(msg)
    print("LLM Response:", response.content)
except Exception as e:
    print("LLM Failed:", e)
