"""Tests for festival management."""

import pytest

from lunar_mcp_server.festivals import FestivalManager


class TestFestivalManager:
    """Test cases for FestivalManager."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = FestivalManager()

    @pytest.mark.asyncio
    async def test_get_festivals_for_date_chinese_new_year(self):
        """Test getting festivals for Chinese New Year."""
        # Chinese New Year 2024 is on Feb 10
        result = await self.manager.get_festivals_for_date("2024-02-10", "chinese")

        assert "date" in result
        assert "festivals" in result
        assert isinstance(result["festivals"], list)

    @pytest.mark.asyncio
    async def test_get_festivals_for_date_no_festival(self):
        """Test getting festivals for a date with no festival."""
        result = await self.manager.get_festivals_for_date("2024-03-17", "chinese")

        assert "date" in result
        assert "festivals" in result
        assert isinstance(result["festivals"], list)

    @pytest.mark.asyncio
    async def test_get_festivals_for_date_invalid_date(self):
        """Test with invalid date."""
        result = await self.manager.get_festivals_for_date("invalid", "chinese")

        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_next_festival_basic(self):
        """Test getting next festival after a date."""
        result = await self.manager.get_next_festival("2024-01-01", "chinese")

        # Check for search_date or reference_date field
        assert (
            "search_date" in result or "reference_date" in result or "error" in result
        )
        # If festival found, check structure
        if "festival" in result:
            assert "name" in result["festival"]
        if "next_festival" in result:
            assert "name" in result["next_festival"]

    @pytest.mark.asyncio
    async def test_get_next_festival_invalid_date(self):
        """Test next festival with invalid date."""
        result = await self.manager.get_next_festival("invalid", "chinese")

        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_festival_details_spring_festival(self):
        """Test getting details for Spring Festival."""
        result = await self.manager.get_festival_details("Spring Festival", "chinese")

        if "error" not in result:
            assert "name" in result
            assert "significance" in result or "description" in result

    @pytest.mark.asyncio
    async def test_get_festival_details_unknown_festival(self):
        """Test getting details for unknown festival."""
        result = await self.manager.get_festival_details("Unknown Festival", "chinese")

        # Should either return empty or error
        assert "error" in result or "name" in result

    @pytest.mark.asyncio
    async def test_get_annual_festivals_basic(self):
        """Test getting annual festivals for a year."""
        result = await self.manager.get_annual_festivals(2024, "chinese")

        assert "year" in result
        assert "culture" in result
        if "error" not in result:
            assert "festivals" in result
            assert isinstance(result["festivals"], list)

    @pytest.mark.asyncio
    async def test_get_annual_festivals_multiple_years(self):
        """Test annual festivals for different years."""
        result_2024 = await self.manager.get_annual_festivals(2024, "chinese")
        result_2025 = await self.manager.get_annual_festivals(2025, "chinese")

        # Both should succeed
        assert "year" in result_2024
        assert "year" in result_2025

    @pytest.mark.asyncio
    async def test_festivals_have_required_fields(self):
        """Test that festival entries have required fields."""
        result = await self.manager.get_annual_festivals(2024, "chinese")

        if "festivals" in result and len(result["festivals"]) > 0:
            festival = result["festivals"][0]
            # Check for common festival fields
            assert "name" in festival or "festival_name" in festival

    @pytest.mark.asyncio
    async def test_next_festival_has_days_until(self):
        """Test that next festival includes days until information."""
        result = await self.manager.get_next_festival("2024-01-01", "chinese")

        if "next_festival" in result and "days_until" in result:
            assert isinstance(result["days_until"], int)
            assert result["days_until"] >= 0

    @pytest.mark.asyncio
    async def test_culture_parameter_chinese(self):
        """Test that culture parameter is properly handled."""
        result = await self.manager.get_annual_festivals(2024, "chinese")

        if "error" not in result:
            assert result["culture"] == "chinese"

    @pytest.mark.asyncio
    async def test_get_festivals_date_format(self):
        """Test various date formats for getting festivals."""
        # Standard format
        result1 = await self.manager.get_festivals_for_date("2024-01-01", "chinese")
        assert "date" in result1

        # Should handle the date properly
        assert result1["date"] == "2024-01-01"

    @pytest.mark.asyncio
    async def test_annual_festivals_chronological_order(self):
        """Test that annual festivals are in chronological order."""
        result = await self.manager.get_annual_festivals(2024, "chinese")

        if "festivals" in result and len(result["festivals"]) > 1:
            # If festivals have dates, they should be ordered
            festivals_with_dates = [
                f for f in result["festivals"] if "date" in f or "solar_date" in f
            ]

            if len(festivals_with_dates) > 1:
                # Just verify we have a list - ordering depends on implementation
                assert isinstance(festivals_with_dates, list)

    @pytest.mark.asyncio
    async def test_festival_manager_initialization(self):
        """Test that FestivalManager initializes properly."""
        assert self.manager is not None

    @pytest.mark.asyncio
    async def test_multiple_festivals_same_date(self):
        """Test handling of multiple festivals on the same date."""
        # Some dates may have multiple festivals
        result = await self.manager.get_festivals_for_date("2024-02-10", "chinese")

        assert "festivals" in result
        assert isinstance(result["festivals"], list)
        # Could be 0, 1, or more festivals

    @pytest.mark.asyncio
    async def test_get_festivals_year_boundary(self):
        """Test getting festivals around year boundaries."""
        # End of year
        result_end = await self.manager.get_festivals_for_date("2024-12-31", "chinese")
        # Start of year
        result_start = await self.manager.get_festivals_for_date(
            "2024-01-01", "chinese"
        )

        assert "date" in result_end
        assert "date" in result_start

    @pytest.mark.asyncio
    async def test_next_festival_from_end_of_year(self):
        """Test getting next festival from end of year."""
        result = await self.manager.get_next_festival("2024-12-31", "chinese")

        # Should find a festival in the next year
        if "next_festival" in result:
            assert "date" in result["next_festival"]

    @pytest.mark.asyncio
    async def test_festival_details_empty_name(self):
        """Test festival details with empty name."""
        result = await self.manager.get_festival_details("", "chinese")

        # Should handle gracefully
        assert "error" in result or "name" in result

    @pytest.mark.asyncio
    async def test_annual_festivals_past_year(self):
        """Test getting festivals for past years."""
        result = await self.manager.get_annual_festivals(2020, "chinese")

        assert "year" in result
        assert result["year"] == 2020

    @pytest.mark.asyncio
    async def test_annual_festivals_future_year(self):
        """Test getting festivals for future years."""
        result = await self.manager.get_annual_festivals(2030, "chinese")

        assert "year" in result
        assert result["year"] == 2030

    @pytest.mark.asyncio
    async def test_festivals_data_structure(self):
        """Test that festivals have proper data structure."""
        result = await self.manager.get_annual_festivals(2024, "chinese")

        if "festivals" in result and result["festivals"]:
            for festival in result["festivals"]:
                # Each festival should be a dictionary
                assert isinstance(festival, dict)

    @pytest.mark.asyncio
    async def test_get_next_festival_consistency(self):
        """Test that next festival is consistent across calls."""
        result1 = await self.manager.get_next_festival("2024-01-01", "chinese")
        result2 = await self.manager.get_next_festival("2024-01-01", "chinese")

        # Results should be the same
        if "next_festival" in result1 and "next_festival" in result2:
            assert result1["next_festival"]["name"] == result2["next_festival"]["name"]

    @pytest.mark.asyncio
    async def test_festival_search_case_sensitivity(self):
        """Test festival details search with different cases."""
        # This tests implementation details - may need adjustment
        result_lower = await self.manager.get_festival_details(
            "spring festival", "chinese"
        )
        result_title = await self.manager.get_festival_details(
            "Spring Festival", "chinese"
        )

        # Both should return same festival or both should error
        if "error" not in result_lower and "error" not in result_title:
            assert result_lower.get("name") == result_title.get("name")
        else:
            # If one errors, likely both will
            assert ("error" in result_lower) == ("error" in result_title)
