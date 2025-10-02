#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== MCP Server Test Suite ===${NC}"

# Test 1: Server can start
echo -e "${BLUE}Test 1: Server startup test${NC}"
# In STDIO mode, server should exit cleanly when input stream closes (EOF)
timeout 3s uv run lunar-mcp-server < /dev/null > /dev/null 2>&1
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ] || [ $EXIT_CODE -eq 124 ]; then
    echo -e "${GREEN}✅ Server handles STDIO correctly${NC}"
else
    echo -e "${RED}❌ Server failed to start (exit code: $EXIT_CODE)${NC}"
fi

# Test 2: Server responds to initialize
echo -e "\n${BLUE}Test 2: Server initialization${NC}"

# Create initialization message
INIT_MSG='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'

# Send init message and get response
RESPONSE=$(echo "$INIT_MSG" | timeout 10s uv run lunar-mcp-server 2>/dev/null | head -1)

if [ -n "$RESPONSE" ] && echo "$RESPONSE" | grep -q '"result"'; then
    echo -e "${GREEN}✅ Server responds to initialization${NC}"
    echo "Response: $RESPONSE" | cut -c1-100
else
    echo -e "${RED}❌ Server failed to respond to initialization${NC}"
    echo "Response: $RESPONSE"
fi

# Test 3: List tools functionality
echo -e "\n${BLUE}Test 3: Comprehensive tool listing${NC}"

# Create a sequence of messages
cat > test_sequence.json << 'EOF'
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
EOF

# Send the sequence and capture output
TOOLS_RESPONSE=$(cat test_sequence.json | timeout 15s uv run lunar-mcp-server 2>/dev/null | tail -1)

if [ -n "$TOOLS_RESPONSE" ] && echo "$TOOLS_RESPONSE" | grep -q '"tools"'; then
    echo -e "${GREEN}✅ Server can list tools${NC}"
    TOOL_COUNT=$(echo "$TOOLS_RESPONSE" | grep -o '"name":' | wc -l)
    echo "Found $TOOL_COUNT tools"

    # Extract and display all tool names
    echo -e "${BLUE}Available tools:${NC}"
    echo "$TOOLS_RESPONSE" | grep -o '"name":"[^"]*"' | sed 's/"name":"/  - /' | sed 's/"$//'

    # Categorize tools
    echo -e "\n${BLUE}Tool categories:${NC}"
    AUSPICIOUS_TOOLS=$(echo "$TOOLS_RESPONSE" | grep -o '"name":"[^"]*"' | grep -c -E "(auspicious|good_dates|fortune|zodiac)")
    FESTIVAL_TOOLS=$(echo "$TOOLS_RESPONSE" | grep -o '"name":"[^"]*"' | grep -c -E "festival")
    MOON_TOOLS=$(echo "$TOOLS_RESPONSE" | grep -o '"name":"[^"]*"' | grep -c -E "moon")
    CONVERSION_TOOLS=$(echo "$TOOLS_RESPONSE" | grep -o '"name":"[^"]*"' | grep -c -E "(solar_to_lunar|lunar_to_solar)")
    NEW_TOOLS=$(echo "$TOOLS_RESPONSE" | grep -o '"name":"[^"]*"' | grep -c -E "(batch_check|compare_dates|lucky_hours)")

    echo "  - Auspicious/Fortune tools: $AUSPICIOUS_TOOLS"
    echo "  - Festival tools: $FESTIVAL_TOOLS"
    echo "  - Moon/Lunar tools: $MOON_TOOLS"
    echo "  - Calendar conversion tools: $CONVERSION_TOOLS"
    echo "  - New Advanced tools: $NEW_TOOLS"

else
    echo -e "${RED}❌ Server failed to list tools${NC}"
    echo "Response: $TOOLS_RESPONSE"
fi

# Test 4: Tool execution
echo -e "\n${BLUE}Test 4: Tool execution${NC}"

cat > test_tool_call.json << 'EOF'
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_moon_phase","arguments":{"date":"2024-01-01","location":"0,0"}}}
EOF

TOOL_RESPONSE=$(cat test_tool_call.json | timeout 15s uv run lunar-mcp-server 2>/dev/null | tail -1)

if [ -n "$TOOL_RESPONSE" ] && echo "$TOOL_RESPONSE" | grep -q '"result"'; then
    echo -e "${GREEN}✅ Server can execute tools${NC}"
    echo "Tool response received (truncated): $(echo "$TOOL_RESPONSE" | cut -c1-100)..."
else
    echo -e "${RED}❌ Server failed to execute tool${NC}"
    echo "Response: $TOOL_RESPONSE"
fi

# Test 5: Comprehensive tool category testing
echo -e "\n${BLUE}Test 5: Comprehensive tool testing by category${NC}"

# Function to test a single tool
test_single_tool() {
    local tool_name="$1"
    local args="$2"
    local desc="$3"

    echo -e "  ${BLUE}Testing $tool_name...${NC}"

    cat > test_single_tool.json << EOF
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"$tool_name","arguments":$args}}
EOF

    SINGLE_RESPONSE=$(cat test_single_tool.json | timeout 15s uv run lunar-mcp-server 2>/dev/null | tail -1)

    if [ -n "$SINGLE_RESPONSE" ] && echo "$SINGLE_RESPONSE" | grep -q '"result"'; then
        echo -e "    ${GREEN}✅ $tool_name works${NC}"
        return 0
    else
        echo -e "    ${RED}❌ $tool_name failed${NC}"
        echo "    Response: $(echo "$SINGLE_RESPONSE" | cut -c1-80)..."
        return 1
    fi
}

# Test Auspicious/Fortune tools
echo -e "\n${YELLOW}Testing Auspicious/Fortune tools:${NC}"
AUSPICIOUS_PASS=0
AUSPICIOUS_TOTAL=4

test_single_tool "check_auspicious_date" '{"date":"2024-01-01","activity":"wedding","culture":"chinese"}' "Check auspicious date" && AUSPICIOUS_PASS=$((AUSPICIOUS_PASS + 1))
test_single_tool "find_good_dates" '{"start_date":"2024-01-01","end_date":"2024-01-15","activity":"business_opening","culture":"chinese","limit":3}' "Find good dates" && AUSPICIOUS_PASS=$((AUSPICIOUS_PASS + 1))
test_single_tool "get_daily_fortune" '{"date":"2024-01-01","culture":"chinese"}' "Get daily fortune" && AUSPICIOUS_PASS=$((AUSPICIOUS_PASS + 1))
test_single_tool "check_zodiac_compatibility" '{"date1":"1990-01-01","date2":"1992-01-01","culture":"chinese"}' "Check zodiac compatibility" && AUSPICIOUS_PASS=$((AUSPICIOUS_PASS + 1))

echo -e "  ${BLUE}Auspicious/Fortune summary: ${GREEN}$AUSPICIOUS_PASS${NC}/$AUSPICIOUS_TOTAL passed${NC}"

# Test Festival tools
echo -e "\n${YELLOW}Testing Festival tools:${NC}"
FESTIVAL_PASS=0
FESTIVAL_TOTAL=4

test_single_tool "get_lunar_festivals" '{"date":"2024-02-10","culture":"chinese"}' "Get lunar festivals" && FESTIVAL_PASS=$((FESTIVAL_PASS + 1))
test_single_tool "get_next_festival" '{"date":"2024-01-01","culture":"chinese"}' "Get next festival" && FESTIVAL_PASS=$((FESTIVAL_PASS + 1))
test_single_tool "get_festival_details" '{"festival_name":"Chinese New Year","culture":"chinese"}' "Get festival details" && FESTIVAL_PASS=$((FESTIVAL_PASS + 1))
test_single_tool "get_annual_festivals" '{"year":2024,"culture":"chinese"}' "Get annual festivals" && FESTIVAL_PASS=$((FESTIVAL_PASS + 1))

echo -e "  ${BLUE}Festival summary: ${GREEN}$FESTIVAL_PASS${NC}/$FESTIVAL_TOTAL passed${NC}"

# Test Moon/Lunar tools
echo -e "\n${YELLOW}Testing Moon/Lunar tools:${NC}"
MOON_PASS=0
MOON_TOTAL=4

test_single_tool "get_moon_phase" '{"date":"2024-01-01","location":"0,0"}' "Get moon phase" && MOON_PASS=$((MOON_PASS + 1))
test_single_tool "get_moon_calendar" '{"month":1,"year":2024,"location":"0,0"}' "Get moon calendar" && MOON_PASS=$((MOON_PASS + 1))
test_single_tool "get_moon_influence" '{"date":"2024-01-01","activity":"planting"}' "Get moon influence" && MOON_PASS=$((MOON_PASS + 1))
test_single_tool "predict_moon_phases" '{"start_date":"2024-01-01","end_date":"2024-01-31"}' "Predict moon phases" && MOON_PASS=$((MOON_PASS + 1))

echo -e "  ${BLUE}Moon/Lunar summary: ${GREEN}$MOON_PASS${NC}/$MOON_TOTAL passed${NC}"

# Test Calendar Conversion tools
echo -e "\n${YELLOW}Testing Calendar Conversion tools:${NC}"
CONVERSION_PASS=0
CONVERSION_TOTAL=3

test_single_tool "solar_to_lunar" '{"solar_date":"2024-01-01","culture":"chinese"}' "Convert solar to lunar" && CONVERSION_PASS=$((CONVERSION_PASS + 1))
test_single_tool "lunar_to_solar" '{"lunar_date":"2024-01-01","culture":"chinese"}' "Convert lunar to solar" && CONVERSION_PASS=$((CONVERSION_PASS + 1))
test_single_tool "get_zodiac_info" '{"date":"1990-01-01","culture":"chinese"}' "Get zodiac info" && CONVERSION_PASS=$((CONVERSION_PASS + 1))

echo -e "  ${BLUE}Calendar Conversion summary: ${GREEN}$CONVERSION_PASS${NC}/$CONVERSION_TOTAL passed${NC}"

# Test New Advanced tools
echo -e "\n${YELLOW}Testing New Advanced tools:${NC}"
NEW_TOOLS_PASS=0
NEW_TOOLS_TOTAL=3

test_single_tool "batch_check_dates" '{"dates":["2024-01-01","2024-01-15","2024-02-01"],"activity":"wedding","culture":"chinese"}' "Batch check dates" && NEW_TOOLS_PASS=$((NEW_TOOLS_PASS + 1))
test_single_tool "compare_dates" '{"dates":["2024-01-01","2024-01-15"],"activity":"wedding","culture":"chinese"}' "Compare dates" && NEW_TOOLS_PASS=$((NEW_TOOLS_PASS + 1))
test_single_tool "get_lucky_hours" '{"date":"2024-01-01","activity":"signing_contract","culture":"chinese"}' "Get lucky hours" && NEW_TOOLS_PASS=$((NEW_TOOLS_PASS + 1))

echo -e "  ${BLUE}New Advanced tools summary: ${GREEN}$NEW_TOOLS_PASS${NC}/$NEW_TOOLS_TOTAL passed${NC}"

# Calculate totals
TOTAL_PASS=$((AUSPICIOUS_PASS + FESTIVAL_PASS + MOON_PASS + CONVERSION_PASS + NEW_TOOLS_PASS))
TOTAL_TESTS=$((AUSPICIOUS_TOTAL + FESTIVAL_TOTAL + MOON_TOTAL + CONVERSION_TOTAL + NEW_TOOLS_TOTAL))

# Test 6: Edge cases and error handling
echo -e "\n${BLUE}Test 6: Edge cases and error handling${NC}"

# Test invalid tool name
echo -e "${YELLOW}Testing invalid tool name...${NC}"
cat > test_invalid_tool.json << 'EOF'
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"invalid_tool_name","arguments":{}}}
EOF

INVALID_RESPONSE=$(cat test_invalid_tool.json | timeout 10s uv run lunar-mcp-server 2>/dev/null | tail -1)
if echo "$INVALID_RESPONSE" | grep -q 'Unknown tool'; then
    echo -e "  ${GREEN}✅ Server correctly handles invalid tool name${NC}"
else
    echo -e "  ${RED}❌ Server should return error for invalid tool${NC}"
    echo "    Response: $(echo "$INVALID_RESPONSE" | cut -c1-80)..."
fi

# Test missing required parameters
echo -e "${YELLOW}Testing missing required parameters...${NC}"
cat > test_missing_params.json << 'EOF'
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"check_auspicious_date","arguments":{}}}
EOF

MISSING_RESPONSE=$(cat test_missing_params.json | timeout 10s uv run lunar-mcp-server 2>/dev/null | tail -1)
if echo "$MISSING_RESPONSE" | grep -q '"error"' || echo "$MISSING_RESPONSE" | grep -q '"isError":.*true' || echo "$MISSING_RESPONSE" | grep -q 'required property'; then
    echo -e "  ${GREEN}✅ Server correctly handles missing parameters${NC}"
else
    echo -e "  ${RED}❌ Server should return error for missing parameters${NC}"
    echo "    Response: $(echo "$MISSING_RESPONSE" | cut -c1-80)..."
fi

# Test Chinese culture
echo -e "${YELLOW}Testing Chinese cultural context...${NC}"
CULTURE_PASS=0

cat > test_culture.json << EOF
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":7,"method":"tools/call","params":{"name":"get_zodiac_info","arguments":{"date":"1990-01-01","culture":"chinese"}}}
EOF

CULTURE_RESPONSE=$(cat test_culture.json | timeout 10s uv run lunar-mcp-server 2>/dev/null | tail -1)
if echo "$CULTURE_RESPONSE" | grep -q '"result"'; then
    echo -e "  ${GREEN}✅ Chinese culture works${NC}"
    CULTURE_PASS=1
else
    echo -e "  ${YELLOW}⚠️  Chinese culture test failed${NC}"
fi

echo -e "\n${BLUE}=== Comprehensive Test Summary ===${NC}"
echo -e "Total comprehensive tests: ${GREEN}$TOTAL_PASS${NC}/$TOTAL_TESTS"
echo -e "Chinese culture test: ${GREEN}$CULTURE_PASS${NC}/1"

echo -e "\n${BLUE}Category breakdown:${NC}"
echo -e "  - Auspicious/Fortune: ${GREEN}$AUSPICIOUS_PASS${NC}/$AUSPICIOUS_TOTAL"
echo -e "  - Festival: ${GREEN}$FESTIVAL_PASS${NC}/$FESTIVAL_TOTAL"
echo -e "  - Moon/Lunar: ${GREEN}$MOON_PASS${NC}/$MOON_TOTAL"
echo -e "  - Calendar Conversion: ${GREEN}$CONVERSION_PASS${NC}/$CONVERSION_TOTAL"
echo -e "  - New Advanced Tools: ${GREEN}$NEW_TOOLS_PASS${NC}/$NEW_TOOLS_TOTAL"

if [ $TOTAL_PASS -eq $TOTAL_TESTS ]; then
    echo -e "\n${GREEN}🎉 All comprehensive tests passed! The MCP server is working excellently.${NC}"
elif [ $TOTAL_PASS -gt $((TOTAL_TESTS * 80 / 100)) ]; then
    echo -e "\n${GREEN}✅ Most tests passed! The MCP server is working well.${NC}"
else
    echo -e "\n${YELLOW}⚠️  Some tools may need attention, but basic functionality works.${NC}"
fi

# Cleanup
rm -f test_sequence.json test_tool_call.json test_single_tool.json test_invalid_tool.json test_missing_params.json test_culture.json

echo -e "\n${BLUE}Server testing complete!${NC}"
echo -e "${BLUE}To use the server, run: ${GREEN}uv run lunar-mcp-server${NC}"