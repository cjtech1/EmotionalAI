# Mind Companion - Mental Health Chatbot

## Project Overview

Mind Companion is an interactive chatbot application designed to provide mental health support to users. The application combines modern web technologies with AI-powered conversation capabilities to create a supportive space for users to express their feelings and receive appropriate guidance, resources, and exercises.

## Key Features

- **Intelligent Conversation**: Engages users in supportive mental health discussions
- **Emotion Recognition**: Detects signs of anxiety, depression, burnout, and suicidal ideation
- **Resource Recommendations**: Provides relevant mental health resources based on conversation context
- **Exercise Suggestions**: Offers appropriate mental wellness exercises based on detected emotional states
- **Interactive UI**: Modern, responsive interface with animations and mood tracking
- **Dark Mode**: Support for light/dark theme preferences
- **Suggestion Chips**: Quick-response options for common queries
- **Breathing Exercises**: Visual breathing exercise animations for relaxation
- **Conversation Reset**: Ability to start a new conversation session

## Technology Stack

### Backend Technologies

1. **Python 3**: Core programming language for the backend application

   - Used for processing user inputs, generating responses, and managing application logic

2. **Flask**: Lightweight Python web framework

   - Handles HTTP requests and responses
   - Routes API endpoints
   - Serves static files and HTML templates
   - Manages user sessions

3. **Natural Language Processing (NLP)**:

   - **NLTK (Natural Language Toolkit)**: Used for text tokenization and basic language processing
   - Custom keyword-based mental health issue detection algorithms

4. **State Management**:
   - Flask session handling for maintaining conversation history
   - Server-side conversation tracking with unique session IDs

### Frontend Technologies

1. **HTML5**: Markup language for structuring web content

   - Semantic elements for better accessibility and SEO

2. **CSS3**: Styling language for designing the user interface

   - Custom animations and transitions
   - Responsive design for all device sizes
   - CSS variables for theming and consistent styling
   - Dark mode support

3. **JavaScript (ES6+)**: Client-side programming

   - DOM manipulation for dynamic content updates
   - Event handling for user interactions
   - Fetch API for asynchronous communication with the backend
   - Animation effects and transitions

4. **Marked.js**: JavaScript library for Markdown parsing

   - Converts markdown from bot responses to formatted HTML

5. **Font Awesome**: Icon library
   - Provides scalable vector icons for UI elements

### User Interface Elements

1. **Mood Tracker**: Interactive component for users to select their current emotional state

   - Uses emoji representations for easy emotional expression
   - Sends mood data to the chatbot for contextual responses

2. **Suggestion Chips**: Quick-response buttons for common user queries

   - Dynamically generated based on conversation context
   - Simplifies user input for common questions

3. **Message Reactions**: Emoji reactions for bot messages

   - Allows users to provide quick feedback on responses
   - "Try another response" option for alternative perspectives

4. **Breathing Exercise Visualization**: Animated circle that expands and contracts

   - Visual guide for breathing exercises
   - Helps users practice mindfulness and stress reduction techniques

5. **Dark Mode Toggle**: Switch between light and dark themes
   - Persists user preference across sessions using localStorage
   - Respects system color scheme preferences

### Data Analysis

1. **Sentiment Analysis**: Basic sentiment detection through keyword matching

   - Categorizes user messages into emotional states (anxiety, depression, burnout)
   - Identifies potential crisis situations requiring immediate attention

2. **Concern Level Assessment**: Algorithm to determine severity of mental health concerns
   - Categorizes concerns as low, moderate, high, or critical
   - Triggers appropriate response strategies based on severity

## Application Architecture

### MVC-inspired Structure

The application follows a Model-View-Controller inspired architecture:

1. **Model** (Data handling):

   - Conversation history storage
   - Mental health issue detection
   - Resource and exercise recommendation logic

2. **View** (User interface):

   - HTML templates
   - CSS styling
   - Client-side JavaScript for UI interactions

3. **Controller** (Application logic):
   - Flask routes and endpoints
   - Request/response handling
   - Session management

### API Endpoints

1. `/api/chat` (POST)

   - Receives user messages
   - Returns bot responses with optional resources and exercises

2. `/api/reset` (POST)
   - Resets the conversation history
   - Starts a new chat session

## Utility Modules

1. **mental_health_utils.py**:

   - Contains functions to detect potential mental health issues from user input
   - Calculates confidence scores for different emotional states
   - Determines overall concern level

2. **response_generator.py**:

   - Generates appropriate responses based on detected mental health issues
   - Customizes response tone and content based on conversation context

3. **mental_health_resources.py**:

   - Provides relevant mental health resources based on concern level
   - Contains database of mental health organizations, websites, and helplines

4. **exercise_suggestions.py**:
   - Suggests mental health exercises based on detected emotional states
   - Contains a variety of breathing techniques, mindfulness exercises, and coping strategies

## User Experience Flow

1. **Initial Greeting**:

   - Welcome animation introduces the application
   - Bot greets user and asks about their feelings
   - Suggestion chips offer common conversation starters

2. **Mood Selection**:

   - User can select their current mood from emoji options
   - Selection informs the bot about user's emotional state

3. **Conversation**:

   - User types messages or selects suggestion chips
   - Bot responds with supportive messages
   - Typing animation indicates when the bot is processing

4. **Resource Provision**:

   - Resources appear when moderate to critical concerns are detected
   - Resources include relevant mental health organizations and helplines

5. **Exercise Suggestions**:

   - Mental wellness exercises are suggested when appropriate
   - Breathing exercises include interactive visual guidance

6. **Conversation Reset**:
   - User can reset the conversation at any time
   - New session begins with fresh context

## Security and Privacy Considerations

1. **Session Management**:

   - Unique session IDs for conversation tracking
   - No personal data storage beyond the current session

2. **Crisis Detection**:

   - Immediate flagging of potential crisis situations
   - Clear disclaimer about limitations of the tool

3. **Data Handling**:
   - Conversation data stored temporarily in server memory
   - No persistent storage of user conversations

## Future Enhancement Opportunities

1. **Advanced NLP**: Integrate more sophisticated natural language processing capabilities
2. **User Authentication**: Optional accounts for returning users to maintain conversation history
3. **More Exercise Types**: Expand the variety of mental wellness exercises
4. **Voice Interaction**: Add speech recognition and text-to-speech capabilities
5. **Progressive Web App**: Enable offline functionality and mobile installation

## Development Team

This application was developed as part of a hackathon project, demonstrating the integration of web technologies and artificial intelligence for mental health support.

---

_Note: This chatbot is not a substitute for professional mental health services. If you're in crisis, please call a mental health hotline or emergency services._
