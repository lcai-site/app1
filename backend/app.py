import os
import base64
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

# --- Configuração do Logging ---
# Configura o logging para escrever em um arquivo chamado app.log
logging.basicConfig(
    filename='backend/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Inicializa o aplicativo Flask
app = Flask(__name__, static_folder='../frontend')

# Habilita o CORS
CORS(app)

@app.route('/api/generate', methods=['POST'])
def generate_image():
    """
    Endpoint para gerar uma imagem a partir de um prompt usando a API do Google Gemini.
    """
    data = request.get_json()
    prompt = data.get('prompt')
    api_key = data.get('api_key')

    # Validação de Entrada
    if not prompt or not api_key:
        logging.warning("Requisição recebida sem API Key ou Prompt.")
        return jsonify({"error": "API Key e Prompt são obrigatórios."}), 400

    logging.info(f"Recebida requisição com prompt: '{prompt}'")

    try:
        # Configura a API Key do Google
        genai.configure(api_key=api_key)

        # Seleciona o modelo de geração de imagem
        model = genai.GenerativeModel('gemini-2.5-flash-image-preview')

        # Gera o conteúdo (a imagem)
        logging.info("Enviando requisição para a API do Google Gemini...")
        response = model.generate_content(prompt)
        logging.info("Resposta recebida da API.")

        # Extrai os dados da primeira imagem gerada.
        image_data = response.candidates[0].content.parts[0].inline_data.data

        # Codifica os dados da imagem em Base64.
        base64_image_data = base64.b64encode(image_data).decode('utf-8')

        # Cria um Data URI para a imagem.
        image_data_uri = f"data:image/png;base64,{base64_image_data}"

        logging.info("Imagem processada e Data URI criado com sucesso.")
        return jsonify({"image_url": image_data_uri})

    except Exception as e:
        # Usa o logger para registrar o traceback completo da exceção
        logging.exception("Ocorreu um erro ao chamar a API do Gemini.")

        error_message = str(e)
        if "API_KEY_INVALID" in error_message:
            return jsonify({"error": "A API Key fornecida é inválida ou expirou."}), 401
        if "content has been blocked" in error_message:
            return jsonify({"error": "A geração de imagem foi bloqueada pela política de segurança. Tente um prompt diferente."}), 400
        if "ResourceExhausted" in error_message:
             return jsonify({"error": "A cota da sua API Key foi excedida. Verifique seu plano e detalhes de faturamento no painel do Google AI."}), 429

        return jsonify({"error": "Falha ao gerar a imagem. Verifique o console do servidor para mais detalhes."}), 500

# Rota para servir o frontend (index.html)
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Rota para servir outros arquivos estáticos (CSS, JS)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    logging.info("Iniciando o servidor Flask.")
    # Executa o aplicativo na porta 5001 (debug=False)
    app.run(host='0.0.0.0', port=5001, debug=False)