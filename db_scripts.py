from cryptography.fernet import Fernet
import uuid
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

KEY_PATH = "fernet.key"
load_dotenv()

client =MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB")]
collection = db["candidates"]

def save_candidate(data):
    data['_id'] = str(uuid.uuid4())
    print("\n\nDATA SAVED!!!",data)
    result= collection.insert_one(data)
    print("\n\nRESULT!!!",result.inserted_id)
    

def get_candidate(candidate_id):
    doc = collection.find_one({"id": candidate_id})
    if doc:
        doc["name"] = decrypt(doc["name"])
        doc["email"] = decrypt(doc["email"])
    return doc

def delete_candidate(candidate_id):
    collection.delete_one({"_id": candidate_id})




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
