# app.py

from flask import Flask, jsonify, request
from datetime import datetime
from zoneinfo import ZoneInfo

# Cria a instância da aplicação Flask
app = Flask(__name__)

# --- Definição das Ferramentas ---

def get_current_date_time_tool():
    """
    Ferramenta que retorna a data e hora atuais no fuso horário de São Paulo.
    """
    sao_paulo_tz = ZoneInfo("America/Sao_Paulo")
    now_in_sao_paulo = datetime.now(sao_paulo_tz)
    return {
        'datetime': now_in_sao_paulo.isoformat(),
        'timezone': str(sao_paulo_tz)
    }

# --- Registro de Ferramentas Disponíveis ---
AVAILABLE_TOOLS = {
    "getCurrentDateTime": get_current_date_time_tool
}

# --- Endpoint de Health Check (Boa prática, vamos manter) ---
@app.route('/healthcheck', methods=['GET'])
def health_check():
    """
    Retorna um status 200 OK se a aplicação estiver rodando.
    """
    return jsonify({
        "status": "healthy",
        "timestamp_utc": datetime.utcnow().isoformat() + "Z"
    })

# --- NOVA ROTA PARA O CONECTOR DO CLAUDE ---
@app.route('/getCurrentDateTime', methods=['GET'])
def get_current_date_time_endpoint():
    """
    Endpoint dedicado para a ferramenta getCurrentDateTime.
    Responde a GET, que é o que o conector simples do Claude espera.
    """
    sao_paulo_tz = ZoneInfo("America/Sao_Paulo")
    now_in_sao_paulo = datetime.now(sao_paulo_tz)
    
    # Retorna diretamente o resultado que o LLM precisa
    return jsonify({
        'datetime': now_in_sao_paulo.isoformat(),
        'timezone': str(sao_paulo_tz)
    })

# --- Endpoint do Protocolo MCP ---
@app.route('/invoke', methods=['POST'])
def invoke_tool():
    """
    Endpoint genérico que invoca uma ferramenta com base no nome fornecido.
    """
    request_data = request.get_json()

    if not request_data or 'tool_name' not in request_data:
        return jsonify({
            "status": "error",
            "error_message": "Requisição inválida. 'tool_name' é obrigatório."
        }), 400

    tool_name = request_data['tool_name']

    if tool_name not in AVAILABLE_TOOLS:
        return jsonify({
            "tool_name": tool_name,
            "status": "error",
            "error_message": "Ferramenta não encontrada."
        }), 404

    try:
        tool_function = AVAILABLE_TOOLS[tool_name]
        result = tool_function()

        response = {
            "tool_name": tool_name,
            "status": "success",
            "result": result
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "tool_name": tool_name,
            "status": "error",
            "error_message": str(e)
        }), 500