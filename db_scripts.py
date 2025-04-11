from cryptography.fernet import Fernet
import uuid
import json
import os

KEY_PATH = "fernet.key"

if not os.path.exists(KEY_PATH):
    with open(KEY_PATH, "wb") as f:
        f.write(Fernet.generate_key())

with open(KEY_PATH, "rb") as f:
    key = f.read()

cipher = Fernet(key)

def encrypt(text): return cipher.encrypt(text.encode()).decode()
def decrypt(text): return cipher.decrypt(text.encode()).decode()

# -------------------------------
# Storage
# -------------------------------
DB_FILE = "candidates.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)
    

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def anonymize_log(text):
    return text.replace("@", "[at]").replace(".", "[dot]")
