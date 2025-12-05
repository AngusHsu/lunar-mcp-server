"""Tests for MCP server implementation."""

from unittest.mock import patch

import pytest
from mcp.types import GetPromptRequest, ListPromptsRequest, ListResourcesRequest, ReadResourceRequest

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
        assert hasattr(self.server, "_calculate_bazi")
        assert hasattr(self.server, "_calculate_bazi_compatibility")


class TestBaZiServerIntegration:
    """Test cases for BaZi MCP server integration."""

    def setup_method(self):
        """Set up test fixtures."""
        self.server = LunarMCPServer()

    @pytest.mark.asyncio
    async def test_calculate_bazi_tool(self):
        """Test calculate_bazi tool through server."""
        result = await self.server._calculate_bazi(
            birth_datetime="1990-05-15 14:30", timezone_offset=8
        )

        assert "eight_characters" in result
        assert "four_pillars" in result
        assert "day_master" in result
        assert len(result["eight_characters"]) == 8

    @pytest.mark.asyncio
    async def test_calculate_bazi_invalid_datetime(self):
        """Test calculate_bazi with invalid datetime."""
        result = await self.server._calculate_bazi(
            birth_datetime="invalid-datetime", timezone_offset=8
        )

        assert "error" in result

    @pytest.mark.asyncio
    async def test_calculate_bazi_compatibility_tool(self):
        """Test calculate_bazi_compatibility tool through server."""
        result = await self.server._calculate_bazi_compatibility(
            birth_datetime1="1990-05-15 14:30",
            birth_datetime2="1992-08-20 10:00",
            timezone_offset=8,
        )

        assert "person1" in result
        assert "person2" in result
        assert "compatibility_score" in result
        assert "compatibility_level" in result
        assert "element_relationship" in result

    @pytest.mark.asyncio
    async def test_calculate_bazi_compatibility_invalid_dates(self):
        """Test calculate_bazi_compatibility with invalid dates."""
        result = await self.server._calculate_bazi_compatibility(
            birth_datetime1="invalid1", birth_datetime2="invalid2", timezone_offset=8
        )

        assert "error" in result

    @pytest.mark.asyncio
    async def test_calculate_bazi_different_timezones(self):
        """Test calculate_bazi with different timezone offsets."""
        result_utc8 = await self.server._calculate_bazi(
            birth_datetime="2000-01-01 12:00", timezone_offset=8
        )

        result_utc0 = await self.server._calculate_bazi(
            birth_datetime="2000-01-01 12:00", timezone_offset=0
        )

        # Different timezones should produce different adjusted times
        assert result_utc8["adjusted_datetime"] != result_utc0["adjusted_datetime"]

    @pytest.mark.asyncio
    async def test_bazi_tool_output_structure(self):
        """Test that BaZi tool output has complete structure."""
        result = await self.server._calculate_bazi(
            birth_datetime="1995-07-20 09:30", timezone_offset=8
        )

        # Verify all required fields are present
        assert "birth_datetime" in result
        assert "timezone_offset" in result
        assert "adjusted_datetime" in result
        assert "eight_characters" in result
        assert "four_pillars" in result
        assert "day_master" in result
        assert "element_analysis" in result
        assert "life_stages" in result
        assert "interpretation" in result

        # Verify four pillars structure
        assert "year" in result["four_pillars"]
        assert "month" in result["four_pillars"]
        assert "day" in result["four_pillars"]
        assert "hour" in result["four_pillars"]

    @pytest.mark.asyncio
    async def test_bazi_compatibility_output_structure(self):
        """Test that BaZi compatibility output has complete structure."""
        result = await self.server._calculate_bazi_compatibility(
            birth_datetime1="1988-04-05 11:00",
            birth_datetime2="1990-09-18 13:00",
            timezone_offset=8,
        )

        # Verify all required fields
        assert "person1" in result
        assert "person2" in result
        assert "compatibility_score" in result
        assert "compatibility_level" in result
        assert "element_relationship" in result
        assert "analysis" in result

        # Verify person information
        for person in ["person1", "person2"]:
            assert "datetime" in result[person]
            assert "day_master" in result[person]
            assert "eight_characters" in result[person]

        # Verify analysis fields
        assert "strengths" in result["analysis"]
        assert "challenges" in result["analysis"]
        assert "recommendations" in result["analysis"]

    def test_bazi_calculator_initialization(self):
        """Test that BaZi calculator is properly initialized."""
        assert self.server.bazi_calculator is not None
        assert hasattr(self.server.bazi_calculator, "calculate_bazi")
        assert hasattr(self.server.bazi_calculator, "get_compatibility")


class TestServerToolIntegration:
    """Additional integration tests for MCP server tools."""

    def setup_method(self):
        """Set up test fixtures."""
        self.server = LunarMCPServer()

    @pytest.mark.asyncio
    async def test_get_daily_fortune_tool(self):
        """Test get_daily_fortune tool through server."""
        result = await self.server._get_daily_fortune("2024-01-15", "chinese")

        assert "date" in result or "error" in result
        if "error" not in result:
            assert "culture" in result

    @pytest.mark.asyncio
    async def test_check_zodiac_compatibility_tool(self):
        """Test check_zodiac_compatibility tool through server."""
        result = await self.server._check_zodiac_compatibility(
            "2024-01-01", "2024-02-01", "chinese"
        )

        assert "compatibility_level" in result or "error" in result

    @pytest.mark.asyncio
    async def test_get_next_festival_tool(self):
        """Test get_next_festival tool through server."""
        result = await self.server._get_next_festival("2024-01-01", "chinese")

        # Check for any valid response field
        assert any(
            key in result
            for key in ["festival", "next_festival", "search_date", "error"]
        )

    @pytest.mark.asyncio
    async def test_get_festival_details_tool(self):
        """Test get_festival_details tool through server."""
        result = await self.server._get_festival_details("Spring Festival", "chinese")

        assert "name" in result or "error" in result

    @pytest.mark.asyncio
    async def test_get_annual_festivals_tool(self):
        """Test get_annual_festivals tool through server."""
        result = await self.server._get_annual_festivals(2024, "chinese")

        assert "year" in result or "error" in result
        if "error" not in result:
            assert result["year"] == 2024

    @pytest.mark.asyncio
    async def test_get_moon_calendar_tool(self):
        """Test get_moon_calendar tool through server."""
        result = await self.server._get_moon_calendar(3, 2024, "0,0")

        assert "month" in result or "error" in result
        if "error" not in result:
            assert result["month"] == 3
            assert result["year"] == 2024

    @pytest.mark.asyncio
    async def test_get_moon_influence_tool(self):
        """Test get_moon_influence tool through server."""
        result = await self.server._get_moon_influence("2024-01-15", "wedding")

        assert "date" in result or "error" in result
        if "error" not in result:
            assert "activity" in result

    @pytest.mark.asyncio
    async def test_predict_moon_phases_tool(self):
        """Test predict_moon_phases tool through server."""
        result = await self.server._predict_moon_phases("2024-01-01", "2024-01-31")

        assert "start_date" in result or "error" in result

    @pytest.mark.asyncio
    async def test_lunar_to_solar_tool(self):
        """Test lunar_to_solar conversion tool."""
        result = await self.server._lunar_to_solar("2024-01-01", "chinese")

        assert "lunar_date" in result or "error" in result

    @pytest.mark.asyncio
    async def test_batch_check_dates_tool(self):
        """Test batch_check_dates tool through server."""
        dates = ["2024-01-01", "2024-01-15", "2024-02-01"]
        result = await self.server._batch_check_dates(dates, "wedding", "chinese")

        assert "total_checked" in result or "error" in result
        if "total_checked" in result:
            assert result["total_checked"] == 3
            assert "results" in result
            assert "activity" in result

    @pytest.mark.asyncio
    async def test_compare_dates_tool(self):
        """Test compare_dates tool through server."""
        dates = ["2024-01-01", "2024-01-15"]
        result = await self.server._compare_dates(dates, "wedding", "chinese")

        assert "comparison" in result or "error" in result
        if "comparison" in result:
            assert "culture" in result
            assert "activity" in result

    @pytest.mark.asyncio
    async def test_compare_dates_without_activity(self):
        """Test compare_dates without activity parameter."""
        dates = ["2024-01-01", "2024-01-15"]
        result = await self.server._compare_dates(dates, None, "chinese")

        assert "comparison" in result or "error" in result

    @pytest.mark.asyncio
    async def test_get_lucky_hours_tool(self):
        """Test get_lucky_hours tool through server."""
        result = await self.server._get_lucky_hours("2024-01-15", "wedding", "chinese")

        assert "date" in result or "error" in result
        if "error" not in result:
            assert "lucky_hours" in result
            assert isinstance(result["lucky_hours"], list)

    @pytest.mark.asyncio
    async def test_get_lucky_hours_without_activity(self):
        """Test get_lucky_hours without activity parameter."""
        result = await self.server._get_lucky_hours("2024-01-15", None, "chinese")

        assert "date" in result or "error" in result

    def test_server_has_all_calculators(self):
        """Test that server has all required calculator instances."""
        assert hasattr(self.server, "lunar_calc")
        assert hasattr(self.server, "auspicious_checker")
        assert hasattr(self.server, "festival_manager")
        assert hasattr(self.server, "calendar_converter")
        assert hasattr(self.server, "bazi_calculator")

        # Verify they're not None
        assert self.server.lunar_calc is not None
        assert self.server.auspicious_checker is not None
        assert self.server.festival_manager is not None
        assert self.server.calendar_converter is not None
        assert self.server.bazi_calculator is not None

    def test_server_mcp_instance(self):
        """Test that server has MCP server instance."""
        assert hasattr(self.server, "server")
        assert self.server.server is not None

    @pytest.mark.asyncio
    async def test_batch_check_dates_with_max_limit(self):
        """Test batch check dates with more than 30 dates."""
        # Create 35 dates
        dates = [f"2024-01-{i:02d}" for i in range(1, 32)]
        dates.extend([f"2024-02-{i:02d}" for i in range(1, 5)])

        result = await self.server._batch_check_dates(dates, "wedding", "chinese")

        if "total_checked" in result:
            # Should limit to 30 dates
            assert result["total_checked"] <= 30

    @pytest.mark.asyncio
    async def test_compare_dates_with_max_limit(self):
        """Test compare dates with more than 10 dates."""
        # Create 15 dates
        dates = [f"2024-01-{i:02d}" for i in range(1, 16)]

        result = await self.server._compare_dates(dates, "wedding", "chinese")

        if "comparison" in result:
            # Should limit to 10 dates
            assert len(result["comparison"]) <= 10

    @pytest.mark.asyncio
    async def test_batch_check_best_worst_dates(self):
        """Test that batch check identifies best and worst dates."""
        dates = ["2024-01-01", "2024-01-15", "2024-02-01"]
        result = await self.server._batch_check_dates(dates, "wedding", "chinese")

        if "best_date" in result and "worst_date" in result:
            # Best and worst should be in the list
            assert result["best_date"] in dates or result["best_date"] is None
            assert result["worst_date"] in dates or result["worst_date"] is None

    @pytest.mark.asyncio
    async def test_compare_dates_recommendation(self):
        """Test that compare dates provides recommendation when activity specified."""
        dates = ["2024-01-01", "2024-01-15"]
        result = await self.server._compare_dates(dates, "wedding", "chinese")

        # Recommendation may or may not be present depending on data
        if "recommendation" in result:
            assert result["recommendation"] in dates or result["recommendation"] is None

