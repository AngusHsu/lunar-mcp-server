# Dockerfile for Smithery deployment
FROM python:3.11-slim

# Install uv for faster package management
RUN pip install --no-cache-dir uv

# Install lunar-mcp-server from PyPI
RUN uv pip install --system lunar-mcp-server

# Set the entry point
ENTRYPOINT ["lunar-mcp-server"]
