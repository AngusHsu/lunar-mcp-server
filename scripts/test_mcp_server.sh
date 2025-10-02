#!/bin/bash
#
# MCP Server Test Script (FIFO-based)
# Tests all 18 MCP tools using FIFO pipes for STDIO communication
#
# NOTE: For more comprehensive testing with better error handling,
# consider using test_mcp_final.sh instead. This script uses FIFOs
# which can have timing issues on slower systems.
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global variables
SERVER_PID=""
TEMP_DIR="/tmp/mcp_test_$$"
FIFO_IN="$TEMP_DIR/mcp_in"
FIFO_OUT="$TEMP_DIR/mcp_out"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# Cleanup function
cleanup() {
    echo -e "${YELLOW}Cleaning up...${NC}"

    # Kill server if running
    if [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "Stopping MCP server (PID: $SERVER_PID)"
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi

    # Remove temp directory
    rm -rf "$TEMP_DIR" 2>/dev/null || true

    echo -e "${BLUE}Test Summary:${NC}"
    echo -e "Total tests: $TEST_COUNT"
    echo -e "${GREEN}Passed: $PASS_COUNT${NC}"
    echo -e "${RED}Failed: $FAIL_COUNT${NC}"

    if [ $FAIL_COUNT -eq 0 ]; then
        echo -e "${GREEN}All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}Some tests failed!${NC}"
        exit 1
    fi
}

# Set up signal handlers
trap cleanup EXIT INT TERM

# Create temp directory and FIFOs
echo -e "${BLUE}Setting up test environment...${NC}"
mkdir -p "$TEMP_DIR"
mkfifo "$FIFO_IN"
mkfifo "$FIFO_OUT"

# Start MCP server in background
echo -e "${BLUE}Starting MCP server...${NC}"
uv run lunar-mcp-server < "$FIFO_IN" > "$FIFO_OUT" 2>"$TEMP_DIR/server.log" &
SERVER_PID=$!

echo "MCP server started with PID: $SERVER_PID"

# Give server time to start
sleep 2

# Check if server is still running
if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo -e "${RED}Server failed to start!${NC}"
    cat "$TEMP_DIR/server.log"
    exit 1
fi

# MCP Client functions
send_mcp_request() {
    local method="$1"
    local params="$2"
    local id="$3"

    local request="{\"jsonrpc\":\"2.0\",\"method\":\"$method\",\"params\":$params,\"id\":$id}"
    echo "$request" > "$FIFO_IN"
}

read_mcp_response() {
    local timeout="$1"
    timeout "$timeout" cat "$FIFO_OUT" 2>/dev/null || echo ""
}

test_tool() {
    local tool_name="$1"
    local arguments="$2"
    local description="$3"

    TEST_COUNT=$((TEST_COUNT + 1))
    echo -e "${BLUE}Test $TEST_COUNT: $description${NC}"

    # Send tool call request
    local params="{\"name\":\"$tool_name\",\"arguments\":$arguments}"
    send_mcp_request "tools/call" "$params" "$TEST_COUNT"

    # Read response with timeout
    local response=$(read_mcp_response "10s")

    if [ -z "$response" ]; then
        echo -e "${RED}  ❌ FAIL: No response received${NC}"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        return 1
    fi

    # Validate JSON-RPC 2.0 response structure
    # Check for jsonrpc version
    if ! echo "$response" | grep -q '"jsonrpc":"2.0"'; then
        echo -e "${RED}  ❌ FAIL: Invalid JSON-RPC format${NC}"
        echo "  Response: $(echo "$response" | cut -c1-100)..."
        FAIL_COUNT=$((FAIL_COUNT + 1))
        return 1
    fi

    # Check if response contains error
    if echo "$response" | grep -q '"error"'; then
        echo -e "${RED}  ❌ FAIL: Error in response${NC}"
        echo "  Response: $(echo "$response" | cut -c1-150)..."
        FAIL_COUNT=$((FAIL_COUNT + 1))
        return 1
    fi

    # Check if response contains result
    if echo "$response" | grep -q '"result"'; then
        # Validate that result contains content
        if echo "$response" | grep -q '"content"'; then
            echo -e "${GREEN}  ✅ PASS${NC}"
            PASS_COUNT=$((PASS_COUNT + 1))
            return 0
        else
            echo -e "${YELLOW}  ⚠️  PASS (but no content field)${NC}"
            PASS_COUNT=$((PASS_COUNT + 1))
            return 0
        fi
    else
        echo -e "${RED}  ❌ FAIL: No result in response${NC}"
        echo "  Response: $(echo "$response" | cut -c1-100)..."
        FAIL_COUNT=$((FAIL_COUNT + 1))
        return 1
    fi
}

# Initialize MCP connection
echo -e "${BLUE}Initializing MCP connection...${NC}"
init_params='{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}'
send_mcp_request "initialize" "$init_params" "0"

# Read initialization response
init_response=$(read_mcp_response "5s")
if [ -z "$init_response" ]; then
    echo -e "${RED}Failed to initialize MCP connection${NC}"
    exit 1
fi

echo -e "${GREEN}MCP connection initialized${NC}"

# Send initialized notification
echo '{"jsonrpc":"2.0","method":"notifications/initialized"}' > "$FIFO_IN"

# Give sufficient time for the notification to be processed
# This prevents race conditions on slower systems
sleep 2

# Test all tools
echo -e "${BLUE}Starting tool tests...${NC}"

# Test 1: Check auspicious date
test_tool "check_auspicious_date" '{"date":"2024-01-01","activity":"wedding","culture":"chinese"}' "Check auspicious date for wedding"

# Test 2: Find good dates
test_tool "find_good_dates" '{"start_date":"2024-01-01","end_date":"2024-01-31","activity":"business_opening","culture":"chinese","limit":5}' "Find good dates for business opening"

# Test 3: Get daily fortune
test_tool "get_daily_fortune" '{"date":"2024-01-01","culture":"chinese"}' "Get daily fortune information"

# Test 4: Check zodiac compatibility
test_tool "check_zodiac_compatibility" '{"date1":"1990-01-01","date2":"1992-01-01","culture":"chinese"}' "Check zodiac compatibility"

# Test 5: Get lunar festivals
test_tool "get_lunar_festivals" '{"date":"2024-02-10","culture":"chinese"}' "Get lunar festivals for date"

# Test 6: Get next festival
test_tool "get_next_festival" '{"date":"2024-01-01","culture":"chinese"}' "Get next upcoming festival"

# Test 7: Get festival details
test_tool "get_festival_details" '{"festival_name":"Chinese New Year","culture":"chinese"}' "Get festival details"

# Test 8: Get annual festivals
test_tool "get_annual_festivals" '{"year":2024,"culture":"chinese"}' "Get annual festivals"

# Test 9: Get moon phase
test_tool "get_moon_phase" '{"date":"2024-01-01","location":"0,0"}' "Get moon phase information"

# Test 10: Get moon calendar
test_tool "get_moon_calendar" '{"month":1,"year":2024,"location":"0,0"}' "Get monthly moon calendar"

# Test 11: Get moon influence
test_tool "get_moon_influence" '{"date":"2024-01-01","activity":"planting"}' "Get moon influence on activity"

# Test 12: Predict moon phases
test_tool "predict_moon_phases" '{"start_date":"2024-01-01","end_date":"2024-01-31"}' "Predict moon phases in range"

# Test 13: Solar to lunar conversion
test_tool "solar_to_lunar" '{"solar_date":"2024-01-01","culture":"chinese"}' "Convert solar to lunar date"

# Test 14: Lunar to solar conversion
test_tool "lunar_to_solar" '{"lunar_date":"2024-01-01","culture":"chinese"}' "Convert lunar to solar date"

# Test 15: Get zodiac info
test_tool "get_zodiac_info" '{"date":"1990-01-01","culture":"chinese"}' "Get zodiac information"

# Test 16: Batch check dates
test_tool "batch_check_dates" '{"dates":["2024-01-01","2024-01-15","2024-02-01"],"activity":"wedding","culture":"chinese"}' "Batch check multiple dates"

# Test 17: Compare dates
test_tool "compare_dates" '{"dates":["2024-01-01","2024-01-15"],"activity":"wedding","culture":"chinese"}' "Compare dates side-by-side"

# Test 18: Get lucky hours
test_tool "get_lucky_hours" '{"date":"2024-01-01","activity":"signing_contract","culture":"chinese"}' "Get lucky hours for the day"

# Test list tools capability
echo -e "${BLUE}Testing list tools capability...${NC}"
TEST_COUNT=$((TEST_COUNT + 1))
send_mcp_request "tools/list" "{}" "$TEST_COUNT"
list_response=$(read_mcp_response "5s")

if [ -n "$list_response" ] && echo "$list_response" | grep -q '"tools"'; then
    echo -e "${GREEN}  ✅ PASS: List tools works${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))

    # Count tools in response
    tool_count=$(echo "$list_response" | grep -o '"name":' | wc -l)
    echo "  Found $tool_count tools"

    # Verify we have all 18 tools
    if [ "$tool_count" -eq 18 ]; then
        echo -e "  ${GREEN}✅ All 18 tools are present${NC}"
    else
        echo -e "  ${YELLOW}⚠️  Expected 18 tools, but found $tool_count${NC}"
    fi
else
    echo -e "${RED}  ❌ FAIL: List tools failed${NC}"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

echo -e "${BLUE}All tests completed!${NC}"
echo -e "${BLUE}Tested 18 MCP tools + list tools capability${NC}"

# Cleanup will be called by the trap