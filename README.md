# Multimodal RAG Chatbot

A powerful multimodal chatbot capable of processing text and images, leveraging Retrieval-Augmented Generation (RAG) for enhanced context, and performing tool calls (e.g., Calculator). Built with FastAPI, LangChain, Groq, and ChromaDB.

## 🚀 Features

-   **Multimodal Capabilities**: Analyze images using Llama 3.2 Vision (or compatible models).
-   **RAG (Retrieval-Augmented Generation)**: Upload PDF or TXT files to chat with your own data.
-   **Tool Calling**: Integrated calculator tool for mathematical operations.
-   **Modern UI**: Sleek, dark-themed interface built with Vanilla JS and CSS.
-   **FastAPI Backend**: High-performance asynchronous backend.

## 🛠️ Tech Stack

-   **Backend**: Python, FastAPI, Uvicorn
-   **AI/LLM**: LangChain, Groq API (Llama 3, Mixtral, Gemma)
-   **Vector Store**: ChromaDB
-   **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
-   **Frontend**: HTML5, CSS3, Vanilla JavaScript

## 📋 Prerequisites

-   Python 3.8+
-   Groq API Key (Get one at [console.groq.com](https://console.groq.com))

## 🔧 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/saideepakk28/Multimodal-Chatbot-RAG-.git
    cd Multimodal-Chatbot-RAG-
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables**:
    Create a `.env` file in the root directory and add your Groq API key:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    ```

## 🏃‍♂️ Running the Application

1.  **Start the server**:
    ```bash
    uvicorn backend.main:app --host 0.0.0.0 --port 8000
    ```

2.  **Access the Chatbot**:
    Open your browser and navigate to `http://localhost:8000`.

## 💡 How to Use

1.  **Upload Data**: Click "Choose File" in the sidebar to upload PDF or TXT documents. The chatbot will use these for context.
2.  **Chat**: Type your message in the input box.
3.  **Image Analysis**: Click the image icon to upload a photo and ask questions about it.
4.  **Calculator**: Ask math questions (e.g., "What is 123 * 456?"), and the bot will use the calculator tool.

## ⚠️ Known Issues

-   **Groq Model Availability**: Some vision models (like `llama-3.2-11b-vision-preview`) may be decommissioned or unavailable. The code is configured to fallback to stable text models (e.g., `llama-3.1-8b-instant`), but image analysis features will be disabled in that case.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
