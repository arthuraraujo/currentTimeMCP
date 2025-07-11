#!/usr/bin/env python3
"""
Simple MCP Server for Providing Current Datetime, composed with FastAPI
"""

from datetime import datetime
from zoneinfo import ZoneInfo
from mcp.server import FastMCP
from fastapi import FastAPI # Import FastAPI

# ======================================================================
# 1. Create a standard FastAPI app instance. This will be our main app.
# ======================================================================
app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    """
    Healthcheck endpoint to verify if the server is running.
    """
    return {"status": "ok"}

# ======================================================================
# 2. Create and configure the MCP server instance as before.
# ======================================================================
mcp = FastMCP("DateTimeMCPServer", stateless_http=True)

@mcp.tool()
def get_current_datetime() -> str:
    """
    Gets the current date and time in São Paulo timezone (UTC-3).

    Returns:
        str: The current date and time in ISO 8601 format.
    """
    sao_paulo_tz = ZoneInfo("America/Sao_Paulo")
    now_in_sao_paulo = datetime.now(sao_paulo_tz)
    return now_in_sao_paulo.isoformat()

# ======================================================================
# 3. Mount the MCP server onto our main FastAPI app.
#    All MCP traffic will now be handled by the 'mcp' object.
# ======================================================================
app.mount("/", mcp)

# NOTE: We no longer need the main() function from the original script,
# as uvicorn will now run the 'app' object directly.