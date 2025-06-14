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
        "Hi there! I'm here to **support you**. How are you doing?",
        "Welcome! How can I help support your mental wellbeing today?"
    ],
    "anxiety": [
        "It sounds like you might be experiencing some anxiety.\n\n**Remember to take deep breaths**. Breathing exercises can help ground you in the present moment.",
        "When we feel anxious, our breathing often becomes shallow.\n\nTry taking a few deep breaths with me. Inhale slowly for 4 counts, hold for 2, and exhale for 6. This can help activate your parasympathetic nervous system.",
        "I understand anxiety can be overwhelming. Let's try to ground ourselves in the present moment.\n\nOne technique you might find helpful is the **5-4-3-2-1 exercise**:\n\n- Notice 5 things you can see\n- Notice 4 things you can touch\n- Notice 3 things you can hear\n- Notice 2 things you can smell\n- Notice 1 thing you can taste"
    ],
    "depression": [
        "I'm sorry you're feeling this way. **Remember that you're not alone** in this.\n\nDepression can make even simple tasks feel overwhelming. Be gentle with yourself and acknowledge the small wins.",
        "Depression can make everything feel heavy.\n\n**Small steps forward are still progress**. What's one tiny thing you could do today that might bring even a moment of relief?",
        "It takes courage to share how you're feeling.\n\nI'm here to listen without judgment. Depression is not your fault, and reaching out is a sign of strength, not weakness."
    ],
    "burnout": [
        "Feeling burnt out is a sign that you've been pushing yourself hard. **It's okay to rest**.\n\nBurnout isn't just tiredness - it's your body and mind telling you that something needs to change. What small boundaries could you set to protect your energy?",
        "Burnout can be draining. **What's one small thing you could do for yourself today**?\n\nSometimes even 5 minutes of intentional rest can help begin the recovery process.",
        "I hear that you're feeling exhausted. **Remember to be kind to yourself** during this time.\n\nBurnout often happens to people who care deeply and try hard. Your worth isn't tied to your productivity."
    ],
    "critical": [
        "It sounds like you are going through a lot right now. **Please know that there's support available**.\n\nConsider reaching out to a crisis hotline or mental health professional. The **988 Suicide & Crisis Lifeline** is available 24/7 and can be reached by dialing or texting 988.",
        "I'm concerned about what you're saying. **If you're in crisis, please reach out for immediate help**.\n\nThere are people who want to support you. The **Crisis Text Line** can be reached by texting HOME to 741741 anytime.",
        "Your safety is important. **If you feel like you might hurt yourself, please contact a crisis support service now**.\n\nYou deserve support, and trained professionals are available 24/7 to talk with you about what you're experiencing."
    ],
    "general": [
        "Thanks for sharing that with me.\n\nI appreciate your openness. How else can I support you today?",
        "I'm here to listen. **Tell me more about what's on your mind**.\n\nSharing your thoughts and feelings can sometimes help make them feel less overwhelming.",
        "It sounds like you're going through a lot. **How can I best support you right now**?\n\nSometimes just having someone to listen can make a difference."
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
        "You are an empathetic mental health support chatbot with expertise in emotional support. "
        "Follow these guidelines:\n\n"
        "1. TONE & STYLE:\n"
        "- Use a warm, compassionate, and understanding tone\n"
        "- Validate emotions and experiences\n"
        "- Write responses in 3-4 sentence and exceed if there is a need \n"
        "- Use phrases like 'I understand', 'It's completely normal to feel', 'You're not alone'\n\n"
        "2. RESPONSE STRUCTURE:\n"
        "- If user is facing a problem, first notify him the issue he is facing"
        "- Start with emotional acknowledgment\n"
        "- Provide gentle guidance and support\n"
        "- Include one practical suggestion or coping strategy\n"
        "- End with a supportive statement\n\n"
        "3. RESOURCES:\n"
        "-Provide resources only if the user asks for resources"
        "- Include 1-2 relevant online resources or websites\n"
        "- Suggest appropriate self-help tools or apps\n"
        "- Mention credible mental health organizations\n\n"
        "4. FORMATTING & READABILITY:\n"
        "- Use proper Markdown formatting in your responses\n"
        "- Split text into paragraphs (2-3 sentences per paragraph)\n"
        "- Use **bold** for emphasis on important words or phrases\n"
        "- Use bullet points for lists when appropriate\n"
        "- Include a clear visual structure with spaces between paragraphs\n\n"
        "5. IMPORTANT RULES:\n"
        "- NEVER diagnose or provide medical advice\n"
        "- Keep responses conversational yet professional\n"
        "- Always prioritize user safety\n"
        "- Encourage professional help when appropriate\n\n"
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
