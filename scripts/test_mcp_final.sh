#!/usr/bin/env bash

set -euo pipefail

# Keep the historical entry point for contributors and the release workflow,
# while delegating protocol framing, lifecycle handling, and assertions to the
# supported Python MCP client integration suite. This is portable across macOS
# and Linux and does not require GNU `timeout` or parse JSON with grep.
exec uv run --frozen pytest --no-cov -v tests/test_mcp_integration.py
