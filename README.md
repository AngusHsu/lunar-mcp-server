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

## Features

### Auspicious Date Analysis
- **Traditional Date Checking**: Determine if dates are favorable for specific activities based on lunar calendar wisdom
- **Good Date Discovery**: Find optimal dates within date ranges for various activities
- **Daily Fortune Analysis**: Get comprehensive daily luck and fortune information
- **Zodiac Compatibility**: Check compatibility between dates based on zodiac systems

### Festival & Holiday Information
- **Chinese Festivals**: Comprehensive support for traditional Chinese festival calendar
- **Festival Discovery**: Find next upcoming festivals and get detailed information
- **Annual Planning**: Get complete festival calendars for any year
- **Cultural Context**: Rich cultural and historical background for each festival

### Moon Phase Analysis
- **Accurate Moon Phases**: Calculate precise moon phases with astronomical data
- **Location-Aware**: Consider geographic location for moon rise/set times
- **Activity Influence**: Understand how moon phases affect specific activities
- **Monthly Calendars**: Generate comprehensive monthly moon phase calendars

### Calendar Conversions
- **Solar-Lunar Conversion**: Convert between solar (Gregorian) and Chinese lunar calendar
- **Chinese Zodiac Information**: Get detailed Chinese zodiac information including animals, elements, and compatibility
- **Cultural Integration**: Seamless integration with Chinese cultural traditions and practices

## Installation

### Using UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/AngusHsu/lunar-mcp-server.git
cd lunar-mcp-server

# Install with UV
uv sync

# Install development dependencies
uv sync --dev
```

### Using pip

```bash
# Install the package
pip install lunar-mcp-server

# Or install from source
pip install -e .
```

## Quick Start

### Running the MCP Server

```bash
# Using UV (development)
uv run lunar-mcp-server

# Using uvx (run without installing)
uvx lunar-mcp-server

# After pip install
lunar-mcp-server

# Using Python module
python -m lunar_mcp_server.server
```

### Basic Usage Examples

#### Check if a Date is Auspicious
```python
import asyncio
from lunar_mcp_server import LunarMCPServer

async def check_wedding_date():
    server = LunarMCPServer()
    result = await server._check_auspicious_date(
        date="2024-03-15",
        activity="wedding",
        culture="chinese"
    )
    print(f"Wedding on 2024-03-15: {result['auspicious_level']}")
    print(f"Recommendations: {result['recommendations']}")

asyncio.run(check_wedding_date())
```

#### Find Good Dates for Business Opening
```python
async def find_business_dates():
    server = LunarMCPServer()
    result = await server._find_good_dates(
        start_date="2024-04-01",
        end_date="2024-04-30",
        activity="business_opening",
        culture="chinese",
        limit=5
    )
    print("Best dates for business opening:")
    for date_info in result['good_dates']:
        print(f"- {date_info['date']}: {date_info['level']} (score: {date_info['score']})")

asyncio.run(find_business_dates())
```

#### Get Moon Phase Information
```python
async def moon_phase_info():
    server = LunarMCPServer()
    result = await server._get_moon_phase(
        date="2024-02-14",
        location="40.7128,-74.0060"  # New York City
    )
    print(f"Moon phase on 2024-02-14: {result['phase_name']}")
    print(f"Illumination: {result['illumination']:.1%}")
    print(f"Good for: {', '.join(result['influence']['good_for'])}")

asyncio.run(moon_phase_info())
```

#### Get Festival Information
```python
async def festival_info():
    server = LunarMCPServer()
    result = await server._get_lunar_festivals(
        date="2024-02-10",
        culture="chinese"
    )
    if result['festivals']:
        festival = result['festivals'][0]
        print(f"Festival: {festival['name']}")
        print(f"Significance: {festival['significance']}")
        print(f"Traditions: {', '.join(festival['traditions'])}")

asyncio.run(festival_info())
```

## MCP Tools Reference

### Auspicious Date Tools

#### `check_auspicious_date`
Check if a date is favorable for specific activities.

**Parameters:**
- `date` (string): Date in YYYY-MM-DD format
- `activity` (string): Activity type (e.g., wedding, business_opening, travel)
- `culture` (string, optional): Cultural tradition (chinese)

**Response:**
```json
{
  "date": "2024-02-14",
  "lunar_date": "2024-1-5",
  "auspicious_level": "very_good",
  "score": 8,
  "good_for": ["wedding", "business_opening", "travel"],
  "avoid": ["funeral", "major_surgery"],
  "lucky_hours": ["9:00-11:00", "13:00-15:00"],
  "zodiac_day": "dragon",
  "five_elements": "wood",
  "recommendations": "Excellent day for new beginnings"
}
```

## Chinese Cultural Traditions Supported

### Chinese Calendar (Traditional)
- **Lunar Calendar**: Traditional Chinese lunar calendar with accurate conversions
- **Zodiac Animals**: 12-year cycle with detailed characteristics and compatibility
- **Five Elements**: Wood, Fire, Earth, Metal, Water with their interactions
- **Lunar Mansions**: 28 stellar mansions for detailed auspiciousness calculations
- **Traditional Festivals**: Spring Festival, Mid-Autumn, Dragon Boat, Qingming, etc.

## Testing

### Running MCP Server Tests

Test the MCP server functionality with our comprehensive test suite:

```bash
# Run the complete test suite (recommended)
./scripts/test_mcp_final.sh

# Alternative test scripts for different scenarios
./scripts/test_mcp_simple.sh      # Basic functionality test
./scripts/test_mcp_server.sh      # FIFO-based test
```

The comprehensive test suite will verify:
- ✅ Server startup and STDIO handling
- ✅ MCP protocol initialization
- ✅ All 18 available tools across 5 categories
- ✅ Error handling for invalid inputs
- ✅ Chinese cultural tradition support

See [Test Documentation](./docs/testing.md) for detailed information about the test suite.

## Development

### Running Unit Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/test_lunar_calculations.py
```

### Code Quality

```bash
# Format code
uv run black src/ tests/

# Sort imports
uv run isort src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

## License

MIT License - see LICENSE file for details.

---

*Built with dedication for preserving and sharing traditional calendar wisdom*