#!/usr/bin/env python3
"""
Simple MCP Server for Providing Current Datetime
"""

from datetime import datetime
from zoneinfo import ZoneInfo
from mcp.server import FastMCP
from fastapi.responses import JSONResponse

# Create a basic stateless MCP server
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


@mcp.get("/healthcheck")
def healthcheck():
    """
    Healthcheck endpoint to verify if the server is running.
    """
    return JSONResponse(content={"status": "ok"})


def main():
    """Main entry point for the MCP server"""
    # print("Starting DateTime MCP Server...")
    # print("Available tools: get_current_datetime")
    # print("Healthcheck endpoint available at GET /healthcheck")

    # Run with streamable HTTP transport
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()