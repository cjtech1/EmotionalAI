# Technical Documentation: Mind Companion Chatbot

This document explains the technical architecture and components of the Mind Companion mental health chatbot.

## Architecture Overview

The Mind Companion chatbot is built with a Flask-based backend and a JavaScript/HTML/CSS frontend. The application uses the OpenAI API to generate empathetic responses while incorporating mental health analysis, exercise suggestions, and resource recommendations.

```
+------------------+      +------------------+      +------------------+
|                  |      |                  |      |                  |
|  Flask Backend   | <--> |   OpenAI API    | <--> | User Interface   |
|                  |      |                  |      |                  |
+------------------+      +------------------+      +------------------+
        |                                                  |
        v                                                  v
+------------------+                              +------------------+
|                  |                              |                  |
| Mental Health    |                              | User Sessions    |
| Analysis         |                              | (In-memory)      |
|                  |                              |                  |
+------------------+                              +------------------+
```

## Core Components

### 1. Mental Health Analysis (`utils/mental_health_utils.py`)

This module is responsible for:

- Analyzing user messages for signs of anxiety, depression, burnout, and suicidal ideation
- Using keyword matching and simple NLP techniques to evaluate the user's state
- Determining a concern level (low, moderate, high, critical) based on the analysis
- Identifying when immediate help is needed

Example mental health data structure:

```python
{
    'anxiety': 0.4,        # Score between 0-1
    'depression': 0.2,     # Score between 0-1
    'burnout': 0.3,        # Score between 0-1
    'suicidal': 0,         # Score between 0-1
    'immediate_help': False  # Boolean flag for crisis detection
}
```

### 2. Exercise Suggestions (`utils/exercise_suggestions.py`)

This module provides:

- Curated lists of mental health exercises categorized by type (breathing, mindfulness, journaling, physical)
- Logic to select appropriate exercises based on detected mental health issues
- Structured exercise data with names, descriptions, and benefits

Example exercise structure:

```python
{
    "name": "4-7-8 Breathing",
    "description": "Inhale for 4 seconds, hold for 7 seconds, exhale for 8 seconds. Repeat 4 times.",
    "benefits": "Helps reduce anxiety and promote sleep"
}
```

### 3. Resource Recommendations (`utils/mental_health_resources.py`)

This module contains:

- Categorized mental health resources (crisis, general, online, reading)
- Logic to provide appropriate resources based on concern level
- Structured resource data including contact information and website links

Example resource structure:

```python
{
    "name": "National Suicide Prevention Lifeline",
    "description": "24/7, free and confidential support",
    "contact": "1-800-273-8255",
    "website": "https://suicidepreventionlifeline.org/"
}
```

### 4. Response Generation (`utils/response_generator.py`)

This module:

- Creates prompts for the OpenAI API based on user input and mental health analysis
- Manages interaction with the OpenAI API
- Provides fallback responses if API calls fail
- Formats and returns empathetic responses

### 5. Web Application (`app.py`)

The main application file:

- Sets up Flask routes and session management
- Orchestrates the flow between components
- Manages conversation history
- Handles API endpoints for chat and reset functionality

## Data Flow

1. User sends a message through the web interface
2. The Flask backend receives the message via the `/api/chat` endpoint
3. The message is analyzed using `mental_health_utils` to detect potential issues
4. Based on the analysis, the concern level is determined
5. A response is generated using OpenAI (via `response_generator`)
6. Appropriate exercises and resources are selected based on the analysis
7. All components are combined into a response JSON object
8. The frontend displays the response, resources, and exercises to the user

## Session Management

User conversations are stored in-memory using a combination of Flask sessions and a server-side dictionary:

```python
# Dictionary to store conversations
conversations = {}

# Session identification
session['session_id'] = str(uuid.uuid4())
conversations[session['session_id']] = []
```

## Frontend Components

The frontend uses:

- HTML templates (`templates/index.html`)
- CSS for styling (`static/css/style.css`)
- JavaScript for interactive functionality (`static/js/script.js`)

Key frontend features:

- Real-time chat interface
- Dynamic resource and exercise display
- Responsive design for mobile and desktop use
- Animated message transitions for better UX

## Security Considerations

- User messages are not persistently stored beyond the session
- OpenAI API key is stored in an environment variable, not in the code
- Response generation is designed to avoid providing medical advice or diagnoses

## Future Enhancements

Potential areas for improvement:

1. Persistent storage for conversations using a database
2. More sophisticated NLP for better mental health analysis
3. User accounts for session continuity across devices
4. Integration with telehealth providers for professional support
5. Multilingual support for broader accessibility
