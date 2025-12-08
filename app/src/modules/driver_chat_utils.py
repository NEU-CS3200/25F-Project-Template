import json

def load_chats(filename="driver_messages.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_chats(chats, filename="driver_messages.json"):
    with open(filename, "w") as f:
        json.dump(chats, f, indent=4)
