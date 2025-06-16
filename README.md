# Mind Companion: Mental Health Chatbot

Mind Companion is an empathetic AI chatbot designed to provide mental health support, motivation, and resources to users.

## Features

- **Empathetic Responses**: The chatbot provides supportive and understanding messages tailored to the user's emotional state.
- **Mental Health Detection**: Identifies potential signs of anxiety, depression, burnout, or crisis situations.
- **Exercise Suggestions**: Offers appropriate mental health exercises such as breathing techniques, mindfulness practices, and journaling prompts.
- **Resource Recommendations**: Provides relevant mental health resources based on the detected concern level.
- **Beautiful UI**: Clean, responsive interface designed for a calming user experience.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Google API key

### Installation

1. Clone the repository (if applicable) or navigate to the project directory:

   ```
   git clone https://github.com/cjtech1/EmotionalAI.git
   ```

2. Create and activate a virtual environment:

   ```
   python3 -m venv
   source venv/bin/activate
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Set up your Google API key:
   Create a `.env` file in the project root and add your API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

### Running the Application

1. Start the Flask application:

   ```
   python app.py
   ```

2. Open a web browser and go to:
   ```
   http://localhost:5000
   ```

## Usage

1. Type your message in the input field at the bottom of the chat interface.
2. Press Enter or click the send button to send your message.
3. The chatbot will respond with supportive messages.
4. Based on your conversation, you may receive:
   - Exercise suggestions to help manage your emotions
   - Relevant mental health resources
5. Click the "Reset Conversation" button at any time to start a new conversation.

## Important Note

This chatbot is not a substitute for professional mental health care. If you or someone you know is in crisis, please contact a mental health professional or crisis service immediately.

## Technology Stack

- Flask: Web framework
- OpenAI API: For generating empathetic responses
- NLTK: For natural language processing
- HTML/CSS/JavaScript: Frontend interface

## Acknowledgments

This project was created as part of a hackathon focusing on mental health support applications.
