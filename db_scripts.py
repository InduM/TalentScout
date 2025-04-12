import os
import uuid
from cryptography.fernet import Fernet
from pymongo import MongoClient
from dotenv import load_dotenv

KEY_PATH = "fernet.key"

if not os.path.exists(KEY_PATH):
    with open(KEY_PATH, "wb") as f:
        f.write(Fernet.generate_key())

with open(KEY_PATH, "rb") as f:
    key = f.read()

cipher = Fernet(key)
def encrypt(text): return cipher.encrypt(text.encode()).decode()
def decrypt(text): return cipher.decrypt(text.encode()).decode()

load_dotenv()

client =MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB")]
collection = db["candidates"]

def save_candidate(data):
    data['_id'] = str(uuid.uuid4())
    data['name'] = encrypt(data['name'])
    data['email'] = encrypt(data['email'])
    data['phone'] = encrypt(data['phone'])
    result= collection.insert_one(data)
    return result.inserted_id


def delete_candidate(candidate_id):
    collection.delete_one({"_id": candidate_id})



