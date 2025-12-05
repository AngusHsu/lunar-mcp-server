"""Integration tests for MCP prompts and resources handlers."""

import json

import pytest
from mcp.types import (
    GetPromptRequest,
    ListPromptsRequest,
    ListResourcesRequest,
    ReadResourceRequest,
)

from lunar_mcp_server.server import LunarMCPServer


class TestServerPromptsAndResources:
    """Test cases for MCP prompts and resources handlers."""

    def setup_method(self):
        """Set up test fixtures."""
        self.server = LunarMCPServer()

    @pytest.mark.asyncio
    async def test_list_prompts_returns_5_prompts(self):
        """Test that list_prompts returns exactly 5 prompts with correct names."""
        handler = self.server.server.request_handlers[ListPromptsRequest]
        request = ListPromptsRequest(params={})
        result = await handler(request)
        prompts = result.root.prompts

        # Verify count
        assert len(prompts) == 5

        # Verify prompt names
        prompt_names = [p.name for p in prompts]
        expected_names = [
            "check_wedding_date",
            "calculate_bazi_chart",
            "find_auspicious_dates",
            "get_daily_almanac",
            "check_relationship_compatibility",
        ]
        assert sorted(prompt_names) == sorted(expected_names)

        # Verify each prompt has required fields
        for prompt in prompts:
            assert hasattr(prompt, "name")
            assert hasattr(prompt, "description")
            assert hasattr(prompt, "arguments")
            assert prompt.description is not None
            assert len(prompt.description) > 0

    @pytest.mark.asyncio
    async def test_get_prompt_check_wedding_date(self):
        """Test get_prompt for check_wedding_date with valid arguments."""
        handler = self.server.server.request_handlers[GetPromptRequest]
        request = GetPromptRequest(
            params={"name": "check_wedding_date", "arguments": {"date": "2024-05-20"}}
        )
        result = await handler(request)

        assert result.root.description is not None
        assert len(result.root.messages) == 1
        assert result.root.messages[0].role == "user"
        assert "2024-05-20" in result.root.messages[0].content.text
        assert "wedding" in result.root.messages[0].content.text.lower()

    @pytest.mark.asyncio
    async def test_get_prompt_calculate_bazi_chart(self):
        """Test get_prompt for calculate_bazi_chart with valid arguments."""
        handler = self.server.server.request_handlers[GetPromptRequest]
        request = GetPromptRequest(
            params={
                "name": "calculate_bazi_chart",
                "arguments": {
                    "birth_datetime": "1990-05-15 14:30",
                    "timezone_offset": "8",
                },
            }
        )
        result = await handler(request)

        assert result.root.description is not None
        assert len(result.root.messages) == 1
        assert result.root.messages[0].role == "user"
        assert "1990-05-15 14:30" in result.root.messages[0].content.text
        assert "BaZi" in result.root.messages[0].content.text

    @pytest.mark.asyncio
    async def test_get_prompt_find_auspicious_dates(self):
        """Test get_prompt for find_auspicious_dates with valid arguments."""
        handler = self.server.server.request_handlers[GetPromptRequest]
        request = GetPromptRequest(
            params={
                "name": "find_auspicious_dates",
                "arguments": {
                    "start_date": "2024-01-01",
                    "end_date": "2024-01-31",
                    "activity": "wedding",
                },
            }
        )
        result = await handler(request)

        assert result.root.description is not None
        assert len(result.root.messages) == 1
        assert result.root.messages[0].role == "user"
        assert "2024-01-01" in result.root.messages[0].content.text
        assert "2024-01-31" in result.root.messages[0].content.text
        assert "wedding" in result.root.messages[0].content.text

    @pytest.mark.asyncio
    async def test_get_prompt_get_daily_almanac(self):
        """Test get_prompt for get_daily_almanac with valid arguments."""
        handler = self.server.server.request_handlers[GetPromptRequest]
        request = GetPromptRequest(
            params={"name": "get_daily_almanac", "arguments": {"date": "2024-02-10"}}
        )
        result = await handler(request)

        assert result.root.description is not None
        assert len(result.root.messages) == 1
        assert result.root.messages[0].role == "user"
        assert "2024-02-10" in result.root.messages[0].content.text

    @pytest.mark.asyncio
    async def test_get_prompt_check_relationship_compatibility(self):
        """Test get_prompt for check_relationship_compatibility with valid arguments."""
        handler = self.server.server.request_handlers[GetPromptRequest]
        request = GetPromptRequest(
            params={
                "name": "check_relationship_compatibility",
                "arguments": {
                    "person1_datetime": "1990-05-15 14:30",
                    "person2_datetime": "1992-08-20 10:00",
                },
            }
        )
        result = await handler(request)

        assert result.root.description is not None
        assert len(result.root.messages) == 1
        assert result.root.messages[0].role == "user"
        assert "1990-05-15 14:30" in result.root.messages[0].content.text
        assert "1992-08-20 10:00" in result.root.messages[0].content.text

    @pytest.mark.asyncio
    async def test_get_prompt_missing_required_date(self):
        """Test get_prompt validation error for missing date in check_wedding_date."""
        handler = self.server.server.request_handlers[GetPromptRequest]
        request = GetPromptRequest(
            params={"name": "check_wedding_date", "arguments": {}}
        )

        with pytest.raises(ValueError) as exc_info:
            await handler(request)

        assert "Missing required argument: date" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_prompt_missing_required_birth_datetime(self):
        """Test get_prompt validation error for missing birth_datetime."""
        handler = self.server.server.request_handlers[GetPromptRequest]
        request = GetPromptRequest(
            params={"name": "calculate_bazi_chart", "arguments": {}}
        )

        with pytest.raises(ValueError) as exc_info:
            await handler(request)

        assert "Missing required argument: birth_datetime" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_prompt_missing_required_start_date(self):
        """Test get_prompt validation error for missing start_date."""
        handler = self.server.server.request_handlers[GetPromptRequest]
        request = GetPromptRequest(
            params={
                "name": "find_auspicious_dates",
                "arguments": {"end_date": "2024-01-31", "activity": "wedding"},
            }
        )

        with pytest.raises(ValueError) as exc_info:
            await handler(request)

        assert "Missing required argument: start_date" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_prompt_missing_required_end_date(self):
        """Test get_prompt validation error for missing end_date."""
        handler = self.server.server.request_handlers[GetPromptRequest]
        request = GetPromptRequest(
            params={
                "name": "find_auspicious_dates",
                "arguments": {"start_date": "2024-01-01", "activity": "wedding"},
            }
        )

        with pytest.raises(ValueError) as exc_info:
            await handler(request)

        assert "Missing required argument: end_date" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_prompt_missing_required_activity(self):
        """Test get_prompt validation error for missing activity."""
        handler = self.server.server.request_handlers[GetPromptRequest]
        request = GetPromptRequest(
            params={
                "name": "find_auspicious_dates",
                "arguments": {"start_date": "2024-01-01", "end_date": "2024-01-31"},
            }
        )

        with pytest.raises(ValueError) as exc_info:
            await handler(request)

        assert "Missing required argument: activity" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_prompt_missing_person1_datetime(self):
        """Test get_prompt validation error for missing person1_datetime."""
        handler = self.server.server.request_handlers[GetPromptRequest]
        request = GetPromptRequest(
            params={
                "name": "check_relationship_compatibility",
                "arguments": {"person2_datetime": "1992-08-20 10:00"},
            }
        )

        with pytest.raises(ValueError) as exc_info:
            await handler(request)

        assert "Missing required argument: person1_datetime" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_prompt_missing_person2_datetime(self):
        """Test get_prompt validation error for missing person2_datetime."""
        handler = self.server.server.request_handlers[GetPromptRequest]
        request = GetPromptRequest(
            params={
                "name": "check_relationship_compatibility",
                "arguments": {"person1_datetime": "1990-05-15 14:30"},
            }
        )

        with pytest.raises(ValueError) as exc_info:
            await handler(request)

        assert "Missing required argument: person2_datetime" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_list_resources_returns_5_resources(self):
        """Test that list_resources returns exactly 5 resources with correct URIs."""
        handler = self.server.server.request_handlers[ListResourcesRequest]
        request = ListResourcesRequest(params={})
        result = await handler(request)
        resources = result.root.resources

        # Verify count
        assert len(resources) == 5

        # Verify resource URIs
        resource_uris = [str(r.uri) for r in resources]
        expected_uris = [
            "lunar://zodiac/animals",
            "lunar://elements/five",
            "lunar://festivals/major",
            "lunar://stems-branches/heavenly",
            "lunar://stems-branches/earthly",
        ]
        assert sorted(resource_uris) == sorted(expected_uris)

        # Verify each resource has required fields
        for resource in resources:
            assert hasattr(resource, "uri")
            assert hasattr(resource, "name")
            assert hasattr(resource, "description")
            assert hasattr(resource, "mimeType")
            assert resource.mimeType == "application/json"
            assert len(resource.name) > 0
            assert len(resource.description) > 0

    @pytest.mark.asyncio
    async def test_read_resource_zodiac_animals(self):
        """Test read_resource for lunar://zodiac/animals URI."""
        handler = self.server.server.request_handlers[ReadResourceRequest]
        request = ReadResourceRequest(params={"uri": "lunar://zodiac/animals"})
        result = await handler(request)
        contents = result.root.contents

        assert len(contents) == 1
        content = contents[0]
        assert str(content.uri) == "lunar://zodiac/animals"
        assert content.mimeType == "text/plain"

        # Parse JSON content
        data = json.loads(content.text)
        assert "zodiac_animals" in data
        assert len(data["zodiac_animals"]) == 12
        assert data["zodiac_animals"][0]["animal"] == "Rat"
        assert data["zodiac_animals"][11]["animal"] == "Pig"

    @pytest.mark.asyncio
    async def test_read_resource_five_elements(self):
        """Test read_resource for lunar://elements/five URI."""
        handler = self.server.server.request_handlers[ReadResourceRequest]
        request = ReadResourceRequest(params={"uri": "lunar://elements/five"})
        result = await handler(request)
        contents = result.root.contents

        assert len(contents) == 1
        content = contents[0]
        assert str(content.uri) == "lunar://elements/five"
        assert content.mimeType == "text/plain"

        # Parse JSON content
        data = json.loads(content.text)
        assert "five_elements" in data
        assert len(data["five_elements"]) == 5
        element_names = [e["element"] for e in data["five_elements"]]
        assert "Wood" in element_names
        assert "Fire" in element_names
        assert "Earth" in element_names
        assert "Metal" in element_names
        assert "Water" in element_names

    @pytest.mark.asyncio
    async def test_read_resource_major_festivals(self):
        """Test read_resource for lunar://festivals/major URI."""
        handler = self.server.server.request_handlers[ReadResourceRequest]
        request = ReadResourceRequest(params={"uri": "lunar://festivals/major"})
        result = await handler(request)
        contents = result.root.contents

        assert len(contents) == 1
        content = contents[0]
        assert str(content.uri) == "lunar://festivals/major"
        assert content.mimeType == "text/plain"

        # Parse JSON content
        data = json.loads(content.text)
        assert "festivals" in data
        assert len(data["festivals"]) >= 5
        festival_names = [f["name"] for f in data["festivals"]]
        assert "Spring Festival" in festival_names
        assert "Mid-Autumn Festival" in festival_names

    @pytest.mark.asyncio
    async def test_read_resource_heavenly_stems(self):
        """Test read_resource for lunar://stems-branches/heavenly URI."""
        handler = self.server.server.request_handlers[ReadResourceRequest]
        request = ReadResourceRequest(params={"uri": "lunar://stems-branches/heavenly"})
        result = await handler(request)
        contents = result.root.contents

        assert len(contents) == 1
        content = contents[0]
        assert str(content.uri) == "lunar://stems-branches/heavenly"
        assert content.mimeType == "text/plain"

        # Parse JSON content
        data = json.loads(content.text)
        assert "heavenly_stems" in data
        assert len(data["heavenly_stems"]) == 10
        assert data["heavenly_stems"][0]["stem"] == "Jia"
        assert data["heavenly_stems"][9]["stem"] == "Gui"

    @pytest.mark.asyncio
    async def test_read_resource_earthly_branches(self):
        """Test read_resource for lunar://stems-branches/earthly URI."""
        handler = self.server.server.request_handlers[ReadResourceRequest]
        request = ReadResourceRequest(params={"uri": "lunar://stems-branches/earthly"})
        result = await handler(request)
        contents = result.root.contents

        assert len(contents) == 1
        content = contents[0]
        assert str(content.uri) == "lunar://stems-branches/earthly"
        assert content.mimeType == "text/plain"

        # Parse JSON content
        data = json.loads(content.text)
        assert "earthly_branches" in data
        assert len(data["earthly_branches"]) == 12
        assert data["earthly_branches"][0]["branch"] == "Zi"
        assert data["earthly_branches"][11]["branch"] == "Hai"

    @pytest.mark.asyncio
    async def test_read_resource_invalid_uri(self):
        """Test read_resource error for invalid URI."""
        handler = self.server.server.request_handlers[ReadResourceRequest]
        request = ReadResourceRequest(params={"uri": "lunar://invalid/uri"})

        with pytest.raises(ValueError) as exc_info:
            await handler(request)

        assert "Unknown resource" in str(exc_info.value)
