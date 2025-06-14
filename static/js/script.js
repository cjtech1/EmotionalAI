document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const chatMessages = document.getElementById("chatMessages");
  const userInput = document.getElementById("userInput");
  const sendButton = document.getElementById("sendButton");
  const resetButton = document.getElementById("resetBtn");
  const resourcesContainer = document.getElementById("resourcesContainer");
  const resourcesContent = document.getElementById("resourcesContent");
  const closeResources = document.getElementById("closeResources");
  const exerciseContainer = document.getElementById("exerciseContainer");
  const exerciseContent = document.getElementById("exerciseContent");
  const closeExercise = document.getElementById("closeExercise");

  // Event Listeners
  sendButton.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  resetButton.addEventListener("click", resetConversation);
  closeResources.addEventListener("click", () => {
    resourcesContainer.style.display = "none";
  });
  closeExercise.addEventListener("click", () => {
    exerciseContainer.style.display = "none";
  });

  // Focus input field when page loads
  userInput.focus();

  // Handle sending messages
  function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Add user message to chat
    appendMessage(message, "user");

    // Clear input field
    userInput.value = "";

    // Show typing indicator
    showTypingIndicator();

    // Send message to server
    fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ message }),
    })
      .then((response) => {
        const contentType = response.headers.get("content-type");

        // Check if response is JSON
        if (contentType && contentType.indexOf("application/json") !== -1) {
          return response.json();
        } else {
          // Try to handle non-JSON responses by converting to text first
          return response.text().then((text) => {
            console.error("Server returned non-JSON response:", text);

            // Try to parse as JSON anyway (sometimes content-type is wrong)
            try {
              return JSON.parse(text);
            } catch (parseError) {
              // If it can't be parsed as JSON, return a formatted error
              throw new Error(
                "Server did not return valid JSON. Response: " +
                  (text.length > 100 ? text.substring(0, 100) + "..." : text)
              );
            }
          });
        }
      })
      .then((data) => {
        // Remove typing indicator
        removeTypingIndicator();

        // Add bot response to chat
        appendMessage(data.message, "bot");

        // Display resources if provided
        if (data.resources) {
          displayResources(data.resources);
        }

        // Display exercise if provided
        if (data.exercise) {
          displayExercise(data.exercise);
        }

        // Scroll to bottom
        scrollToBottom();
      })
      .catch((error) => {
        console.error("Error:", error);
        removeTypingIndicator();

        // Extract more helpful error message if available
        let errorMessage = "Sorry, I encountered an error. Please try again.";

        // Try to get more specific error from the server response
        if (error.message && error.message.includes("Response:")) {
          try {
            // Try to extract JSON from the error message
            const jsonStr = error.message.split("Response:")[1].trim();
            const parsedError = JSON.parse(jsonStr);
            if (parsedError && parsedError.message) {
              errorMessage = parsedError.message;
            }
          } catch (parseError) {
            console.error("Error parsing error response:", parseError);
          }
        }

        appendMessage(errorMessage, "bot");
      });
  }

  // Append a message to the chat
  function appendMessage(content, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}-message`;

    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";

    // If it's a bot message, parse Markdown, otherwise use plain text
    if (sender === "bot") {
      contentDiv.innerHTML = marked.parse(content);
    } else {
      const paragraph = document.createElement("p");
      paragraph.textContent = content;
      contentDiv.appendChild(paragraph);
    }

    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);

    scrollToBottom();
  }

  // Show typing indicator
  function showTypingIndicator() {
    const typingDiv = document.createElement("div");
    typingDiv.className = "message bot-message typing-indicator";
    typingDiv.id = "typingIndicator";

    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";

    const dots = document.createElement("p");
    dots.innerHTML = "<span>.</span><span>.</span><span>.</span>";

    contentDiv.appendChild(dots);
    typingDiv.appendChild(contentDiv);
    chatMessages.appendChild(typingDiv);

    scrollToBottom();
  }

  // Remove typing indicator
  function removeTypingIndicator() {
    const typingIndicator = document.getElementById("typingIndicator");
    if (typingIndicator) {
      typingIndicator.remove();
    }
  }

  // Display resources
  function displayResources(resources) {
    resourcesContent.innerHTML = "";

    const messageElement = document.createElement("p");
    messageElement.textContent = resources.message;
    resourcesContent.appendChild(messageElement);

    resources.resources.forEach((resource) => {
      const resourceItem = document.createElement("div");
      resourceItem.className = "resource-item";

      const name = document.createElement("h3");
      name.textContent = resource.name;
      resourceItem.appendChild(name);

      const description = document.createElement("p");
      description.textContent = resource.description;
      resourceItem.appendChild(description);

      if (resource.website) {
        const website = document.createElement("p");
        const link = document.createElement("a");
        link.href = resource.website;
        link.target = "_blank";
        link.className = "resource-link";
        link.textContent = "Visit Website";
        website.appendChild(link);
        resourceItem.appendChild(website);
      }

      if (resource.contact) {
        const contact = document.createElement("p");
        contact.textContent = `Contact: ${resource.contact}`;
        resourceItem.appendChild(contact);
      }

      if (resource.helpline) {
        const helpline = document.createElement("p");
        helpline.textContent = `Helpline: ${resource.helpline}`;
        resourceItem.appendChild(helpline);
      }

      resourcesContent.appendChild(resourceItem);
    });

    resourcesContainer.style.display = "block";
  }

  // Display exercise
  function displayExercise(exercise) {
    exerciseContent.innerHTML = "";

    const name = document.createElement("h3");
    name.className = "exercise-name";
    name.textContent = exercise.name;
    exerciseContent.appendChild(name);

    const description = document.createElement("p");
    description.className = "exercise-description";
    description.textContent = exercise.description;
    exerciseContent.appendChild(description);

    const benefits = document.createElement("p");
    benefits.className = "exercise-benefits";
    benefits.textContent = `Benefits: ${exercise.benefits}`;
    exerciseContent.appendChild(benefits);

    exerciseContainer.style.display = "block";
  }

  // Reset conversation
  function resetConversation() {
    fetch("/api/reset", {
      method: "POST",
    })
      .then((response) => {
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.indexOf("application/json") !== -1) {
          return response.json();
        } else {
          return response.text().then((text) => {
            throw new Error("Server did not return JSON. Response: " + text);
          });
        }
      })
      .then((data) => {
        chatMessages.innerHTML = "";
        appendMessage(
          "Hello! I'm Mind Companion, your mental health support chatbot. How are you feeling today?",
          "bot"
        );
        resourcesContainer.style.display = "none";
        exerciseContainer.style.display = "none";
      })
      .catch((error) => console.error("Error:", error));
  }

  // Scroll chat to bottom
  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});
