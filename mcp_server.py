#!/usr/bin/env python3
"""
Servidor MCP puro para retornar a data e hora.
"""
from datetime import datetime
from zoneinfo import ZoneInfo
from mcp.server import FastMCP

mcp = FastMCP("DateTimeMCPServer", stateless_http=True)

@mcp.tool()
def get_current_datetime() -> str:
    """
    Obtém a data e hora atuais no fuso horário de São Paulo (UTC-3).
    Retorna a data/hora em formato ISO 8601.
    """
    sao_paulo_tz = ZoneInfo("America/Sao_Paulo")
    now_in_sao_paulo = datetime.now(sao_paulo_tz)
    return now_in_sao_paulo.isoformat()

def main():
    """Ponto de entrada que inicia o servidor MCP."""
    print("Starting pure MCP Server, which will bind to 127.0.0.1:8000")
    # A biblioteca irá rodar em 127.0.0.1:8000 por padrão.
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()