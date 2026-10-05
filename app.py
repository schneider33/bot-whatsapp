from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

PHONE_ID = os.getenv("PHONE_NUMBER_ID", "1399150573276670")
TOKEN = os.getenv("ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "meu_token_123")

@app.route("/")
def home():
    return "Bot Online ✅"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Token inválido", 403
    if request.method == "POST":
        data = request.json
        try:
            entry = data["entry"][0]["changes"][0]["value"]
            if "messages" in entry:
                msg = entry["messages"][0]
                numero = msg["from"]
                texto = msg["text"]["body"]
                resposta = f"Recebi: {texto} 🤖 Bot funcionando!"
                url = f"https://graph.facebook.com/v25.0/{PHONE_ID}/messages"
                headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
                payload = {"messaging_product": "whatsapp","to": numero,"type": "text","text": {"body": resposta}}
                requests.post(url, headers=headers, json=payload)
        except Exception as e:
            print(e)
        return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
