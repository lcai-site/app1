import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

# Inicializa o aplicativo Flask
app = Flask(__name__, static_folder='../frontend')

# Habilita o CORS para permitir que o frontend se comunique com o backend
# Em um ambiente de produção, restrinja a origem para o seu domínio de frontend
CORS(app)

@app.route('/api/generate', methods=['POST'])
def generate_image():
    """
    Endpoint para gerar uma imagem a partir de um prompt.
    Recebe um JSON com 'prompt' e 'api_key'.
    """
    data = request.get_json()
    prompt = data.get('prompt')
    api_key = data.get('api_key')

    # --- Validação de Entrada ---
    if not prompt or not api_key:
        return jsonify({"error": "API Key e Prompt são obrigatórios."}), 400

    print(f"Received request: API Key='{api_key[:4]}...', Prompt='{prompt}'")

    # --- LÓGICA DE PLACEHOLDER ---
    # Aqui é onde a chamada para a API de IA (Google, Meta, etc.) seria feita.
    # Por enquanto, vamos simular o comportamento.
    # Vamos retornar uma imagem de placeholder de um serviço como o placehold.co.

    # Simulação de sucesso
    try:
        # Em um caso real, a chamada seria algo como:
        # headers = {"Authorization": f"Bearer {api_key}"}
        # payload = {"prompt": prompt, "model": "latest-model"}
        # response = requests.post("https://api.actual-ai.com/v1/images/generations", headers=headers, json=payload)
        # response.raise_for_status() # Lança um erro para respostas 4xx/5xx
        # image_url = response.json()['data'][0]['url']

        print("Simulando chamada de API... Sucesso!")
        # Usando um placeholder que gera uma imagem com base no texto do prompt
        image_url = f"https://placehold.co/512x512/6a11cb/ffffff?text=Gerado:\\n{prompt[:30].replace(' ', '+')}"

        return jsonify({"image_url": image_url})

    except requests.exceptions.RequestException as e:
        # Simulação de falha na API
        print(f"Simulando erro de API: {e}")
        return jsonify({"error": "Falha ao se comunicar com a API de geração de imagem."}), 500
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return jsonify({"error": "Ocorreu um erro interno no servidor."}), 500

# Rota para servir o frontend (index.html)
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Rota para servir outros arquivos estáticos (CSS, JS)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Executa o aplicativo na porta 5001 em modo de depuração
    app.run(host='0.0.0.0', port=5001, debug=True)