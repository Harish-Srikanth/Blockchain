import os
import random
import hashlib
import datetime

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx

from flask import Flask, jsonify, render_template, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit

# ----------------------------
# App setup
# ----------------------------
app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# ----------------------------
# Quantum Key (simple simulation)
# ----------------------------
def generate_quantum_key():
    return ''.join(random.choice(['0', '1']) for _ in range(16))

QUANTUM_KEY = generate_quantum_key()

# ----------------------------
# Blockchain
# ----------------------------
class Transaction:
    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.hash = hashlib.sha256(message.encode()).hexdigest()
        self.signature = hashlib.sha256((self.hash + QUANTUM_KEY).encode()).hexdigest()
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.verification = "Verified"

class Blockchain:
    def __init__(self):
        self.chain = []

    def add(self, tx):
        self.chain.append(tx)
        self.draw_chain()

    def draw_chain(self):
        G = nx.DiGraph()
        for i, tx in enumerate(self.chain):
            label = f"Block {i+1}\n{tx.sender} → {tx.receiver}"
            G.add_node(label)
            if i > 0:
                G.add_edge(f"Block {i}", label)

        plt.figure(figsize=(8, 4))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color="#93c5fd", node_size=2500)
        plt.tight_layout()
        plt.savefig("blockchain_graph.png")
        plt.close()

blockchain = Blockchain()
messages = []

# ----------------------------
# Routes
# ----------------------------

# FRONTEND
@app.route("/")
def index():
    return render_template("index.html")

# BACKEND STATUS
@app.route("/status")
def status():
    return jsonify({"message": "Blockchain project running"})

# BLOCKCHAIN IMAGE
@app.route("/blockchain/image")
def blockchain_image():
    if os.path.exists("blockchain_graph.png"):
        return send_file("blockchain_graph.png", mimetype="image/png")
    return jsonify({"error": "No blockchain data yet"})

# ----------------------------
# Socket.IO
# ----------------------------
@socketio.on("connect")
def connect():
    emit("history", messages)

@socketio.on("send_message")
def handle_message(data):
    sender = data.get("sender", "Node 1")
    receiver = "Node 2" if sender == "Node 1" else "Node 1"
    message = data.get("message", "")

    if not message:
        return

    tx = Transaction(sender, receiver, message)
    blockchain.add(tx)

    record = {
        "sender": sender,
        "receiver": receiver,
        "message": message,
        "timestamp": tx.timestamp,
        "verification": tx.verification
    }

    messages.append(record)
    emit("new_message", record, broadcast=True)

# ----------------------------
# Run (Render-safe)
# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)
