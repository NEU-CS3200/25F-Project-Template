import os
import json

MODULES_DIR = os.path.dirname(os.path.abspath(__file__))

# datasets folder is outside app/, at the same level as app/
PROJECT_ROOT = os.path.abspath(os.path.join(MODULES_DIR, "..", ".."))
DATASETS_DIR = os.path.join(PROJECT_ROOT, "datasets")
CHAT_FILE = os.path.join(DATASETS_DIR, "messages.json")

def load_chats():
    if not os.path.exists(CHAT_FILE):
        return {"customers": {}}
    try:
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"customers": {}}

def save_chats(data):
    # ensure datasets folder exists (optional if it always exists)
    os.makedirs(DATASETS_DIR, exist_ok=True)
    with open(CHAT_FILE, "w") as f:
        json.dump(data, f, indent=4)


