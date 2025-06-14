"""
Mental Health Chatbot - Main application
"""

from flask import Flask, render_template, request, jsonify, session
import os
import uuid
import traceback
from datetime import datetime
from dotenv import load_dotenv

# Import utility modules
from utils.mental_health_utils import detect_mental_health_issues, get_concern_level
from utils.exercise_suggestions import get_exercise_for_state
from utils.mental_health_resources import get_resources_by_concern
from utils.response_generator import generate_response

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(16))

# Dictionary to store conversations
conversations = {}

# Error handler for all routes
@app.errorhandler(Exception)
def handle_exception(e):
    """Convert all unhandled exceptions to JSON responses"""
    # Prepare error response
    error_response = {
        'error': str(e)[:200],
        'message': "An unexpected error occurred. Please try again.",
        'traceback': traceback.format_exc()[:500] if os.getenv('DEBUG') == 'True' else None
    }
    return jsonify(error_response), 500

@app.route('/')
def home():
    # Generate a session ID if one doesn't exist
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        conversations[session['session_id']] = []
    
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Ensure we're dealing with JSON 
        if not request.is_json:
            return jsonify({
                'error': 'Request must be JSON',
                'message': "I'm sorry, there was an error processing your request."
            }), 400
            
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = session.get('session_id')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        if not session_id or session_id not in conversations:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
            conversations[session_id] = []
        
        # Add user message to conversation history
        conversations[session_id].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        try:
            # Analyze mental health issues in the message
            mental_health_data = detect_mental_health_issues(user_message)
            concern_level = get_concern_level(mental_health_data)
            
            # Generate a response based on the analysis
            bot_response = generate_response(
                user_message, 
                mental_health_data,
                conversations[session_id]
            )
            
            # Determine if we should add an exercise suggestion
            should_add_exercise = any(score > 0.3 for score in [
                mental_health_data['anxiety'],
                mental_health_data['depression'],
                mental_health_data['burnout']
            ])
            
            exercise_suggestion = None
            if should_add_exercise:
                # Find the most prominent issue
                issues = {
                    'anxiety': mental_health_data['anxiety'],
                    'depression': mental_health_data['depression'],
                    'burnout': mental_health_data['burnout']
                }
                prominent_issue = max(issues, key=issues.get)
                exercise_suggestion = get_exercise_for_state(prominent_issue)
            
            # Get appropriate resources based on concern level
            resources = get_resources_by_concern(concern_level)
            
            # Add bot response to conversation history
            conversations[session_id].append({
                'role': 'assistant',
                'content': bot_response,
                'timestamp': datetime.now().isoformat()
            })
            
            # Ensure all response components are properly structured
            response = {
                'status': 'success',
                'message': bot_response,
                'exercise': exercise_suggestion if exercise_suggestion else None,
                'resources': resources if concern_level in ['moderate', 'high', 'critical'] else None,
                'concern_level': concern_level
            }
            
            return jsonify(response), 200
            
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                'error': 'Processing error',
                'message': "I apologize, but I encountered an error while processing your message. Please try again.",
                'resources': None,
                'exercise': None
            }), 500
            
    except Exception as e:
        print(f"Error in /api/chat: {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            'error': str(e)[:200],
            'message': "I'm sorry, I encountered an error processing your message. Please try again.",
            'resources': None,
            'exercise': None
        }), 500
    
@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    try:
        session_id = session.get('session_id')
        if session_id and session_id in conversations:
            conversations[session_id] = []
        
        return jsonify({
            'message': 'Conversation reset successfully',
            'success': True
        })
    except Exception as e:
        print(f"Error in /api/reset: {str(e)}")
        print(traceback.format_exc())  # This will print the full stacktrace to help with debugging
        return jsonify({'error': str(e), 'message': "Error resetting conversation."}), 500

if __name__ == '__main__':
    # Ensure directories exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')
    
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
