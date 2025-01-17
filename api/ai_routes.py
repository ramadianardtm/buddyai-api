from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import os
import openai
from api.services import test_input

api_blueprint = Blueprint('api', __name__)

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API Key not found. Please check your .env file.")

openai.api_key = api_key

lang = 'en'
conversation_histories = {}
@api_blueprint.route('process-ai', methods=['POST'])
def process_ai():
    try: 
        data = request.json
        user_id = data.get('user_id')
        audio_command = data.get('command')
        ai_name = data.get('ai_name', 'Friday')
        
        if not user_id:
            return jsonify({"error": "User ID is required."}), 400
        
         # Initialize user conversation history if not present
        if user_id not in conversation_histories:
            conversation_histories[user_id] = [
                {"role": "system", "content": "You are an AI assistant named {ai_name}."}
            ]
        
        # Add user input to their conversation history
        conversation_histories[user_id].append({"role": "user", "content": audio_command})
        
        if ai_name in audio_command:
            
            # Make the OpenAI API call
            completion = openai.chat.completions.create(
                model="gpt-3.5-turbo", 
                messages=[{"role": "user", "content": audio_command}]
            )
            
            # Add AI response to the user's conversation history
            conversation_histories[user_id].append({"role": "assistant", "content": response_text})
            response_text = completion.choices[0].message.content
            
            return jsonify({"response": response_text}), 200
        
        return jsonify({"response": f"Command not recognized or '{ai_name}' not mentioned."}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_blueprint.route('/test', methods=['POST'])
def test():
    print("Received a request at /api/process")
    # Extract input from the request
    data = request.json
    user_input = data.get('input', '')

    # Example response logic
    response = test_input(user_input)

    # Return the response as JSON
    return jsonify({'response': response})