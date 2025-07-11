#!/usr/bin/env python3
"""
MCP Server com suporte a descoberta e registro para compatibilidade com clientes complexos.
"""
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI
from mcp.server import FastMCP
from fastapi.responses import JSONResponse

# 1. Criar a aplicação FastAPI principal. Ela será nosso ponto de entrada único.
app = FastAPI(
    title="DateTime MCP Server",
    description="Um servidor MCP que retorna a data/hora e suporta descoberta de ferramentas."
)

# 2. Criar a instância do MCP, mas sem rodá-la diretamente.
#    Ela servirá como um "motor" para as nossas ferramentas.
mcp = FastMCP("DateTimeMCPServer", stateless_http=True)

# 3. Definir a nossa ferramenta no motor MCP, como antes.
@mcp.tool()
def get_current_datetime() -> str:
    """
    Obtém a data e hora atuais no fuso horário de São Paulo (UTC-3).
    Retorna a data/hora em formato ISO 8601.
    """
    sao_paulo_tz = ZoneInfo("America/Sao_Paulo")
    now_in_sao_paulo = datetime.now(sao_paulo_tz)
    return now_in_sao_paulo.isoformat()

# ==============================================================================
# 4. Implementar os Endpoints de Descoberta e Registro (Stubs)
#    Esta é a parte crucial para "enganar" o cliente claude.ai.
# ==============================================================================

@app.post("/register", status_code=200)
def register_client():
    """
    Endpoint FALSO de registro. Apenas retorna um sucesso para o cliente
    prosseguir para o próximo passo.
    """
    # Retornamos um ID de cliente falso. O importante é a resposta de sucesso.
    return {"client_id": "static-client-for-claude-ai", "status": "registered"}

@app.get("/.well-known/{full_path:path}")
def handle_well_known(full_path: str):
    """
    Endpoint FALSO para descoberta de segurança. Informa ao cliente que
    nenhuma autenticação complexa é necessária.
    """
    # Apenas dizemos que não há métodos de autenticação especiais.
    return {"authentication_methods": ["none"]}

@app.get("/", status_code=200)
def discover_tools():
    """
    Endpoint de Descoberta de Ferramentas. Descreve as ferramentas que
    nosso servidor oferece no formato que o cliente espera (JSON Schema).
    """
    return {
        "tools": [
            {
                "name": "get_current_datetime",
                "description": "Obtém a data e hora atuais no fuso horário de São Paulo (UTC-3). Retorna a data/hora em formato ISO 8601.",
                "input_schema": {
                    "type": "object",
                    "properties": {}, # Sem parâmetros de entrada
                },
                "output_schema": {
                    "type": "string",
                    "format": "date-time"
                }
            }
        ]
    }

# 5. Integrar as rotas de execução de ferramentas do MCP na nossa app principal.
#    Isso faz com que as chamadas de ferramenta (ex: POST para /) sejam
#    direcionadas para o motor do MCP.
app.include_router(mcp.router)

# 6. Adicionar o endpoint de healthcheck para monitoramento.
@app.get("/healthcheck")
def healthcheck():
    """Endpoint de Healthcheck para verificar se o serviço está no ar."""
    return {"status": "ok"}