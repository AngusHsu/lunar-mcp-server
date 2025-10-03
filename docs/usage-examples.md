# Usage Examples

Complete examples for using the Lunar Calendar MCP Server.

## Python API Examples

### Check if a Date is Auspicious

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

### Find Good Dates for Business Opening

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

### Get Moon Phase Information

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

### Get Festival Information

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

## MCP Client Examples

### Using with Claude Desktop

Add to your Claude Desktop configuration:

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

Then ask Claude:
- "Check if March 15, 2024 is a good date for a wedding"
- "Find me the best dates in April 2024 for opening a business"
- "What's the moon phase today and what activities is it good for?"
- "When is the next Chinese festival?"

### Using MCP Inspector

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run the server with inspector
mcp-inspector uv run lunar-mcp-server
```

Visit http://localhost:5173 to test all tools interactively.

## Common Use Cases

### Wedding Date Planning

```python
async def plan_wedding():
    server = LunarMCPServer()

    # Find good dates
    dates = await server._find_good_dates(
        start_date="2024-06-01",
        end_date="2024-12-31",
        activity="wedding",
        culture="chinese",
        limit=10
    )

    # Check moon phase for each
    for date in dates['good_dates'][:3]:
        moon = await server._get_moon_phase(date['date'])
        print(f"\n{date['date']}:")
        print(f"  Auspiciousness: {date['level']}")
        print(f"  Moon: {moon['phase_name']}")
        print(f"  Score: {date['score']}/10")
```

### Business Opening Consultation

```python
async def business_consultation():
    server = LunarMCPServer()

    # Compare multiple dates
    result = await server._compare_dates(
        dates=["2024-05-01", "2024-05-08", "2024-05-15"],
        activity="business_opening",
        culture="chinese"
    )

    print(f"Best date: {result['recommendation']}")
    for date, info in result['comparison'].items():
        print(f"{date}: Score {info['score']}, {info['zodiac']['animal']}")
```

### Festival Calendar

```python
async def annual_festivals():
    server = LunarMCPServer()

    # Get all festivals for 2024
    festivals = await server._get_annual_festivals(
        year=2024,
        culture="chinese"
    )

    print(f"Total festivals: {festivals['total_festivals']}")
    for month, events in festivals['calendar'].items():
        print(f"\n{month}:")
        for event in events:
            print(f"  - {event['name']}")
```

## Error Handling

```python
async def safe_date_check():
    server = LunarMCPServer()

    try:
        result = await server._check_auspicious_date(
            date="2024-13-45",  # Invalid date
            activity="wedding",
            culture="chinese"
        )
    except ValueError as e:
        print(f"Invalid input: {e}")

    # Check for error in response
    result = await server._check_auspicious_date(
        date="2024-03-15",
        activity="wedding",
        culture="chinese"
    )

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Success: {result['auspicious_level']}")
```

## Advanced Usage

### Batch Processing

```python
async def batch_analysis():
    server = LunarMCPServer()

    dates = ["2024-03-01", "2024-03-15", "2024-04-01", "2024-05-01"]

    result = await server._batch_check_dates(
        dates=dates,
        activity="wedding",
        culture="chinese"
    )

    print(f"Best: {result['best_date']}")
    print(f"Worst: {result['worst_date']}")
    print(f"Checked: {result['total_checked']} dates")
```

### Lucky Hour Analysis

```python
async def find_lucky_hours():
    server = LunarMCPServer()

    result = await server._get_lucky_hours(
        date="2024-03-15",
        activity="signing_contract",
        culture="chinese"
    )

    print(f"Best hours on {result['date']}:")
    for hour in result['best_hours']:
        print(f"  {hour['time_range']}: {hour['level']} (score: {hour['score']})")
```

## Integration Examples

### With FastAPI

```python
from fastapi import FastAPI
from lunar_mcp_server import LunarMCPServer

app = FastAPI()
server = LunarMCPServer()

@app.get("/check-date/{date}/{activity}")
async def check_date(date: str, activity: str):
    return await server._check_auspicious_date(date, activity, "chinese")
```

### With Flask

```python
from flask import Flask, jsonify
from lunar_mcp_server import LunarMCPServer
import asyncio

app = Flask(__name__)
server = LunarMCPServer()

@app.route('/moon-phase/<date>')
def moon_phase(date):
    result = asyncio.run(server._get_moon_phase(date))
    return jsonify(result)
```

## See Also

- [Tools Reference](./tools-reference.md) - Complete API documentation
- [Cultural Traditions](./cultural-traditions.md) - Understanding the calculations
- [Development Guide](./development.md) - Contributing to the project
