# Running Lunar MCP Server in STDIO Mode

The Lunar MCP Server supports running in STDIO mode for integration with MCP clients. This mode allows the server to communicate via standard input/output streams.

## Quick Start

### Using uv (recommended)

```bash
uv run lunar-mcp-server
```

Or using the module directly:

```bash
uv run python -m lunar_mcp_server.server
```

### Using the installed script

If you've installed the package globally:

```bash
lunar-mcp-server
```

### Direct execution (not recommended)

```bash
python src/lunar_mcp_server/server.py
```

## How it works

The server runs in STDIO mode by default, which means:

- It reads MCP protocol messages from stdin
- It writes responses to stdout
- It uses stderr for logging (set logging level via `PYTHONPATH` or logging configuration)

## Integration with MCP Clients

To use this server with an MCP client, configure it in your client's settings. For example, with Claude Desktop:

Using uv (recommended):
```json
{
  "mcpServers": {
    "lunar-calendar": {
      "command": "uv",
      "args": ["run", "lunar-mcp-server"],
      "cwd": "/path/to/lunar-mcp-server"
    }
  }
}
```

Or using the globally installed script:
```json
{
  "mcpServers": {
    "lunar-calendar": {
      "command": "lunar-mcp-server",
      "args": []
    }
  }
}
```

## Available Tools

The server provides comprehensive lunar calendar functionality including:

- **Auspicious Date Checking**: Check if dates are favorable for specific activities
- **Good Date Finding**: Find optimal dates in a range for activities
- **Daily Fortune**: Get daily fortune and luck information
- **Zodiac Compatibility**: Check compatibility between dates based on zodiac
- **Festival Information**: Get festival data for dates, years, or specific festivals
- **Moon Phase Calculations**: Get detailed moon phase information
- **Calendar Conversions**: Convert between solar and lunar calendar systems
- **Zodiac Information**: Get zodiac animal/sign details

## Technical Details

- **Entry Point**: `lunar_mcp_server.server:main` (defined in pyproject.toml)
- **Default Transport**: STDIO (standard input/output)
- **Async Runtime**: Uses asyncio for handling concurrent operations
- **Protocol**: Implements MCP (Model Context Protocol) specification

## Logging

The server uses Python's logging module. To see debug information:

```bash
PYTHONPATH=. python -c "import logging; logging.basicConfig(level=logging.DEBUG); from lunar_mcp_server.server import main; main()"
```

## Dependencies

All required dependencies are automatically installed when you install the package. Key dependencies include:

- `mcp>=1.0.0` - MCP protocol implementation
- `skyfield>=1.48` - Astronomical calculations
- `lunardate>=0.2.2` - Lunar calendar conversions
- `chinese-calendar>=1.9.0` - Chinese calendar support
- Plus various other calendar and astronomical libraries

## Development

For development purposes, use uv to run the server with proper dependency management:

```bash
cd /path/to/lunar-mcp-server
uv run lunar-mcp-server
```

Or for debugging with specific logging:

```bash
uv run python -c "import logging; logging.basicConfig(level=logging.DEBUG); from lunar_mcp_server.server import main; main()"
```

This will start the server in STDIO mode, ready to receive MCP protocol messages.