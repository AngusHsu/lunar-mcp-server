#!/usr/bin/env python3
"""
Comprehensive MCP server test that starts the server, tests all tools, and stops it.
"""

import asyncio
import json
import subprocess
import sys
import time
from typing import Dict, Any, List
import signal
import os

class MCPTester:
    def __init__(self):
        self.server_process = None
        self.test_count = 0
        self.pass_count = 0
        self.fail_count = 0

    def log(self, message: str, color: str = "blue"):
        colors = {
            "red": "\033[0;31m",
            "green": "\033[0;32m",
            "yellow": "\033[1;33m",
            "blue": "\033[0;34m",
            "nc": "\033[0m"
        }
        print(f"{colors.get(color, '')}{message}{colors['nc']}")

    async def start_server(self):
        """Start the MCP server in background"""
        self.log("Starting MCP server...")

        self.server_process = subprocess.Popen(
            ["uv", "run", "lunar-mcp-server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0
        )

        # Give server time to start
        await asyncio.sleep(2)

        if self.server_process.poll() is not None:
            stdout, stderr = self.server_process.communicate()
            self.log(f"Server failed to start! Exit code: {self.server_process.returncode}", "red")
            self.log(f"STDOUT: {stdout}", "red")
            self.log(f"STDERR: {stderr}", "red")
            return False

        self.log(f"MCP server started with PID: {self.server_process.pid}", "green")
        return True

    def stop_server(self):
        """Stop the MCP server"""
        if self.server_process:
            self.log("Stopping MCP server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
                self.server_process.wait()
            self.log("MCP server stopped", "green")

    async def send_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send a message to the server and get response"""
        if not self.server_process:
            raise Exception("Server not running")

        # Send message
        message_str = json.dumps(message) + "\n"
        self.server_process.stdin.write(message_str)
        self.server_process.stdin.flush()

        # Read response
        response_line = self.server_process.stdout.readline()
        if not response_line:
            raise Exception("No response from server")

        try:
            return json.loads(response_line.strip())
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {response_line.strip()}")

    async def initialize_connection(self):
        """Initialize MCP connection"""
        self.log("Initializing MCP connection...")

        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }

        response = await self.send_message(init_request)
        if "error" in response:
            raise Exception(f"Initialize failed: {response['error']}")

        self.log("MCP connection initialized", "green")

        # Send initialized notification
        initialized_notif = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        await self.send_message(initialized_notif)

        # Give a moment for notification to process
        await asyncio.sleep(0.5)

    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools"""
        self.log("Listing available tools...")

        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        response = await self.send_message(request)
        if "error" in response:
            raise Exception(f"List tools failed: {response['error']}")

        tools = response.get("result", {}).get("tools", [])
        self.log(f"Found {len(tools)} tools", "green")

        for tool in tools:
            self.log(f"  - {tool['name']}: {tool['description']}")

        return tools

    async def test_tool(self, tool_name: str, arguments: Dict[str, Any], description: str) -> bool:
        """Test a single tool"""
        self.test_count += 1
        self.log(f"Test {self.test_count}: {description}")

        request = {
            "jsonrpc": "2.0",
            "id": self.test_count + 10,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        try:
            response = await self.send_message(request)

            if "error" in response:
                self.log(f"  ❌ FAIL: {response['error']}", "red")
                self.fail_count += 1
                return False

            if "result" in response:
                self.log("  ✅ PASS", "green")
                self.pass_count += 1
                return True
            else:
                self.log(f"  ❌ FAIL: No result in response", "red")
                self.fail_count += 1
                return False

        except Exception as e:
            self.log(f"  ❌ FAIL: {str(e)}", "red")
            self.fail_count += 1
            return False

    async def run_all_tests(self):
        """Run comprehensive tests of all tools"""
        try:
            # Start server
            if not await self.start_server():
                return False

            # Initialize connection
            await self.initialize_connection()

            # List tools
            tools = await self.list_tools()

            # Test individual tools
            self.log("Starting tool tests...")

            test_cases = [
                ("check_auspicious_date", {"date": "2024-01-01", "activity": "wedding", "culture": "chinese"}, "Check auspicious date for wedding"),
                ("find_good_dates", {"start_date": "2024-01-01", "end_date": "2024-01-31", "activity": "business_opening", "culture": "chinese", "limit": 5}, "Find good dates for business opening"),
                ("get_daily_fortune", {"date": "2024-01-01", "culture": "chinese"}, "Get daily fortune information"),
                ("check_zodiac_compatibility", {"date1": "1990-01-01", "date2": "1992-01-01", "culture": "chinese"}, "Check zodiac compatibility"),
                ("get_lunar_festivals", {"date": "2024-02-10", "culture": "chinese"}, "Get lunar festivals for date"),
                ("get_next_festival", {"date": "2024-01-01", "culture": "chinese"}, "Get next upcoming festival"),
                ("get_festival_details", {"festival_name": "Chinese New Year", "culture": "chinese"}, "Get festival details"),
                ("get_annual_festivals", {"year": 2024, "culture": "chinese"}, "Get annual festivals"),
                ("get_moon_phase", {"date": "2024-01-01", "location": "0,0"}, "Get moon phase information"),
                ("get_moon_calendar", {"month": 1, "year": 2024, "location": "0,0"}, "Get monthly moon calendar"),
                ("get_moon_influence", {"date": "2024-01-01", "activity": "planting"}, "Get moon influence on activity"),
                ("predict_moon_phases", {"start_date": "2024-01-01", "end_date": "2024-01-31"}, "Predict moon phases in range"),
                ("solar_to_lunar", {"solar_date": "2024-01-01", "culture": "chinese"}, "Convert solar to lunar date"),
                ("lunar_to_solar", {"lunar_date": "2024-01-01", "culture": "chinese"}, "Convert lunar to solar date"),
                ("get_zodiac_info", {"date": "1990-01-01", "culture": "chinese"}, "Get zodiac information"),
            ]

            for tool_name, arguments, description in test_cases:
                await self.test_tool(tool_name, arguments, description)
                await asyncio.sleep(0.1)  # Small delay between tests

            return True

        except Exception as e:
            self.log(f"Test execution failed: {str(e)}", "red")
            return False

        finally:
            self.stop_server()

    def print_summary(self):
        """Print test summary"""
        self.log("Test Summary:")
        self.log(f"Total tests: {self.test_count}")
        self.log(f"Passed: {self.pass_count}", "green")
        self.log(f"Failed: {self.fail_count}", "red")

        if self.fail_count == 0:
            self.log("All tests passed!", "green")
            return True
        else:
            self.log("Some tests failed!", "red")
            return False

async def main():
    tester = MCPTester()

    def signal_handler(sig, frame):
        tester.log("Test interrupted, cleaning up...", "yellow")
        tester.stop_server()
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        success = await tester.run_all_tests()
        all_passed = tester.print_summary()

        if success and all_passed:
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        tester.log(f"Unexpected error: {str(e)}", "red")
        tester.stop_server()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())