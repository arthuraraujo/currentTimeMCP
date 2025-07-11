#!/usr/bin/env python3
"""
Servidor MCP puro para retornar a data e hora.
"""
from datetime import datetime
from zoneinfo import ZoneInfo
from mcp.server import FastMCP

# 1. Criar a instância do MCP.
mcp = FastMCP("DateTimeMCPServer", stateless_http=True)

# 2. Definir a ferramenta.
@mcp.tool()
def get_current_datetime() -> str:
    """
    Obtém a data e hora atuais no fuso horário de São Paulo (UTC-3).
    Retorna a data/hora em formato ISO 8601.
    """
    sao_paulo_tz = ZoneInfo("America/Sao_Paulo")
    now_in_sao_paulo = datetime.now(sao_paulo_tz)
    return now_in_sao_paulo.isoformat()

# 3. Criar a função main para iniciar o servidor com o método .run().
def main():
    """Ponto de entrada que inicia o servidor MCP."""
    print("Starting pure MCP Server on port 5000...")
    # O host 0.0.0.0 é crucial para funcionar no Docker.
    mcp.run(transport="streamable-http", host="0.0.0.0", port=5000)

# 4. Executar a função main se o script for chamado diretamente.
if __name__ == "__main__":
    main()