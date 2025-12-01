try:
    print("Importing fastapi...")
    import fastapi
    print("Importing langchain_groq...")
    import langchain_groq
    print("Importing langchain_huggingface...")
    import langchain_huggingface
    print("Importing chromadb...")
    import chromadb
    print("Importing langchain_chroma...")
    import langchain_chroma
    print("Imports successful.")
except Exception as e:
    print(f"Import failed: {e}")
