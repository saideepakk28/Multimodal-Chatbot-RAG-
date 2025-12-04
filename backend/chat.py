import os
print("Loading backend.chat...")
from typing import List, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.rag import retrieve_documents

load_dotenv()

# Initialize Gemini LLM
# Using gemini-pro as fallback for better availability
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0,
    max_retries=2,
    api_key=os.getenv("GOOGLE_API_KEY")
)

@tool
def calculator(expression: str) -> str:
    """Calculates the result of a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error calculating: {str(e)}"

tools = [calculator]

# System prompt
system_prompt = """You are a helpful multimodal assistant with RAG capabilities.
You have access to a calculator tool.
When answering questions, use the provided context if available.
If the user provides an image, analyze it as requested.
"""

def process_chat(message: str, history: List[BaseMessage], image_url: Optional[str] = None) -> str:
    """
    Processes the user message with RAG, Tools, and optional Image.
    """
    
    # 1. RAG Retrieval
    docs = retrieve_documents(message)
    context_text = "\n\n".join([doc.page_content for doc in docs])
    
    # 2. Construct Messages
    augmented_system_prompt = system_prompt + f"\n\nContext from documents:\n{context_text}"
    
    messages = [SystemMessage(content=augmented_system_prompt)]
    messages.extend(history)
    
    user_content = [{"type": "text", "text": message}]
    if image_url:
        user_content.append({"type": "image_url", "image_url": {"url": image_url}})
        
    messages.append(HumanMessage(content=user_content))

    # 3. Bind tools and invoke
    llm_with_tools = llm.bind_tools(tools)
    response = llm_with_tools.invoke(messages)
    
    # 4. Handle Tool Calls
    if response.tool_calls:
        messages.append(response)
        for tool_call in response.tool_calls:
            if tool_call["name"] == "calculator":
                result = calculator.invoke(tool_call["args"])
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": result,
                    }
                )
        final_response = llm_with_tools.invoke(messages)
        return final_response.content
    
    return response.content
print("backend.chat loaded.")
