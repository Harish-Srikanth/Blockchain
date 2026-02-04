import React, { useState, useEffect } from "react";

export default function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  // Fetch messages from backend
  const fetchMessages = async () => {
    const res = await fetch("http://localhost:5000/messages");
    const data = await res.json();
    setMessages(data);
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    await fetch("http://localhost:5000/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    setMessage("");
    fetchMessages();
  };

  useEffect(() => {
    fetchMessages();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <h1 className="text-2xl font-bold mb-4 text-blue-600">🔐 Quantum Secure Messenger</h1>

      <form onSubmit={sendMessage} className="flex gap-2 mb-6">
        <input
          className="border rounded-lg p-2 w-80"
          placeholder="Enter your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          required
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          Send
        </button>
      </form>

      <div className="bg-white shadow-lg rounded-lg w-full max-w-2xl p-4">
        <h2 className="text-lg font-semibold mb-2 text-gray-700">🗂️ Secure Messages</h2>
        {messages.length === 0 ? (
          <p className="text-gray-500 text-center">No messages yet...</p>
        ) : (
          messages.map((msg, i) => (
            <div key={i} className="p-2 border-b border-gray-200">
              <p><strong>From:</strong> Node {msg.sender}</p>
              <p><strong>Message:</strong> {msg.decrypted}</p>
              <p className="text-xs text-gray-400 italic">Stored securely on blockchain.</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
