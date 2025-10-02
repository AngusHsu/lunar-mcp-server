#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global variables
SERVER_PID=""
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

# Test if server can start and respond
echo -e "${BLUE}Testing MCP server startup...${NC}"

# Create a simple Python MCP client
cat > test_client.py << 'EOF'
#!/usr/bin/env python3
import asyncio
import json
import sys
from mcp.client.stdio import stdio_client

async def test_server():
    try:
        print("Connecting to MCP server...")

        async with stdio_client() as (read, write):
            # Initialize
            init_result = await read.read_message()
            print(f"Server capabilities: {json.dumps(init_result, indent=2)}")

            # Send initialized notification
            await write.send_message({
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
            })

            # List tools
            print("Listing tools...")
            list_result = await write.send_request({
                "method": "tools/list",
                "params": {}
            })

            print(f"Available tools: {len(list_result.get('tools', []))}")
            for tool in list_result.get('tools', []):
                print(f"  - {tool['name']}: {tool['description']}")

            # Test a simple tool call
            print("\nTesting check_auspicious_date tool...")
            tool_result = await write.send_request({
                "method": "tools/call",
                "params": {
                    "name": "check_auspicious_date",
                    "arguments": {
                        "date": "2024-01-01",
                        "activity": "wedding",
                        "culture": "chinese"
                    }
                }
            })

            print(f"Tool result: {json.dumps(tool_result, indent=2)}")
            print("✅ Basic test passed!")
            return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_server())
    sys.exit(0 if result else 1)
EOF

# Start the server in background
echo -e "${BLUE}Starting MCP server...${NC}"
uv run lunar-mcp-server > server_output.log 2>&1 &
SERVER_PID=$!

echo "MCP server started with PID: $SERVER_PID"

# Give server time to start
sleep 3

# Check if server is still running
if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo -e "${RED}Server failed to start!${NC}"
    cat server_output.log
    exit 1
fi

# Run the Python test client
echo -e "${BLUE}Running MCP client tests...${NC}"
TEST_COUNT=1

if python3 test_client.py; then
    echo -e "${GREEN}✅ MCP server test passed!${NC}"
    PASS_COUNT=1
else
    echo -e "${RED}❌ MCP server test failed!${NC}"
    FAIL_COUNT=1
    echo "Server output:"
    cat server_output.log
fi

# Clean up test files
rm -f test_client.py server_output.log

echo -e "${BLUE}Test completed!${NC}"