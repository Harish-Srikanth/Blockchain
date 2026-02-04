const socket = io();

const messagesList = document.getElementById("messages");
const senderInput = document.getElementById("sender");
const messageInput = document.getElementById("message");

socket.on("history", (messages) => {
    messagesList.innerHTML = "";
    messages.forEach(addMessage);
});

socket.on("new_message", (msg) => {
    addMessage(msg);
    refreshImage();
});

function sendMessage() {
    const sender = senderInput.value;
    const message = messageInput.value.trim();
    if (!message) return;

    socket.emit("send_message", {
        sender: sender,
        message: message
    });

    messageInput.value = "";
}

function addMessage(msg) {
    const li = document.createElement("li");
    li.innerHTML = `<b>${msg.sender}</b> → ${msg.receiver}: ${msg.message}
                    <br><small>${msg.timestamp} [${msg.verification}]</small>`;
    messagesList.appendChild(li);
}

function refreshImage() {
    const img = document.getElementById("blockchainImage");
    img.src = "/blockchain/image?" + new Date().getTime();
}
