# Testing Documentation

This document provides comprehensive information about testing the Lunar MCP Server, including test scripts, coverage, and methodologies.

## Overview

The Lunar MCP Server includes a comprehensive test suite that validates:
- MCP protocol compliance and STDIO communication
- All 15 available tools across multiple categories
- Error handling and edge cases
- Multi-cultural support (Chinese, Islamic, Hindu, Western)
- Real-world usage scenarios

## Test Scripts

All test scripts are located in the `./scripts/` directory and are designed to test the MCP server in STDIO mode without requiring external dependencies.

### Main Test Scripts

#### `test_mcp_final.sh` (Recommended)
**Comprehensive test suite with full coverage**

```bash
./scripts/test_mcp_final.sh
```

**Features:**
- ✅ Server startup and STDIO handling verification
- ✅ MCP protocol initialization testing
- ✅ Complete tool listing with categorization
- ✅ All 15 tools tested with realistic parameters
- ✅ Error handling validation (invalid tools, missing parameters)
- ✅ Multi-cultural context testing
- ✅ Detailed reporting with color-coded output

**Test Categories:**
1. **Auspicious/Fortune Tools** (4 tools)
   - `check_auspicious_date` - Wedding date validation
   - `find_good_dates` - Business opening date search
   - `get_daily_fortune` - Daily fortune information
   - `check_zodiac_compatibility` - Zodiac compatibility analysis

2. **Festival Tools** (4 tools)
   - `get_lunar_festivals` - Festival lookup for specific dates
   - `get_next_festival` - Upcoming festival discovery
   - `get_festival_details` - Detailed festival information
   - `get_annual_festivals` - Complete yearly festival calendar

3. **Moon/Lunar Tools** (4 tools)
   - `get_moon_phase` - Current moon phase calculation
   - `get_moon_calendar` - Monthly moon phase calendar
   - `get_moon_influence` - Moon's influence on activities
   - `predict_moon_phases` - Future moon phase predictions

4. **Calendar Conversion Tools** (3 tools)
   - `solar_to_lunar` - Solar to lunar date conversion
   - `lunar_to_solar` - Lunar to solar date conversion
   - `get_zodiac_info` - Zodiac information retrieval

#### `test_mcp_simple.sh`
**Basic functionality test**

```bash
./scripts/test_mcp_simple.sh
```

**Features:**
- Quick server startup verification
- Basic tool execution testing
- Minimal dependency validation
- Fast execution (< 30 seconds)

#### `test_mcp_server.sh`
**Advanced FIFO-based testing**

```bash
./scripts/test_mcp_server.sh
```

**Features:**
- FIFO-based server communication
- Background server process management
- Concurrent request handling
- Advanced cleanup mechanisms

#### `test_mcp_comprehensive.py`
**Python-based test implementation**

```bash
uv run python ./scripts/test_mcp_comprehensive.py
```

**Features:**
- Native Python MCP client implementation
- Asynchronous server communication
- Detailed response validation
- Object-oriented test structure

## Test Output Interpretation

### Success Indicators
```bash
✅ Server handles STDIO correctly
✅ Server responds to initialization
✅ Server can list tools
✅ All comprehensive tests passed!
```

### Test Categories Summary
```bash
=== Comprehensive Test Summary ===
Total comprehensive tests: 15/15
Cultural contexts tested: 4/4

Category breakdown:
  - Auspicious/Fortune: 4/4
  - Festival: 4/4
  - Moon/Lunar: 4/4
  - Calendar Conversion: 3/3
```

### Error Handling Validation
```bash
✅ Server correctly handles invalid tool name
✅ Server correctly handles missing parameters
✅ chinese culture works
✅ islamic culture works
✅ hindu culture works
✅ western culture works
```

## Common Test Scenarios

### 1. Tool Parameter Validation
The test suite validates tools with realistic parameters:

```json
// Auspicious date checking
{
  "date": "2024-01-01",
  "activity": "wedding",
  "culture": "chinese"
}

// Moon phase analysis
{
  "date": "2024-01-01",
  "location": "0,0"
}

// Festival lookup
{
  "date": "2024-02-10",
  "culture": "chinese"
}
```

### 2. Error Condition Testing
Tests verify proper error handling for:

- **Invalid tool names**: Returns structured error with tool name
- **Missing required parameters**: Validates input schema
- **Malformed requests**: Proper JSON-RPC error responses

### 3. Cultural Context Validation
Each cultural tradition is tested:

- **Chinese**: Traditional lunar calendar and zodiac
- **Islamic**: Hijri calendar system
- **Hindu**: Panchang calendar system
- **Western**: Modern astrological system

## Performance Considerations

### Test Execution Times
- **Complete suite**: ~2-3 minutes
- **Simple test**: ~30 seconds
- **Individual tool**: ~5-10 seconds per tool

### Resource Usage
- **Memory**: Minimal (< 50MB during testing)
- **CPU**: Light (server startup and JSON processing)
- **Network**: None (local STDIO communication)

## Troubleshooting

### Common Issues

#### Server Startup Failures
```bash
❌ Server failed to start (exit code: 1)
```
**Solutions:**
- Verify `uv` installation: `uv --version`
- Check dependencies: `uv sync --dev`
- Validate environment: `uv run python --version`

#### Tool Execution Errors
```bash
❌ tool_name failed
Response: {"error": "...", "tool": "tool_name"}
```
**Solutions:**
- Check parameter format and required fields
- Validate date formats (YYYY-MM-DD)
- Ensure cultural context is supported

#### Timeout Issues
```bash
❌ No response received
```
**Solutions:**
- Increase timeout values in test script
- Check system resources
- Verify server process isn't hanging

### Debug Mode

For detailed debugging, modify test scripts to show full responses:

```bash
# Add debug output to test scripts
echo "Full response: $RESPONSE"
```

Or run individual tools manually:

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_moon_phase","arguments":{"date":"2024-01-01"}}}' | uv run lunar-mcp-server
```

## Contributing to Tests

### Adding New Test Cases

1. **Identify test category** (Auspicious, Festival, Moon, Conversion)
2. **Define realistic parameters** based on tool schema
3. **Add to appropriate test section** in `test_mcp_final.sh`
4. **Verify with manual testing** before committing

### Test Script Structure

```bash
# Test function template
test_single_tool() {
    local tool_name="$1"
    local args="$2"
    local desc="$3"

    # Create MCP request
    cat > test.json << EOF
    {"jsonrpc":"2.0","id":1,"method":"initialize",...}
    {"jsonrpc":"2.0","method":"notifications/initialized"}
    {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"$tool_name","arguments":$args}}
EOF

    # Execute and validate
    response=$(cat test.json | timeout 15s uv run lunar-mcp-server 2>/dev/null | tail -1)

    if echo "$response" | grep -q '"result"'; then
        echo "✅ $tool_name works"
        return 0
    else
        echo "❌ $tool_name failed"
        return 1
    fi
}
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: MCP Server Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v2
      - name: Install dependencies
        run: uv sync --dev
      - name: Run MCP tests
        run: ./scripts/test_mcp_final.sh
```

### Test Automation

For automated testing environments:

```bash
# Run tests with machine-readable output
./scripts/test_mcp_final.sh 2>&1 | tee test_results.log

# Parse results
if grep -q "All comprehensive tests passed" test_results.log; then
    echo "Tests passed"
    exit 0
else
    echo "Tests failed"
    exit 1
fi
```

---

This comprehensive testing approach ensures the Lunar MCP Server maintains high quality and reliability across all supported features and cultural contexts.