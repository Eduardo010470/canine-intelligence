from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'app': 'Canine Intelligence'})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    context = data.get('context', {})
    
    prompt = f"""You are Canine Intelligence, an AI that interprets dog behavior.

Dog: {context.get('dog_name', 'Unknown')} ({context.get('breed', 'Unknown breed')})
Time: {context.get('time', datetime.now().strftime('%H:%M'))}
Last meal: {context.get('last_meal', 'Unknown')}
Last walk: {context.get('last_walk', 'Unknown')}
Bark type: {context.get('bark_type', 'Unknown')}
Duration: {context.get('duration', 'Unknown')} seconds
Intensity: {context.get('intensity', 'Unknown')}/10
Location: {context.get('location', 'Unknown')}
Temperature: {context.get('temperature', 'Unknown')}°C

Based on all signals, provide:
1. Most likely intention (with % confidence)
2. Top 10 possibilities (top_3_possibilities array with all 10)
3. Dog Mood Index (DMI): score 0-100, energy, anxiety, stress
4. Recommended action for owner
5. Alert level: none/low/medium/high

Respond in JSON format only."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return jsonify({'analysis': response.content[0].text})

if __name__ == '__main__':
    app.run(debug=True)
