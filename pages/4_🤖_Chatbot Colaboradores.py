# railway_app.py
from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("OPENAI_API_KEY")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Chatbot Nutrisco</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
            background: #0e1117; 
            color: white; 
        }
        .header { 
            background: linear-gradient(90deg, #ea580c, #c2410c); 
            padding: 2rem; 
            border-radius: 20px; 
            text-align: center; 
            margin-bottom: 2rem; 
        }
        .chat-container { 
            margin-bottom: 100px; 
        }
        .message { 
            padding: 12px 16px; 
            margin: 10px 0; 
            border-radius: 12px; 
            max-width: 70%; 
        }
        .user-message { 
            background: #262730; 
            margin-left: auto; 
        }
        .bot-message { 
            background: #ea580c; 
            margin-right: auto; 
        }
        .input-container { 
            position: fixed; 
            bottom: 0; 
            left: 0; 
            right: 0; 
            background: #0e1117; 
            padding: 1rem; 
            border-top: 1px solid #333; 
        }
        input { 
            width: 100%; 
            padding: 12px; 
            border-radius: 25px; 
            border: 1px solid #444; 
            background: #1e1e1e; 
            color: white; 
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>💬 Chatbot Colaboradores</h1>
        <p>Nutrisco - Atención a Personas</p>
    </div>
    
    <div class="chat-container" id="chat">
        <div class="message bot-message">
            ¡Hola! Soy parte del equipo de Atención a Personas de Nutrisco. ¿En qué puedo ayudarte?
        </div>
    </div>
    
    <div class="input-container">
        <input type="text" id="userInput" placeholder="Escribe tu consulta aquí..." onkeypress="handleKeyPress(event)">
    </div>

    <script>
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (message === '') return;
            
            // Agregar mensaje usuario
            const chat = document.getElementById('chat');
            const userMsg = document.createElement('div');
            userMsg.className = 'message user-message';
            userMsg.textContent = message;
            chat.appendChild(userMsg);
            
            // Limpiar input
            input.value = '';
            
            // Obtener respuesta
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                const botMsg = document.createElement('div');
                botMsg.className = 'message bot-message';
                botMsg.textContent = data.response;
                chat.appendChild(botMsg);
                chat.scrollTop = chat.scrollHeight;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Eres un asistente de RR.HH. de Nutrisco."},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7
            }
        )
        bot_response = response.json()["choices"][0]["message"]["content"]
    except:
        bot_response = "⚠️ Contacta a belen.bastias@nutrisco.com"
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
