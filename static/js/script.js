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
  const darkModeToggle = document.getElementById("darkModeToggle");
  const moodTracker = document.getElementById("moodTracker");
  const moodOptions = document.querySelectorAll(".mood-option");
  const welcomeScreen = document.getElementById("welcomeScreen");
  const scrollToBottomBtn = document.getElementById("scrollToBottom");
  const suggestionChips = document.querySelectorAll(".suggestion-chip");

  // Dark Mode Setup
  const prefersDarkMode = window.matchMedia(
    "(prefers-color-scheme: dark)"
  ).matches;

  // Check if dark mode was previously set
  if (
    localStorage.getItem("darkMode") === "true" ||
    (prefersDarkMode && localStorage.getItem("darkMode") === null)
  ) {
    document.body.classList.add("dark-mode");
    darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
  }

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

  // Dark mode toggle
  darkModeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");

    // Update icon
    if (document.body.classList.contains("dark-mode")) {
      darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
      localStorage.setItem("darkMode", "true");
    } else {
      darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
      localStorage.setItem("darkMode", "false");
    }
  });

  // Mood tracking
  moodOptions.forEach((option) => {
    option.addEventListener("click", () => {
      // Remove selected class from all options
      moodOptions.forEach((btn) => btn.classList.remove("selected"));

      // Add selected class to clicked option
      option.classList.add("selected");

      // Send mood to chat
      const mood = option.getAttribute("data-mood");
      userInput.value = `I'm feeling ${mood} today`;
      sendMessage();

      // Hide mood tracker with animation
      moodTracker.style.animation = "slideInUp 0.5s ease-out forwards reverse";
      setTimeout(() => {
        moodTracker.style.display = "none";
      }, 500);
    });
  });

  // Scroll to bottom button
  chatMessages.addEventListener("scroll", () => {
    const isScrolledToBottom =
      chatMessages.scrollHeight - chatMessages.clientHeight <=
      chatMessages.scrollTop + 100;
    if (!isScrolledToBottom) {
      scrollToBottomBtn.classList.add("visible");
    } else {
      scrollToBottomBtn.classList.remove("visible");
    }
  });

  scrollToBottomBtn.addEventListener("click", () => {
    scrollToBottom();
  });

  // Suggestion chips
  suggestionChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      userInput.value = chip.textContent;
      sendMessage();
    });
  });

  // Hide welcome screen after animation completes
  setTimeout(() => {
    welcomeScreen.style.display = "none";
  }, 3500);

  // Focus input field when page loads (after welcome animation)
  setTimeout(() => {
    userInput.focus();
  }, 3600);

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

      // Add reaction buttons to bot messages
      const reactionsDiv = document.createElement("div");
      reactionsDiv.className = "message-reactions";

      const reactions = [
        { emoji: "❤️", title: "Thank you" },
        { emoji: "👍", title: "Helpful" },
        { emoji: "🔄", title: "Try another response" },
      ];

      reactions.forEach((reaction) => {
        const button = document.createElement("button");
        button.className = "reaction-button";
        button.innerHTML = reaction.emoji;
        button.title = reaction.title;

        // Add event listener to reaction buttons
        button.addEventListener("click", () => {
          if (reaction.emoji === "🔄") {
            // Request alternative response
            userInput.value = "Can you give me another perspective on this?";
            sendMessage();
          } else {
            // Show appreciation animation
            button.style.transform = "scale(1.5)";
            setTimeout(() => {
              button.style.transform = "scale(1)";
            }, 300);
          }
        });

        reactionsDiv.appendChild(button);
      });

      contentDiv.appendChild(reactionsDiv);

      // Add suggestion chips for relevant bot messages
      if (
        content.includes("anxiety") ||
        content.includes("stress") ||
        content.includes("feeling") ||
        content.includes("help") ||
        content.includes("support")
      ) {
        const suggestionsDiv = document.createElement("div");
        suggestionsDiv.className = "suggestion-chips";

        const suggestions = [];

        if (content.includes("anxiety") || content.includes("stress")) {
          suggestions.push("How can I manage anxiety?", "Breathing exercises");
        }

        if (content.includes("feeling") || content.includes("mood")) {
          suggestions.push("Why do I feel this way?", "How to improve mood");
        }

        if (content.includes("sleep")) {
          suggestions.push("Sleep meditation", "Insomnia tips");
        }

        if (suggestions.length === 0) {
          suggestions.push(
            "Tell me more",
            "How can you help me?",
            "Mental health tips"
          );
        }

        // Only show up to 3 suggestions
        const finalSuggestions = suggestions.slice(0, 3);

        finalSuggestions.forEach((suggestion) => {
          const chip = document.createElement("button");
          chip.className = "suggestion-chip";
          chip.textContent = suggestion;

          chip.addEventListener("click", () => {
            userInput.value = suggestion;
            sendMessage();
          });

          suggestionsDiv.appendChild(chip);
        });

        contentDiv.appendChild(suggestionsDiv);
      }
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

    // Enhanced typing animation
    const dots = document.createElement("p");
    dots.innerHTML = "<span>.</span><span>.</span><span>.</span>";

    // Add a subtle message to enhance user experience
    const typingText = document.createElement("div");
    typingText.style.fontSize = "0.8rem";
    typingText.style.opacity = "0.7";
    typingText.style.marginTop = "5px";
    typingText.textContent = "Mind Companion is thinking...";

    contentDiv.appendChild(dots);
    contentDiv.appendChild(typingText);
    typingDiv.appendChild(contentDiv);
    chatMessages.appendChild(typingDiv);

    scrollToBottom();

    // Add random typing delay for more natural feel
    if (!window.typingAnimation) {
      window.typingAnimation = setInterval(() => {
        dots.style.opacity = dots.style.opacity === "0.4" ? "1" : "0.4";
      }, 500);
    }
  }

  // Remove typing indicator
  function removeTypingIndicator() {
    const typingIndicator = document.getElementById("typingIndicator");
    if (typingIndicator) {
      // Add fade out animation
      typingIndicator.style.opacity = "0";
      typingIndicator.style.transform = "translateY(10px)";
      typingIndicator.style.transition = "opacity 0.3s, transform 0.3s";

      // Clear typing animation
      if (window.typingAnimation) {
        clearInterval(window.typingAnimation);
        window.typingAnimation = null;
      }

      setTimeout(() => {
        if (typingIndicator.parentNode) {
          typingIndicator.remove();
        }
      }, 300);
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

      // Add a nice fade in animation for each item
      resourceItem.style.animation = "fadeIn 0.5s ease-out forwards";
      resourceItem.style.opacity = "0";

      // Stagger the animations
      const index = Array.from(resourcesContent.children).indexOf(resourceItem);
      resourceItem.style.animationDelay = `${index * 0.15}s`;

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

        // Add icon for better visual cue
        link.innerHTML =
          '<i class="fas fa-external-link-alt"></i> Visit Website';

        website.appendChild(link);
        resourceItem.appendChild(website);
      }

      if (resource.contact) {
        const contact = document.createElement("p");
        contact.innerHTML = `<i class="fas fa-address-card"></i> <strong>Contact:</strong> ${resource.contact}`;
        resourceItem.appendChild(contact);
      }

      if (resource.helpline) {
        const helpline = document.createElement("p");
        helpline.innerHTML = `<i class="fas fa-phone"></i> <strong>Helpline:</strong> ${resource.helpline}`;
        resourceItem.appendChild(helpline);
      }

      resourcesContent.appendChild(resourceItem);
    });

    resourcesContainer.style.display = "block";

    // Animation effect
    resourcesContainer.style.animation = "slideInUp 0.5s ease-out";
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

    // Add breathing exercise animation for breathing-related exercises
    if (
      exercise.name.toLowerCase().includes("breath") ||
      exercise.description.toLowerCase().includes("breath")
    ) {
      const breathingDiv = document.createElement("div");
      breathingDiv.className = "breathing-exercise";

      const circle = document.createElement("div");
      circle.className = "breathing-circle";
      circle.innerHTML = "Breathe";

      const instructions = document.createElement("p");
      instructions.className = "breathing-instructions";
      instructions.innerHTML =
        "Breathe in as the circle expands<br>Breathe out as it contracts";

      breathingDiv.appendChild(circle);
      breathingDiv.appendChild(instructions);

      exerciseContent.appendChild(breathingDiv);
    }

    exerciseContainer.style.display = "block";

    // Animation effect
    exerciseContainer.style.animation = "slideInUp 0.5s ease-out";
  }

  // Reset conversation
  function resetConversation() {
    // Add loading animation
    chatMessages.innerHTML = `
      <div class="message bot-message">
        <div class="message-content">
          <p>Resetting our conversation...</p>
        </div>
      </div>
    `;

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
        // Fade out effect before clearing
        const messages = chatMessages.querySelectorAll(".message");
        messages.forEach((msg) => {
          msg.style.opacity = "0";
          msg.style.transform = "translateY(20px)";
          msg.style.transition = "opacity 0.5s, transform 0.5s";
        });

        setTimeout(() => {
          chatMessages.innerHTML = "";

          // Show mood tracker again
          moodTracker.style.display = "block";
          moodTracker.style.animation = "slideInDown 0.5s ease-out";

          // Reset mood options
          moodOptions.forEach((option) => {
            option.classList.remove("selected");
          });

          // Add welcome message
          appendMessage(
            "Hello! I'm Mind Companion, your mental health support chatbot. How are you feeling today?",
            "bot"
          );

          // Add suggestion chips
          const firstMessage = chatMessages.querySelector(".bot-message");
          if (firstMessage) {
            const suggestionsDiv = document.createElement("div");
            suggestionsDiv.className = "suggestion-chips";

            const suggestions = [
              "I'm feeling anxious",
              "Feeling down today",
              "Need help managing stress",
              "Can't sleep well",
            ];

            suggestions.forEach((text) => {
              const chip = document.createElement("button");
              chip.className = "suggestion-chip";
              chip.textContent = text;

              chip.addEventListener("click", () => {
                userInput.value = text;
                sendMessage();
              });

              suggestionsDiv.appendChild(chip);
            });

            firstMessage
              .querySelector(".message-content")
              .appendChild(suggestionsDiv);
          }

          // Hide resources and exercise containers
          resourcesContainer.style.display = "none";
          exerciseContainer.style.display = "none";
        }, 500);
      })
      .catch((error) => console.error("Error:", error));
  }

  // Scroll chat to bottom
  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});
