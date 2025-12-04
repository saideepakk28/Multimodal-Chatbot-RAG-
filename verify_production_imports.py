import sys
import os

print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

try:
    print("Attempting to import backend.rag...")
    import backend.rag
    print("Successfully imported backend.rag")
except ImportError as e:
    print(f"Failed to import backend.rag: {e}")
except Exception as e:
    print(f"An error occurred importing backend.rag: {e}")

try:
    print("Attempting to import backend.chat...")
    import backend.chat
    print("Successfully imported backend.chat")
except ImportError as e:
    print(f"Failed to import backend.chat: {e}")
except Exception as e:
    print(f"An error occurred importing backend.chat: {e}")

try:
    print("Attempting to import backend.main...")
    import backend.main
    print("Successfully imported backend.main")
except ImportError as e:
    print(f"Failed to import backend.main: {e}")
except Exception as e:
    print(f"An error occurred importing backend.main: {e}")
