#!/usr/bin/env python3
from datetime import datetime
from zoneinfo import ZoneInfo
from mcp.server import FastMCP

mcp = FastMCP("DateTimeMCPServer", stateless_http=True)

@mcp.tool()
def get_current_datetime() -> str:
    sao_paulo_tz = ZoneInfo("America/Sao_Paulo")
    now_in_sao_paulo = datetime.now(sao_paulo_tz)
    return now_in_sao_paulo.isoformat()

if __name__ == "__main__":
    # Roda em uma porta interna, escutando apenas localmente
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)