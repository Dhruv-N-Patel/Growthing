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
 
  
// Function to fetch project data from the database
function fetchProjectData() {
    // Make an API call to your backend server to fetch the project data from the SQLite database
    // Use the appropriate server-side language and database driver to execute the query

    // For this example, let's assume the API returns the following JSON data
    return fetch('/projects/')
    .then(response => response.json())
    .then(data => data[0]); // Assuming you want to display the first project in the response data
}


// Function to update the project page with the fetched data
function updateProjectPage(data) {
  document.getElementById("project-title").innerText = data.title;
  document.getElementById("project-description").innerText = data.description;
  document.getElementById("project-skills").innerText = data.skills;
}


// Fetch project data and update the page when it loads
window.addEventListener("DOMContentLoaded", function() {
  fetchProjectData()
      .then(projectData => updateProjectPage(projectData));
});