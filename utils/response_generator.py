"""
Response Generator - Uses Google Generative AI API to generate empathetic responses
"""

import os
import google.generativeai as genai
import random
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

# Set up Google API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("WARNING: GOOGLE_API_KEY not found in .env file!")
else:
    genai.configure(api_key=api_key)
    # List available models to debug
    try:
        available_models = []
        for model in genai.list_models():
            if "generateContent" in model.supported_generation_methods:
                available_models.append(model.name)
                print(f"Available model: {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

# Set the model name to use - this one has been confirmed working
MODEL_NAME = "gemini-1.5-flash"  # Using the tested and working model

# Backup responses in case API fails
FALLBACK_RESPONSES = {
    "greeting": [
        "Hello! How are you feeling today?",
        "Hi there! I'm here to support you. How are you doing?",
        "Welcome! How can I help support your mental wellbeing today?"
    ],
    "anxiety": [
        "It sounds like you might be experiencing some anxiety. Remember to take deep breaths.",
        "When we feel anxious, our breathing often becomes shallow. Try taking a few deep breaths with me.",
        "I understand anxiety can be overwhelming. Let's try to ground ourselves in the present moment."
    ],
    "depression": [
        "I'm sorry you're feeling this way. Remember that you're not alone in this.",
        "Depression can make everything feel heavy. Small steps forward are still progress.",
        "It takes courage to share how you're feeling. I'm here to listen without judgment."
    ],
    "burnout": [
        "Feeling burnt out is a sign that you've been pushing yourself hard. It's okay to rest.",
        "Burnout can be draining. What's one small thing you could do for yourself today?",
        "I hear that you're feeling exhausted. Remember to be kind to yourself during this time."
    ],
    "critical": [
        "It sounds like you are going through a lot right now. Please know that there's support available. Consider reaching out to a crisis hotline or mental health professional.",
        "I'm concerned about what you're saying. If you're in crisis, please reach out for immediate help. There are people who want to support you.",
        "Your safety is important. If you feel like you might hurt yourself, please contact a crisis support service now."
    ],
    "general": [
        "Thanks for sharing that with me.",
        "I'm here to listen. Tell me more about what's on your mind.",
        "It sounds like you're going through a lot. How can I best support you right now?"
    ]
}

def create_prompt(user_message, mental_health_data):
    """
    Create a system prompt based on mental health data
    """
    # Determine the most prominent issue
    issues = {
        'anxiety': mental_health_data['anxiety'],
        'depression': mental_health_data['depression'],
        'burnout': mental_health_data['burnout']
    }
    prominent_issue = max(issues, key=issues.get)
    
    # Build the system prompt
    system_prompt = (
        "You are an empathetic mental health support chatbot. You provide supportive, "
        "non-judgmental responses that acknowledge emotions. "
        "You NEVER diagnose or provide medical advice. "
        "Keep responses brief and conversational (3-4 sentences maximum). "
        "Be gentle and encouraging. Use a warm, supportive tone. "
    )
    
    # Add information about detected issues
    if mental_health_data['immediate_help']:
        system_prompt += (
            "The user may be in crisis and need immediate help. "
            "Express concern, validate their feelings, and strongly encourage "
            "them to contact a crisis service immediately. Be direct but compassionate."
        )
    elif issues[prominent_issue] > 0.3:
        system_prompt += f"The user may be experiencing {prominent_issue}. "
        if prominent_issue == 'anxiety':
            system_prompt += "Focus on grounding techniques and present moment awareness."
        elif prominent_issue == 'depression':
            system_prompt += "Offer gentle encouragement and validate their feelings."
        elif prominent_issue == 'burnout':
            system_prompt += "Emphasize the importance of rest and boundaries."
            
    return system_prompt

def generate_response(user_message, mental_health_data, conversation_history=None):
    """
    Generate a response using the Google Generative AI API with improved error handling
    """
    if conversation_history is None:
        conversation_history = []
    
    # Default to using fallback responses
    use_fallback = False
        
    try:
        # Check if API key is available
        if not os.getenv("GOOGLE_API_KEY"):
            print("No Google API key found - using fallback response")
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
            
        # Create the prompt incorporating the mental health analysis
        system_prompt = create_prompt(user_message, mental_health_data)
        
        # Configure the model with simplified generation parameters
        generation_config = {
            "temperature": 0.7,
            "max_output_tokens": 800,
        }

        try:
            # Initialize the model with recommended model
            model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                generation_config=generation_config
            )
            
            # Create prompt with system instructions and user message
            prompt = f"{system_prompt}\n\nUser: {user_message}\n\nResponse:"
            
            # Generate the response
            response = model.generate_content(prompt)
            
            # Return the text content
            return response.text
        
        except Exception as model_error:
            print(f"Error with {MODEL_NAME}: {model_error}")
            print(traceback.format_exc())
            use_fallback = True
            raise model_error
            
    except Exception as e:
        print(f"Error generating response with Google Gemini API: {e}")
        print(traceback.format_exc())
        use_fallback = True
    
    # Use fallback responses if API fails
    if use_fallback:
        if mental_health_data['immediate_help']:
            return random.choice(FALLBACK_RESPONSES["critical"])
        elif mental_health_data['anxiety'] > 0.3:
            return random.choice(FALLBACK_RESPONSES["anxiety"])
        elif mental_health_data['depression'] > 0.3:
            return random.choice(FALLBACK_RESPONSES["depression"])  
        elif mental_health_data['burnout'] > 0.3:
            return random.choice(FALLBACK_RESPONSES["burnout"])
        else:
            return random.choice(FALLBACK_RESPONSES["general"])
