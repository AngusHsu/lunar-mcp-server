<div align="center">

# 🌙 Lunar Calendar MCP Server

### Traditional Chinese Lunar Calendar for AI Applications

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-2024--11--05-green.svg)](https://modelcontextprotocol.io)
[![Tests](https://img.shields.io/badge/tests-18%2F18%20passing-brightgreen.svg)](./scripts/test_mcp_final.sh)

**18 Tools** | **Chinese Zodiac** | **Five Elements** | **Moon Phases** | **Festivals** | **Auspicious Dates**

---

</div>

## 📖 Overview

A comprehensive Model Context Protocol (MCP) server providing traditional Chinese lunar calendar information, auspicious date checking, and festival data based on Chinese cultural traditions.

Perfect for integrating ancient Chinese wisdom into modern AI applications through the Model Context Protocol.

## ✨ Features

- 🎯 **Auspicious Date Analysis** - Check favorable dates, find good dates, daily fortune, zodiac compatibility
- 🎊 **Festival Information** - Chinese festivals, next festival, festival details, annual calendars
- 🌙 **Moon Phase Analysis** - Accurate moon phases, location-aware, activity influence, monthly calendars
- 📅 **Calendar Conversions** - Solar-lunar conversion, zodiac information, cultural integration
- ⚡ **Advanced Tools** - Batch checking, date comparison, lucky hours

**[📚 Complete Features List →](./docs/tools-reference.md)**

## 🚀 Quick Start

### Installation

```bash
# Using pip
pip install lunar-mcp-server

# Using uvx (no installation needed)
uvx lunar-mcp-server

# From source
git clone https://github.com/AngusHsu/lunar-mcp-server.git
cd lunar-mcp-server
uv sync
```

### Running the Server

```bash
# Using uv
uv run lunar-mcp-server

# Using uvx
uvx lunar-mcp-server

# After pip install
lunar-mcp-server
```

### Claude Desktop Integration

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "lunar-calendar": {
      "command": "uvx",
      "args": ["lunar-mcp-server"]
    }
  }
}
```

**[📖 Detailed Usage Guide →](./docs/usage-examples.md)**

## 🛠️ Available Tools

### 🎯 Auspicious Date Tools (4)
- `check_auspicious_date` - Check if date is favorable
- `find_good_dates` - Find optimal dates
- `get_daily_fortune` - Daily fortune info
- `check_zodiac_compatibility` - Zodiac compatibility

### 🎊 Festival Tools (4)
- `get_lunar_festivals` - Festivals on date
- `get_next_festival` - Next upcoming festival
- `get_festival_details` - Festival information
- `get_annual_festivals` - Annual calendar

### 🌙 Moon Phase Tools (4)
- `get_moon_phase` - Moon phase info
- `get_moon_calendar` - Monthly calendar
- `get_moon_influence` - Activity influence
- `predict_moon_phases` - Phase predictions

### 📅 Calendar Conversion Tools (3)
- `solar_to_lunar` - Solar to lunar conversion
- `lunar_to_solar` - Lunar to solar conversion
- `get_zodiac_info` - Zodiac information

### ⚡ Advanced Tools (3)
- `batch_check_dates` - Check multiple dates
- `compare_dates` - Compare dates
- `get_lucky_hours` - Lucky hours of day

**[📖 Complete API Reference →](./docs/tools-reference.md)**

## 🏮 Cultural Traditions

Based on traditional Chinese calendar systems:

- **Lunar Calendar** - Traditional lunar-solar calendar
- **12 Zodiac Animals** - Rat, Ox, Tiger, Rabbit, Dragon, Snake, Horse, Goat, Monkey, Rooster, Dog, Pig
- **Five Elements** - Wood, Fire, Earth, Metal, Water
- **28 Lunar Mansions** - Traditional stellar divisions
- **Traditional Festivals** - Spring Festival, Mid-Autumn, Dragon Boat, and more

**[📖 Cultural Traditions Guide →](./docs/cultural-traditions.md)**

## 📝 Example Usage

```python
import asyncio
from lunar_mcp_server import LunarMCPServer

async def main():
    server = LunarMCPServer()

    # Check if date is auspicious for wedding
    result = await server._check_auspicious_date(
        date="2024-03-15",
        activity="wedding",
        culture="chinese"
    )
    print(f"Auspiciousness: {result['auspicious_level']}")
    print(f"Score: {result['score']}/10")

asyncio.run(main())
```

**[📖 More Examples →](./docs/usage-examples.md)**

## 🧪 Testing

```bash
# Run comprehensive MCP server tests
./scripts/test_mcp_final.sh

# Run unit tests
uv run pytest --cov
```

**[📖 Testing Guide →](./docs/testing.md)**

## 📦 Publishing

This server is published to:

- **PyPI**: `pip install lunar-mcp-server`
- **Smithery.ai**: `npx @smithery/cli install lunar-mcp-server` *(coming soon)*

**[📖 Publishing Guide →](./docs/smithery-publishing.md)**

## 🛠️ Development

```bash
# Clone and setup
git clone https://github.com/AngusHsu/lunar-mcp-server.git
cd lunar-mcp-server
uv sync --dev

# Code quality
uv run black src/ tests/
uv run ruff check src/ tests/
uv run mypy src/
```

**[📖 Development Guide →](./docs/development.md)**

## 📚 Documentation

- [📖 Usage Examples](./docs/usage-examples.md) - Practical examples and integration guides
- [📖 Tools Reference](./docs/tools-reference.md) - Complete API documentation
- [📖 Cultural Traditions](./docs/cultural-traditions.md) - Understanding Chinese calendar systems
- [📖 Testing Guide](./docs/testing.md) - Running and writing tests
- [📖 Development Guide](./docs/development.md) - Contributing to the project
- [📖 Smithery Publishing](./docs/smithery-publishing.md) - Publishing to MCP registry

## 📄 License

MIT License - see [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

Built with dedication for preserving and sharing traditional calendar wisdom.

---

<div align="center">

**[⭐ Star on GitHub](https://github.com/AngusHsu/lunar-mcp-server)** | **[📦 View on PyPI](https://pypi.org/project/lunar-mcp-server/)** | **[🐛 Report Issues](https://github.com/AngusHsu/lunar-mcp-server/issues)**

</div>
