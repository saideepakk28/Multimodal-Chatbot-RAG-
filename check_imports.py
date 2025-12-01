import sys
import os
print(f"CWD: {os.getcwd()}")
try:
    print(f"Files in backend: {os.listdir('backend')}")
except Exception as e:
    print(f"Error listing backend: {e}")

try:
    import backend.chat
    print("Successfully imported backend.chat")
except Exception as e:
    print(f"Failed to import backend.chat: {e}")
