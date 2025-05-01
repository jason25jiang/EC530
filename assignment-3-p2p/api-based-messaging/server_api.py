from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
messages = []  # In-memory store of messages
subscribers = {}

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    username = data.get("username")
    if not username:
        return jsonify({"error": "Username required"}), 400
    if username not in subscribers:
        subscribers[username] = []
    return jsonify({"status": f"{username} subscribed"})

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    sender = data.get("sender")
    recipient = data.get("recipient")
    message = data.get("message")

    if not all([sender, recipient, message]):
        return jsonify({"error": "sender, recipient, and message required"}), 400

    if recipient not in subscribers:
        return jsonify({"error": f"Recipient '{recipient}' not subscribed"}), 404

    msg = {
        "from": sender,
        "message": message,
        "time": datetime.utcnow().isoformat()
    }

    subscribers[recipient].append(msg)
    return jsonify({"status": "Message sent"}), 200

@app.route('/messages', methods=['GET'])
def get_messages(username):
    if username not in subscribers:
        return jsonify({"error": f"User '{username}' not subscribed"}), 404

    user_messages = subscribers[username][:]
    subscribers[username].clear() 

    return jsonify(user_messages), 200

if __name__ == '__main__':
    app.run(host="localhost", port=8000)
