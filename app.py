from flask import Flask, request, redirect
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Telegram bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Firebase setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def check_telegram_auth(data):
    auth_data = data.copy()
    check_hash = auth_data.pop("hash")
    sorted_data = sorted([f"{k}={v}" for k, v in auth_data.items()])
    data_check_string = "\n".join(sorted_data)
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    h = hashlib.sha256(data_check_string.encode()).hexdigest()
    return h == check_hash

@app.route("/auth/telegram")
def telegram_auth():
    data = request.args.to_dict()
    if not check_telegram_auth(data):
        return "Invalid login", 403

    telegram_id = data["id"]
    username = data.get("username", "unknown")
    full_name = f"{data.get('first_name', '')} {data.get('last_name', '')}"
    photo_url = data.get("photo_url", "")

    user_ref = db.collection("users").document(str(telegram_id))
    if not user_ref.get().exists:
        user_ref.set({
            "telegram_id": telegram_id,
            "username": username,
            "full_name": full_name,
            "photo_url": photo_url
        })

    return redirect(f"/welcome/{username}")

@app.route("/welcome/<username>")
def welcome(username):
    return f"Welcome {username}! You are logged in using Telegram."

if __name__ == "__main__":
    app.run(debug=True)
