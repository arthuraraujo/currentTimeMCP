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
# Um dicionário que mapeia nomes de ferramentas às suas funções.
# Isso torna a API facilmente extensível com novas ferramentas.
AVAILABLE_TOOLS = {
    "getCurrentDateTime": get_current_date_time_tool
}

# --- Endpoint do Protocolo MCP ---

@app.route('/invoke', methods=['POST'])
def invoke_tool():
    """
    Endpoint genérico que invoca uma ferramenta com base no nome fornecido.
    """
    # Pega o corpo da requisição como JSON
    request_data = request.get_json()

    # Validação básica da requisição
    if not request_data or 'tool_name' not in request_data:
        return jsonify({
            "status": "error",
            "error_message": "Requisição inválida. 'tool_name' é obrigatório."
        }), 400

    tool_name = request_data['tool_name']

    # Verifica se a ferramenta solicitada existe
    if tool_name not in AVAILABLE_TOOLS:
        return jsonify({
            "tool_name": tool_name,
            "status": "error",
            "error_message": "Ferramenta não encontrada."
        }), 404

    try:
        # Pega a função da ferramenta no dicionário e a executa
        tool_function = AVAILABLE_TOOLS[tool_name]
        result = tool_function()

        # Monta a resposta de sucesso
        response = {
            "tool_name": tool_name,
            "status": "success",
            "result": result
        }
        return jsonify(response), 200

    except Exception as e:
        # Resposta genérica para qualquer erro durante a execução da ferramenta
        return jsonify({
            "tool_name": tool_name,
            "status": "error",
            "error_message": str(e)
        }), 500