import os
from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

# Initialize Groq client. Insert your free API key here:
client = Groq(api_key='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')

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        user_request = request.form.get('user_request')
        
        try:
            # Sending request to Llama 3 via Groq API
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert in movie soundtracks and music. The user will describe "
                            "a movie and a scene. Your task is to identify the most likely songs playing "
                            "in that scene. "
                            "CRITICAL INSTRUCTIONS:\n"
                            "1. Respond strictly in English.\n"
                            "2. For every song you suggest, you MUST provide a clickable HTML hyperlink to YouTube search. "
                            "Use this exact format for links: <a href=\"https://www.youtube.com/results?search_query=Song+Name+Artist+Name\" target=\"_blank\">Listen on YouTube 🎥</a>\n"
                            "3. Replace 'Song+Name+Artist+Name' in the URL with the actual song title and artist, using plus signs (+) instead of spaces.\n"
                            "4. Keep your response concise, polite, and well-formatted."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_request,
                    }
                ],
                model="llama-3.1-8b-instant",
            )
            
            # Get the text response from AI
            result = chat_completion.choices[0].message.content
            
        except Exception as e:
            result = f"An error occurred while connecting to the AI: {e}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)