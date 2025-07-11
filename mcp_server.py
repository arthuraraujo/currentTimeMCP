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
    print("Starting pure MCP Server...")
    print("Host and Port will be configured by HOST/PORT environment variables.")
    # A chamada correta, sem os argumentos não suportados.
    mcp.run(transport="streamable-http")

# 4. Executar a função main se o script for chamado diretamente.
if __name__ == "__main__":
    main()