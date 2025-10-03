FROM python:3.11-slim

# Install uv for faster package installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install the package from PyPI
RUN uv pip install --system lunar-mcp-server

# Run the MCP server
CMD ["python", "-m", "lunar_mcp_server.server"]
