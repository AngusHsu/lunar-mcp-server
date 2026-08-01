"""End-to-end MCP client coverage over the production STDIO transport."""

import sys
from pathlib import Path

import pytest
from mcp import types
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

EXPECTED_TOOL_CALLS: dict[str, dict[str, object]] = {
    "check_auspicious_date": {"date": "2024-01-01", "activity": "wedding"},
    "find_good_dates": {
        "start_date": "2024-01-01",
        "end_date": "2024-01-03",
        "activity": "wedding",
        "limit": 1,
    },
    "get_daily_fortune": {"date": "2024-01-01"},
    "check_zodiac_compatibility": {
        "date1": "1990-01-01",
        "date2": "1992-01-01",
    },
    "get_lunar_festivals": {"date": "2024-02-10"},
    "get_next_festival": {"date": "2024-01-01"},
    "get_festival_details": {"festival_name": "Spring Festival"},
    "get_annual_festivals": {"year": 2024},
    "get_moon_phase": {"date": "2024-01-01", "location": "0,0"},
    "get_moon_calendar": {"month": 1, "year": 2024, "location": "0,0"},
    "get_moon_influence": {"date": "2024-01-01", "activity": "planting"},
    "predict_moon_phases": {
        "start_date": "2024-01-01",
        "end_date": "2024-01-07",
    },
    "solar_to_lunar": {"solar_date": "2024-01-01"},
    "lunar_to_solar": {"lunar_date": "2024-01-01"},
    "get_zodiac_info": {"date": "1990-01-01"},
    "batch_check_dates": {
        "dates": ["2024-01-01", "2024-01-02"],
        "activity": "wedding",
    },
    "compare_dates": {
        "dates": ["2024-01-01", "2024-01-02"],
        "activity": "wedding",
    },
    "get_lucky_hours": {
        "date": "2024-01-01",
        "activity": "signing_contract",
    },
    "calculate_bazi": {
        "birth_datetime": "1990-01-01 12:00",
        "timezone_offset": 8,
    },
    "calculate_bazi_compatibility": {
        "birth_datetime1": "1990-01-01 12:00",
        "birth_datetime2": "1992-02-02 08:00",
        "timezone_offset": 8,
    },
}

EXPECTED_PROMPTS: dict[str, dict[str, str]] = {
    "check_wedding_date": {"date": "2024-01-01"},
    "calculate_bazi_chart": {"birth_datetime": "1990-01-01 12:00"},
    "find_auspicious_dates": {
        "start_date": "2024-01-01",
        "end_date": "2024-01-03",
        "activity": "wedding",
    },
    "get_daily_almanac": {"date": "2024-01-01"},
    "check_relationship_compatibility": {
        "person1_datetime": "1990-01-01 12:00",
        "person2_datetime": "1992-02-02 08:00",
    },
}

EXPECTED_RESOURCES = {
    "lunar://zodiac/animals",
    "lunar://elements/five",
    "lunar://festivals/major",
    "lunar://stems-branches/heavenly",
    "lunar://stems-branches/earthly",
}


def stdio_parameters() -> StdioServerParameters:
    """Launch the package entry point with the active test interpreter."""
    return StdioServerParameters(
        command=sys.executable,
        args=["-c", "from lunar_mcp_server.server import main; main()"],
        cwd=str(Path(__file__).resolve().parents[1]),
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_complete_stdio_surface_and_clean_shutdown() -> None:
    """Discover and successfully exercise the complete production surface."""
    async with stdio_client(stdio_parameters()) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            initialization = await session.initialize()
            assert initialization.protocolVersion == "2025-11-25"
            assert initialization.serverInfo.name == "lunar-mcp-server"

            tools = (await session.list_tools()).tools
            assert {tool.name for tool in tools} == set(EXPECTED_TOOL_CALLS)
            assert len(tools) == 20
            for tool_name, arguments in EXPECTED_TOOL_CALLS.items():
                result = await session.call_tool(tool_name, arguments)
                assert not result.isError, f"{tool_name}: {result.content}"
                assert result.content

            prompts = (await session.list_prompts()).prompts
            assert {prompt.name for prompt in prompts} == set(EXPECTED_PROMPTS)
            assert len(prompts) == 5
            for prompt_name, arguments in EXPECTED_PROMPTS.items():
                result = await session.get_prompt(prompt_name, arguments)
                assert result.messages

            resources = (await session.list_resources()).resources
            resource_uris = {str(resource.uri) for resource in resources}
            assert resource_uris == EXPECTED_RESOURCES
            assert len(resources) == 5
            for resource_uri in EXPECTED_RESOURCES:
                result = await session.read_resource(resource_uri)
                assert len(result.contents) == 1
                assert result.contents[0].mimeType == "application/json"

            invalid = await session.call_tool("invalid_tool_name", {})
            assert "Unknown tool: invalid_tool_name" in invalid.content[0].text

            missing = await session.call_tool("check_auspicious_date", {})
            assert missing.isError
            assert "required property" in missing.content[0].text


@pytest.mark.integration
@pytest.mark.asyncio
async def test_legacy_2024_protocol_initialization(monkeypatch) -> None:
    """Retain initialization compatibility with existing 2024-11-05 clients."""
    monkeypatch.setattr(types, "LATEST_PROTOCOL_VERSION", "2024-11-05")

    async with stdio_client(stdio_parameters()) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            initialization = await session.initialize()
            assert initialization.protocolVersion == "2024-11-05"
            assert len((await session.list_tools()).tools) == 20
