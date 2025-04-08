import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)


ENDPOINT_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=" + API_KEY

def generate_text(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(ENDPOINT_URL, headers=headers, json=data)
    response_json = response.json()

    # Print the response for debugging
    print(response_json)

    # Check if 'contents' and 'parts' are in the response
    if 'candidates' in response_json and 'content' in response_json['candidates'][0]:
        generated_text = response_json['candidates'][0]['content']['parts'][0].get('text', 'No text generated')
    else:
        generated_text = 'Error: Invalid response structure'
    
    return generated_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    generated_text = generate_text(prompt)
    return render_template('index.html', generated_text=generated_text)

if __name__ == '__main__':
    port = int(os.environ.get('PORT',80))
    app.run(host='0.0.0.0', port=port, debug=True)
