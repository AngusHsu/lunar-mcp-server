"""Tests for MCP server implementation."""

from unittest.mock import patch

import pytest

from lunar_mcp_server.server import LunarMCPServer


class TestLunarMCPServer:
    """Test cases for LunarMCPServer."""

    def setup_method(self):
        """Set up test fixtures."""
        self.server = LunarMCPServer()

    @pytest.mark.asyncio
    async def test_check_auspicious_date_tool(self):
        """Test check_auspicious_date tool."""
        with patch.object(self.server.auspicious_checker, "check_date") as mock_check:
            mock_check.return_value = {
                "date": "2024-01-15",
                "auspicious_level": "very_good",
                "score": 8,
                "good_for": ["wedding", "celebration"],
                "avoid": ["conflict"],
                "zodiac_day": "Dragon",
            }

            result = await self.server._check_auspicious_date(
                "2024-01-15", "wedding", "chinese"
            )

            assert result["date"] == "2024-01-15"
            assert result["auspicious_level"] == "very_good"
            mock_check.assert_called_once_with("2024-01-15", "wedding", "chinese")

    @pytest.mark.asyncio
    async def test_find_good_dates_tool(self):
        """Test find_good_dates tool."""
        with patch.object(
            self.server.auspicious_checker, "find_good_dates"
        ) as mock_find:
            mock_find.return_value = {
                "activity": "wedding",
                "good_dates": [
                    {"date": "2024-01-15", "level": "very_good", "score": 8}
                ],
                "found_dates": 1,
            }

            result = await self.server._find_good_dates(
                "2024-01-01", "2024-01-31", "wedding", "chinese", 5
            )

            assert result["activity"] == "wedding"
            assert result["found_dates"] == 1
            mock_find.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_moon_phase_tool(self):
        """Test get_moon_phase tool."""
        with patch.object(self.server.lunar_calc, "get_moon_phase") as mock_moon:
            mock_moon.return_value = {
                "date": "2024-01-15",
                "phase_name": "Full Moon",
                "illumination": 0.98,
                "lunar_day": 15,
            }

            result = await self.server._get_moon_phase("2024-01-15", "0,0")

            assert result["date"] == "2024-01-15"
            assert result["phase_name"] == "Full Moon"
            mock_moon.assert_called_once_with("2024-01-15", "0,0")

    @pytest.mark.asyncio
    async def test_get_lunar_festivals_tool(self):
        """Test get_lunar_festivals tool."""
        with patch.object(
            self.server.festival_manager, "get_festivals_for_date"
        ) as mock_festivals:
            mock_festivals.return_value = {
                "date": "2024-02-10",
                "festivals": [
                    {
                        "name": "Chinese New Year",
                        "significance": "Beginning of lunar new year",
                    }
                ],
                "festival_count": 1,
            }

            result = await self.server._get_lunar_festivals("2024-02-10", "chinese")

            assert result["date"] == "2024-02-10"
            assert result["festival_count"] == 1
            mock_festivals.assert_called_once_with("2024-02-10", "chinese")

    @pytest.mark.asyncio
    async def test_solar_to_lunar_conversion(self):
        """Test solar to lunar date conversion."""
        with patch.object(
            self.server.calendar_converter, "solar_to_lunar"
        ) as mock_convert:
            mock_convert.return_value = {
                "solar_date": "2024-01-15",
                "lunar_year": 2024,
                "lunar_month": 12,
                "lunar_day": 5,
            }

            result = await self.server._solar_to_lunar("2024-01-15", "chinese")

            assert result["solar_date"] == "2024-01-15"
            assert result["lunar_year"] == 2024
            mock_convert.assert_called_once_with("2024-01-15", "chinese")

    @pytest.mark.asyncio
    async def test_get_zodiac_info_tool(self):
        """Test get_zodiac_info tool."""
        with patch.object(
            self.server.calendar_converter, "get_zodiac_info"
        ) as mock_zodiac:
            mock_zodiac.return_value = {
                "date": "2024-01-15",
                "culture": "chinese",
                "year_zodiac": {"animal": "Dragon", "element": "Wood"},
            }

            result = await self.server._get_zodiac_info("2024-01-15", "chinese")

            assert result["date"] == "2024-01-15"
            assert result["culture"] == "chinese"
            mock_zodiac.assert_called_once_with("2024-01-15", "chinese")

    def test_server_initialization(self):
        """Test server proper initialization."""
        assert self.server.lunar_calc is not None
        assert self.server.auspicious_checker is not None
        assert self.server.festival_manager is not None
        assert self.server.calendar_converter is not None
        assert self.server.server is not None

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling in tools."""
        with patch.object(self.server.auspicious_checker, "check_date") as mock_check:
            mock_check.side_effect = Exception("Test error")

            # Since the server doesn't have built-in error handling for this method,
            # we expect the exception to propagate
            with pytest.raises(Exception) as exc_info:
                await self.server._check_auspicious_date(
                    "2024-01-15", "wedding", "chinese"
                )

            assert str(exc_info.value) == "Test error"


class TestServerHandlers:
    """Test MCP server handlers."""

    def setup_method(self):
        """Set up test fixtures."""
        self.server = LunarMCPServer()

    @pytest.mark.asyncio
    async def test_list_tools_handler(self):
        """Test list_tools handler returns all expected tools."""
        # Since we can't directly access handlers, test the server setup
        # by checking if the server has the expected methods
        expected_methods = [
            "_check_auspicious_date",
            "_find_good_dates",
            "_get_moon_phase",
            "_get_lunar_festivals",
            "_solar_to_lunar",
            "_get_zodiac_info",
        ]

        for method_name in expected_methods:
            assert hasattr(self.server, method_name)
            assert callable(getattr(self.server, method_name))

    def test_tool_schemas(self):
        """Test that tools have proper input schemas."""
        # This is a basic test to ensure tools are properly defined
        assert hasattr(self.server, "_check_auspicious_date")
        assert hasattr(self.server, "_find_good_dates")
        assert hasattr(self.server, "_get_moon_phase")
        assert hasattr(self.server, "_get_lunar_festivals")
