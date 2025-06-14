"""
Mental Health Utils - Contains functions to identify potential signs of 
mental health issues from user input.
"""
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK data is downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Keywords related to different mental health states
ANXIETY_KEYWORDS = [
    'anxiety', 'anxious', 'worry', 'worried', 'panic', 'fear', 'scared', 
    'nervous', 'stress', 'stressed', 'overwhelming', 'tension', 'afraid', 
    'frightened', 'apprehensive', 'uneasy', 'restless'
]

DEPRESSION_KEYWORDS = [
    'depression', 'depressed', 'sad', 'unhappy', 'hopeless', 'worthless', 
    'empty', 'numb', 'tired', 'exhausted', 'despair', 'miserable', 'lonely', 
    'alone', 'grief', 'down', 'blue', 'upset', 'hurt', 'lost'
]

BURNOUT_KEYWORDS = [
    'burnout', 'exhausted', 'tired', 'fatigue', 'overwhelmed', 'drained', 
    'overworked', 'stressed', 'workload', 'pressure', 'deadlines', 'too much', 
    'can\'t cope', 'can\'t handle', 'breaking point', 'overload'
]

SUICIDAL_KEYWORDS = [
    'suicide', 'suicidal', 'kill myself', 'end it all', 'want to die', 
    'better off dead', 'no reason to live', 'can\'t go on', 'too much to bear'
]

IMMEDIATE_HELP_NEEDED_PHRASES = [
    'kill myself', 'end my life', 'want to die', 'planning to commit suicide',
    'going to kill myself', 'no reason to live', 'better off dead',
    'can\'t go on anymore', 'want to end it all', 'ready to die'
]

def detect_mental_health_issues(message):
    """
    Detect potential mental health issues from user input.
    Returns a dictionary with detected issues and confidence scores.
    """
    if not message:
        return {
            'anxiety': 0,
            'depression': 0,
            'burnout': 0,
            'suicidal': 0,
            'immediate_help': False
        }
        
    message = message.lower()
    
    # Use a simple word split instead of NLTK tokenization to avoid errors
    words = message.split()
    
    result = {
        'anxiety': 0,
        'depression': 0,
        'burnout': 0,
        'suicidal': 0,
        'immediate_help': False
    }
    
    # Check for immediate help needed phrases first
    for phrase in IMMEDIATE_HELP_NEEDED_PHRASES:
        if phrase in message:
            result['immediate_help'] = True
            result['suicidal'] = 1.0
            break
            
    # Calculate confidence scores
    word_count = len(words)
    if word_count == 0:
        return result
        
    for word in words:
        if word in ANXIETY_KEYWORDS:
            result['anxiety'] += 1/word_count
        if word in DEPRESSION_KEYWORDS:
            result['depression'] += 1/word_count
        if word in BURNOUT_KEYWORDS:
            result['burnout'] += 1/word_count
        if word in SUICIDAL_KEYWORDS:
            result['suicidal'] += 1/word_count
    
    # Normalize scores between 0 and 1
    for key in ['anxiety', 'depression', 'burnout', 'suicidal']:
        result[key] = min(result[key], 1.0)
        
    return result

def get_concern_level(mental_health_data):
    """
    Determine overall concern level based on detected mental health issues.
    Returns: low, moderate, high, or critical
    """
    if mental_health_data['immediate_help']:
        return "critical"
    
    max_score = max(
        mental_health_data['anxiety'],
        mental_health_data['depression'],
        mental_health_data['burnout'],
        mental_health_data['suicidal']
    )
    
    if mental_health_data['suicidal'] > 0.3:
        return "critical"
    elif max_score > 0.6:
        return "high"
    elif max_score > 0.3:
        return "moderate"
    else:
        return "low"
