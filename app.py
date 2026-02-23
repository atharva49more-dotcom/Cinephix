import os
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import json # Make sure this is at the very top of app.py

load_dotenv()
app = Flask(__name__)

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.json.get('preferences')
    
    prompt = f"""
    User Preferences: {user_input}
    You are a stylish, expert movie critic. Recommend 5 movies based on the user's personality or mood.
    Return the response strictly as a JSON list of objects with keys: "title", "year", "genre", and "reason".
    Example: [{{ "title": "Inception", "year": "2010", "genre": "Sci-Fi", "reason": "Because you love mind-bending plots." }}]
    """

    try:
        # NEW: Force the model to return pure JSON
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )
        
        # Look how clean this is now! No more markdown stripping.
        print(f"AI Response: {response.text}")
        movie_data = json.loads(response.text)
        
        return jsonify(movie_data)
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
