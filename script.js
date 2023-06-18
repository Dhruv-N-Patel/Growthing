document.addEventListener("DOMContentLoaded", function() {
    const chatLog = document.getElementById("chat-log");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
  
    sendButton.addEventListener("click", sendMessage);
    messageInput.addEventListener("keypress", function(event) {
      if (event.key === "Enter") {
        sendMessage();
      }
    });
  
    function sendMessage() {
      const message = messageInput.value;
      if (message.trim() !== "") {
        appendMessage("user", message);
        messageInput.value = "";
        simulateBotReply(message);
      }
    }
  
    function simulateBotReply(userMessage) {
      // Replace this with your own logic for generating bot replies
      const botReply = "This is a sample bot reply.";
      setTimeout(function() {
        appendMessage("bot", botReply);
      }, 500);
    }
  
    function appendMessage(sender, message) {
      const messageContainer = document.createElement("div");
      messageContainer.classList.add(sender === "user" ? "user-message" : "bot-message");
      messageContainer.textContent = message;
      chatLog.appendChild(messageContainer);
      chatLog.scrollTop = chatLog.scrollHeight;
    }
  });
 