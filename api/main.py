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
Intensity: {context.get('intensity', 'Unknown')}/10
Temperature: {context.get('temperature', 'Unknown')}C

REGRAS:
- Se "Last meal" ou "Last walk" indicar mais de 2 dias, trate como CAMPO DESATUALIZADO, nao como negligencia: o tutor provavelmente esqueceu de registrar. Ignore esse campo e diga que nao foi informado.
- Voce e uma ferramenta de leitura de comportamento, nao um servico de emergencia. Sugerir consulta veterinaria quando ha sinal fisico e adequado; acusar o tutor de maus-tratos, orientar denuncia a autoridades ou citar legislacao NAO e.
- Nunca contradiga os dados recebidos: se o tutor informou que o cao comeu ha 1h, nao afirme que esta em jejum.
- Mantenha o tom informativo. Este app nao substitui avaliacao veterinaria.

REGRAS:
- Se "Last meal" ou "Last walk" indicar mais de 2 dias, trate como CAMPO DESATUALIZADO, nao como negligencia: o tutor provavelmente esqueceu de registrar. Ignore esse campo e diga que nao foi informado.
- Voce e uma ferramenta de leitura de comportamento, nao um servico de emergencia. Sugerir consulta veterinaria quando ha sinal fisico e adequado; acusar o tutor de maus-tratos, orientar denuncia a autoridades ou citar legislacao NAO e.
- Nunca contradiga os dados recebidos: se o tutor informou que o cao comeu ha 1h, nao afirme que esta em jejum.
- Mantenha o tom informativo. Este app nao substitui avaliacao veterinaria.

Language: {context.get("language", "pt")}. Respond ONLY in the language specified: Brazilian Portuguese if language=pt, English if language=en. Use this exact JSON structure, no wrapper, no markdown:
{{
  "most_likely": {{
    "intention": "string describing main intention",
    "confidence": 75
  }},
  "top_10": [
    {{"intention": "string", "confidence": 75}},
    {{"intention": "string", "confidence": 60}}
  ],
  "dog_mood_index": {{
    "score": 65,
    "mood": "string describing mood",
    "energy": 70,
    "anxiety": 30,
    "stress": 25,
    "play_drive": 60,
    "walk_need": 80
  }},
  "recommended_action": "string with immediate recommendation",
  "alert_level": "low"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return jsonify({'analysis': response.content[0].text})

if __name__ == '__main__':
    app.run(debug=True)
