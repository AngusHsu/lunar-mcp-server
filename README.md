<div align="center">

# 🌙 Lunar Calendar MCP Server

### Traditional Chinese Lunar Calendar for AI Applications

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-2025--11--25-green.svg)](https://modelcontextprotocol.io)
[![CI](https://github.com/AngusHsu/lunar-mcp-server/actions/workflows/ci.yaml/badge.svg)](https://github.com/AngusHsu/lunar-mcp-server/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/AngusHsu/lunar-mcp-server/branch/main/graph/badge.svg)](https://codecov.io/gh/AngusHsu/lunar-mcp-server)
[![Tests](https://img.shields.io/badge/tests-37%20passed-brightgreen.svg)](./scripts/test_mcp_final.sh)
[![PyPI version](https://badge.fury.io/py/lunar-mcp-server.svg)](https://pypi.org/project/lunar-mcp-server/)

**20 Tools** | **BaZi (八字)** | **Chinese Zodiac** | **Five Elements** | **Moon Phases** | **Festivals** | **Auspicious Dates**

---

</div>

Standard CPython 3.11, 3.12, 3.13, and 3.14 are supported and tested. Python
3.14 free-threaded builds are not part of the v1.2.1 support guarantee.

## 📖 Overview

A comprehensive Model Context Protocol (MCP) server providing traditional Chinese lunar calendar information, auspicious date checking, and festival data based on Chinese cultural traditions.

Perfect for integrating ancient Chinese wisdom into modern AI applications through the Model Context Protocol.

## ✨ Features

- 🎯 **Auspicious Date Analysis** - Check favorable dates, find good dates, daily fortune, zodiac compatibility
- 🎊 **Festival Information** - Chinese festivals, next festival, festival details, annual calendars
- 🌙 **Moon Phase Analysis** - Accurate moon phases, location-aware, activity influence, monthly calendars
- 📅 **Calendar Conversions** - Solar-lunar conversion, zodiac information, cultural integration
- 🔮 **BaZi (八字) Four Pillars** - Birth chart analysis, destiny calculation, compatibility reading
- ⚡ **Advanced Tools** - Batch checking, date comparison, lucky hours

**[📚 Complete Features List →](./docs/tools-reference.md)**

## 🚀 Quick Start in 30 Seconds

### One-Line Installation

The fastest way to get started - no Python installation required:

```bash
# Install and run with uvx (recommended)
uvx lunar-mcp-server
```

### Try It Out

Once running, you can immediately ask questions like:

- "Is today a good day for a wedding?"
- "When is the next Chinese festival?"
- "What's my Chinese zodiac sign if I was born in 1990?"
- "Find me 3 auspicious dates for moving house in March 2024"
- "Calculate my BaZi (八字) for 1990-05-15 14:30"
- "Check our BaZi compatibility for marriage"

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

Then restart Claude Desktop and start asking about lunar calendar information!

### MCP compatibility

- MCP Python SDK: `>=1.28.1,<2` (the lockfile records the exact tested v1 release)
- Primary protocol: `2025-11-25`
- Backward-compatible initialization: `2024-11-05`
- Production transport: STDIO

MCP SDK v2, the prerelease 2026 protocol, and remote production transports are
not part of the v1.2.1 compatibility contract.

### Alternative Installation Methods

```bash
# Using pip
pip install lunar-mcp-server
lunar-mcp-server

# Using uv
uv tool install lunar-mcp-server
lunar-mcp-server

# From source (for development)
git clone https://github.com/AngusHsu/lunar-mcp-server.git
cd lunar-mcp-server
uv sync
uv run lunar-mcp-server
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

### 🔮 BaZi (八字) Tools (2)
- `calculate_bazi` - Calculate Four Pillars of Destiny
- `calculate_bazi_compatibility` - BaZi compatibility analysis

### ⚡ Advanced Tools (3)
- `batch_check_dates` - Check multiple dates
- `compare_dates` - Compare dates
- `get_lucky_hours` - Lucky hours of day

**[📖 Complete API Reference →](./docs/tools-reference.md)**

## 🔮 BaZi (八字) - Four Pillars of Destiny

The BaZi feature provides authentic traditional Chinese fortune-telling based on birth date and time.

### What is BaZi?

BaZi (八字), also known as "Four Pillars of Destiny" or "Eight Characters," is a traditional Chinese astrological system that analyzes a person's destiny and characteristics based on the cosmic energies present at their birth. Each person has four pillars (year, month, day, hour), and each pillar consists of two characters (a Heavenly Stem and an Earthly Branch), totaling eight characters.

### Features

- **Complete Four Pillars Analysis**: Year (年柱), Month (月柱), Day (日柱), Hour (时柱)
- **Heavenly Stems & Earthly Branches**: All 10 stems (天干) and 12 branches (地支)
- **Five Elements Analysis**: Wood, Fire, Earth, Metal, Water distribution and balance
- **Day Master (日主)**: Your core element and personality traits
- **Life Stage Insights**: How each pillar influences different life periods
- **Element Recommendations**: Favorable colors, directions, and career paths
- **Compatibility Analysis**: Relationship harmony based on element interactions
- **Timezone Support**: Accurate calculations for any timezone

### Example Usage

```python
from lunar_mcp_server.bazi import BaZiCalculator

calculator = BaZiCalculator()

# Calculate BaZi chart
result = await calculator.calculate_bazi("1990-05-15 14:30", timezone_offset=8)

print(f"Eight Characters: {result['eight_characters']}")
# Output: 庚午乙巳丙子乙未

print(f"Day Master: {result['day_master']['element']} {result['day_master']['polarity']}")
# Output: Day Master: Fire Yang

# Check compatibility
compat = await calculator.get_compatibility(
    "1990-05-15 14:30",
    "1992-08-20 10:00",
    timezone_offset=8
)

print(f"Compatibility: {compat['compatibility_score']}/10 - {compat['compatibility_level']}")
# Output: Compatibility: 8/10 - Excellent
print(f"Relationship: {compat['element_relationship']}")
# Output: Wood generates Fire - supportive relationship
```

### Understanding Your BaZi Chart

Each pillar represents different aspects of your life:

- **Year Pillar (年柱)**: Ancestors, early life (0-15 years), inherited characteristics
- **Month Pillar (月柱)**: Parents, youth (16-30 years), career development
- **Day Pillar (日柱)**: Self, spouse, middle age (31-45 years), marriage
- **Hour Pillar (时柱)**: Children, later life (46+ years), legacy

The **Day Master** (your day pillar's Heavenly Stem) represents your core self and is the most important element in BaZi analysis.

### Element Relationships

BaZi uses two key cycles:

- **Generation Cycle (生)**: Wood → Fire → Earth → Metal → Water → Wood
- **Control Cycle (克)**: Wood → Earth → Water → Fire → Metal → Wood

These relationships determine compatibility and element balance in your chart.

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

### Python API

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

### Example Output

Here's what you can expect when checking an auspicious date:

```json
{
  "date": "2024-03-15",
  "activity": "wedding",
  "auspicious_level": "Very Auspicious",
  "score": 8.5,
  "lunar_date": {
    "year": 2024,
    "month": 2,
    "day": 6,
    "zodiac": "Dragon",
    "element": "Wood"
  },
  "recommendations": [
    "Excellent day for new beginnings",
    "Dragon day brings good fortune",
    "Wood element supports growth"
  ],
  "lucky_hours": ["7-9 AM", "11 AM-1 PM", "5-7 PM"],
  "favorable_colors": ["red", "gold", "purple"],
  "things_to_do": ["Marriage ceremony", "Important contracts", "Grand openings"],
  "things_to_avoid": ["Funerals", "Moving house", "Starting construction"]
}
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
