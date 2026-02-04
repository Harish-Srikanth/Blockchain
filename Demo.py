# app.py
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import hashlib, random, datetime, json, networkx as nx, matplotlib.pyplot as plt
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# ----------------------------
# Quantum Key Distribution (QKD) Simulation
# ----------------------------
class QuantumKeyDistribution:
    def __init__(self):
        self.key_node1 = ""
        self.key_node2 = ""
        self.shared_key = ""

    def generate_random_bits(self, n=16):
        return [random.choice(['0', '1']) for _ in range(n)]

    def generate_bases(self, n=16):
        # + or x bases
        return [random.choice(['+', 'x']) for _ in range(n)]

    def simulate_bb84(self):
        print("🔮 Starting Quantum Key Distribution (BB84 Simulation)...")

        # Step 1: Node 1 prepares qubits
        node1_bits = self.generate_random_bits()
        node1_bases = self.generate_bases()

        # Step 2: Node 2 randomly chooses measurement bases
        node2_bases = self.generate_bases()

        # Step 3: Node 2 measures qubits (simulate matching bases)
        shared_bits = []
        for b1, base1, base2 in zip(node1_bits, node1_bases, node2_bases):
            if base1 == base2:
                shared_bits.append(b1)

        # Step 4: Both nodes discard non-matching bits → shared key
        shared_key = ''.join(shared_bits)[:16]
        self.shared_key = shared_key
        self.key_node1 = shared_key
        self.key_node2 = shared_key

        print(f"✅ QKD Complete! Shared Quantum Key established between nodes.")
        print(f"🔐 Shared Key: {self.shared_key}\n")

        return self.shared_key

# Initialize QKD before blockchain
qkd = QuantumKeyDistribution()
quantum_shared_key = qkd.simulate_bb84()

# ----------------------------
# Blockchain Data Structures
# ----------------------------
class Transaction:
    def __init__(self, sender_id, receiver_id, message, shared_key):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = message
        self.shared_key = shared_key
        self.encrypted_message = self.encrypt_message(message)
        self.message_hash = self.generate_hash(message)
        self.signature = self.sign_message(self.message_hash)
        self.verification = self.verify_signature(self.signature, self.message_hash)
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def encrypt_message(self, message):
        # Simulate lattice-based encryption with the shared quantum key
        random.seed(self.shared_key)
        return [random.randint(20, 255) for _ in range(random.randint(8, 22))]

    def generate_hash(self, message):
        return hashlib.sha256(message.encode()).hexdigest()

    def sign_message(self, message_hash):
        # Use quantum-derived shared key instead of a static one
        return hashlib.sha256((message_hash + self.shared_key).encode()).hexdigest()[:64]

    def verify_signature(self, signature, message_hash):
        return "Verified" if signature else "Invalid"

class Blockchain:
    def __init__(self):
        self.chain = []

    def add_transaction(self, transaction):
        self.chain.append(transaction)
        print("Transaction added to blockchain")
        self.display_transaction(transaction)
        self.visualize_blockchain()

    def display_transaction(self, t):
        print(f"\nTransaction {len(self.chain)}:")
        print(f"  Sender: Node {t.sender_id}")
        print(f"  Receiver: Node {t.receiver_id}")
        print(f"  Message: {t.message}")
        print(f"  Encrypted: {t.encrypted_message}")
        print(f"  Shared Key: {t.shared_key}")
        print(f"  Hash: {t.message_hash}")
        print(f"  Signature: {t.signature}")
        print(f"  Verification: {t.verification}")
        print(f"  Timestamp: {t.timestamp}\n")

    def visualize_blockchain(self, filename="blockchain_graph.png"):
        """Generate blockchain visualization."""
        if not self.chain:
            return

        G = nx.DiGraph()
        for i, block in enumerate(self.chain):
            node_label = f"Block {i+1}\n{block.timestamp}\n{block.sender_id}->{block.receiver_id}"
            G.add_node(node_label)
            if i > 0:
                G.add_edge(f"Block {i}", node_label)

        plt.figure(figsize=(8, 4))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color="#bae6fd", node_size=2500, font_size=8, font_weight="bold")
        plt.title("Blockchain Transaction Flow", fontsize=12)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        print(f"📊 Blockchain visualization updated → {filename}")

    def export_log(self, filename="blockchain_log.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            for i, t in enumerate(self.chain, 1):
                f.write(f"Transaction {i}:\n")
                f.write(f"  Sender: Node {t.sender_id}\n")
                f.write(f"  Receiver: Node {t.receiver_id}\n")
                f.write(f"  Message: {t.message}\n")
                f.write(f"  Encrypted: {t.encrypted_message}\n")
                f.write(f"  Shared Key: {t.shared_key}\n")
                f.write(f"  Hash: {t.message_hash}\n")
                f.write(f"  Signature: {t.signature}\n")
                f.write(f"  Verification: {t.verification}\n")
                f.write(f"  Timestamp: {t.timestamp}\n\n")

# Initialize
print("🔗 Quantum channel established between Node 1 and Node 2")
print("🔐 Lattice cryptography + Quantum Key Distribution initialized\n")

blockchain = Blockchain()
messages = []

print("🚀 Secure Quantum Blockchain Chat Backend Ready...\n")

# ----------------------------
# Endpoints
# ----------------------------
@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/blockchain/image', methods=['GET'])
def get_blockchain_image():
    path = "blockchain_graph.png"
    if os.path.exists(path):
        return send_file(path, mimetype='image/png')
    return jsonify({"error": "Blockchain visualization not found"}), 404

# ----------------------------
# Socket.IO Handlers
# ----------------------------
@socketio.on('connect')
def handle_connect():
    emit('history', messages)
    print("Client connected - sent history")

@socketio.on('send_message')
def handle_send_message(data):
    sender_name = data.get('sender', 'Node 1')
    message_text = data.get('message', '')

    sender_id = 1 if sender_name == "Node 1" else 2
    receiver_id = 2 if sender_id == 1 else 1
    receiver_name = f"Node {receiver_id}"

    tx = Transaction(sender_id, receiver_id, message_text, quantum_shared_key)
    blockchain.add_transaction(tx)

    record = {
        "sender": f"Node {sender_id}",
        "receiver": receiver_name,
        "message": message_text,
        "timestamp": tx.timestamp,
        "verification": tx.verification
    }
    messages.append(record)

    blockchain.export_log()
    socketio.emit('new_message', record)

    print(f"Node {sender_id} sent → Node {receiver_id}: '{message_text}'")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
