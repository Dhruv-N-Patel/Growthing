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
 // Fetch genre data from the backend (mocked data for demonstration)
const genres = ['All', 'Programming', 'Design', 'Video Editing', 'Marketing', 'Misc'];

// Function to populate the genre filter options
function populateGenreFilter() {
  const genreFilter = document.getElementById('genre-filter');

  genres.forEach(genre => {
    const li = document.createElement('li');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.name = 'genre';
    checkbox.value = genre;
    checkbox.id = genre.toLowerCase();

    const label = document.createElement('label');
    label.textContent = genre;
    label.htmlFor = genre.toLowerCase();

    li.appendChild(checkbox);
    li.appendChild(label);

    genreFilter.appendChild(li);
  });
}

// Apply the selected filters
function applyFilters() {
  const selectedGenres = Array.from(document.querySelectorAll('input[name="genre"]:checked'))
    .map(checkbox => checkbox.value);

  const selectedDifficultyLevels = Array.from(document.querySelectorAll('input[name="difficulty"]:checked'))
    .map(checkbox => checkbox.value);

  // Do something with the selected genres and difficulty levels
  console.log('Selected Genres:', selectedGenres);
  console.log('Selected Difficulty Levels:', selectedDifficultyLevels);

  // Update the displayed projects based on the selected filters
  const projectTabs = document.getElementsByClassName('project-tab');
  for (let i = 0; i < projectTabs.length; i++) {
    const tab = projectTabs[i];
    if (selectedGenres.includes(tab.id) || selectedGenres.includes('All')) {
      tab.classList.add('active');
    } else {
      tab.classList.remove('active');
    }
  }
}

// Event listener for the "Apply Filters" button
const applyFiltersButton = document.getElementById('apply-filters');
applyFiltersButton.addEventListener('click', applyFilters);

// Initialize the genre filter options
populateGenreFilter();
