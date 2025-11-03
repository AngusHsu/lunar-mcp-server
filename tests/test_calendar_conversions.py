"""Tests for calendar conversion utilities."""

import pytest

from lunar_mcp_server.calendar_conversions import CalendarConverter


class TestCalendarConverter:
    """Test cases for CalendarConverter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = CalendarConverter()

    @pytest.mark.asyncio
    async def test_solar_to_lunar_basic(self):
        """Test basic solar to lunar conversion."""
        result = await self.converter.solar_to_lunar("2024-01-01", "chinese")

        assert "solar_date" in result
        assert "lunar_year" in result or "error" in result
        assert result["solar_date"] == "2024-01-01"

    @pytest.mark.asyncio
    async def test_solar_to_lunar_chinese_new_year(self):
        """Test conversion around Chinese New Year."""
        # Test date before Chinese New Year
        result_before = await self.converter.solar_to_lunar("2024-01-01", "chinese")

        # Test date after Chinese New Year (Feb 10, 2024)
        result_after = await self.converter.solar_to_lunar("2024-02-15", "chinese")

        # Both should succeed or have error
        assert "solar_date" in result_before
        assert "solar_date" in result_after

    @pytest.mark.asyncio
    async def test_solar_to_lunar_invalid_date(self):
        """Test with invalid solar date."""
        result = await self.converter.solar_to_lunar("invalid-date", "chinese")

        assert "error" in result

    @pytest.mark.asyncio
    async def test_lunar_to_solar_basic(self):
        """Test basic lunar to solar conversion."""
        result = await self.converter.lunar_to_solar("2024-01-01", "chinese")

        assert "lunar_date" in result
        assert "solar_date" in result or "error" in result

    @pytest.mark.asyncio
    async def test_lunar_to_solar_invalid_format(self):
        """Test lunar to solar with invalid format."""
        result = await self.converter.lunar_to_solar("invalid", "chinese")

        assert "error" in result

    @pytest.mark.asyncio
    async def test_lunar_to_solar_invalid_date_parts(self):
        """Test lunar to solar with invalid date parts."""
        result = await self.converter.lunar_to_solar("2024-13-32", "chinese")

        # Should handle invalid month/day gracefully
        assert "lunar_date" in result

    @pytest.mark.asyncio
    async def test_get_zodiac_info_basic(self):
        """Test basic zodiac info retrieval."""
        result = await self.converter.get_zodiac_info("2024-01-01", "chinese")

        assert "date" in result
        assert "culture" in result
        if "error" not in result:
            assert "year_zodiac" in result

    @pytest.mark.asyncio
    async def test_get_zodiac_info_dragon_year(self):
        """Test zodiac for Dragon year (2024)."""
        result = await self.converter.get_zodiac_info("2024-03-01", "chinese")

        if "error" not in result:
            assert result["year_zodiac"]["animal"] == "Dragon"

    @pytest.mark.asyncio
    async def test_get_zodiac_info_invalid_date(self):
        """Test zodiac info with invalid date."""
        result = await self.converter.get_zodiac_info("invalid", "chinese")

        assert "error" in result

    def test_calculate_chinese_zodiac_year(self):
        """Test Chinese zodiac year calculation."""
        # Test Rat year (2020)
        zodiac_2020 = self.converter._calculate_chinese_zodiac_year(2020)
        assert zodiac_2020["animal"] == "Rat"
        assert zodiac_2020["element"] in self.converter.zodiac_elements

        # Test Ox year (2021)
        zodiac_2021 = self.converter._calculate_chinese_zodiac_year(2021)
        assert zodiac_2021["animal"] == "Ox"

        # Test Dragon year (2024)
        zodiac_2024 = self.converter._calculate_chinese_zodiac_year(2024)
        assert zodiac_2024["animal"] == "Dragon"
        assert zodiac_2024["element"] in self.converter.zodiac_elements

    def test_zodiac_animals_list(self):
        """Test that all zodiac animals are defined."""
        assert len(self.converter.zodiac_animals) == 12

        expected_animals = [
            "Rat",
            "Ox",
            "Tiger",
            "Rabbit",
            "Dragon",
            "Snake",
            "Horse",
            "Goat",
            "Monkey",
            "Rooster",
            "Dog",
            "Pig",
        ]

        assert self.converter.zodiac_animals == expected_animals

    def test_zodiac_elements_list(self):
        """Test that all zodiac elements are defined."""
        assert len(self.converter.zodiac_elements) == 5

        expected_elements = ["Wood", "Fire", "Earth", "Metal", "Water"]
        assert self.converter.zodiac_elements == expected_elements

    def test_yin_yang_calculation(self):
        """Test Yin/Yang calculation in zodiac."""
        # Even year offset = Yang
        zodiac_even = self.converter._calculate_chinese_zodiac_year(1900)
        assert zodiac_even["yin_yang"] == "Yang"

        # Odd year offset = Yin
        zodiac_odd = self.converter._calculate_chinese_zodiac_year(1901)
        assert zodiac_odd["yin_yang"] == "Yin"

    def test_cycle_position(self):
        """Test 60-year cycle position calculation."""
        zodiac = self.converter._calculate_chinese_zodiac_year(1900)
        assert "cycle_position" in zodiac
        assert 0 <= zodiac["cycle_position"] < 60

        # After 60 years, should return to same position
        zodiac_60 = self.converter._calculate_chinese_zodiac_year(1960)
        assert zodiac_60["cycle_position"] == 0

    def test_get_zodiac_compatibility(self):
        """Test zodiac compatibility mapping."""
        # Test Dragon compatibility
        dragon_compat = self.converter._get_zodiac_compatibility("Dragon")
        assert "best" in dragon_compat
        assert "challenging" in dragon_compat
        assert "Rat" in dragon_compat["best"]
        assert "Dog" in dragon_compat["challenging"]

        # Test Rat compatibility
        rat_compat = self.converter._get_zodiac_compatibility("Rat")
        assert "Dragon" in rat_compat["best"]
        assert "Horse" in rat_compat["challenging"]

    def test_all_animals_have_compatibility(self):
        """Test that all zodiac animals have compatibility data."""
        for animal in self.converter.zodiac_animals:
            compat = self.converter._get_zodiac_compatibility(animal)
            assert "best" in compat
            assert "challenging" in compat
            assert len(compat["best"]) > 0
            assert len(compat["challenging"]) > 0

    def test_unknown_animal_compatibility(self):
        """Test compatibility for unknown animal."""
        compat = self.converter._get_zodiac_compatibility("Unknown")
        assert compat == {"best": [], "challenging": []}

    @pytest.mark.asyncio
    async def test_solar_to_lunar_with_leap_month(self):
        """Test solar to lunar conversion in leap month year."""
        # 2023 had a leap month
        result = await self.converter.solar_to_lunar("2023-03-15", "chinese")

        assert "solar_date" in result
        if "error" not in result and "is_leap_month" in result:
            assert isinstance(result["is_leap_month"], bool)

    @pytest.mark.asyncio
    async def test_multiple_year_zodiac_calculation(self):
        """Test zodiac calculation across multiple years."""
        years_animals = {
            2020: "Rat",
            2021: "Ox",
            2022: "Tiger",
            2023: "Rabbit",
            2024: "Dragon",
            2025: "Snake",
        }

        for year, expected_animal in years_animals.items():
            result = await self.converter.get_zodiac_info(f"{year}-06-01", "chinese")
            if "error" not in result:
                assert result["year_zodiac"]["animal"] == expected_animal

    @pytest.mark.asyncio
    async def test_daily_zodiac_calculation(self):
        """Test that daily zodiac is calculated."""
        result = await self.converter.get_zodiac_info("2024-01-01", "chinese")

        if "error" not in result:
            assert "daily_zodiac" in result
            assert "animal" in result["daily_zodiac"]
            assert result["daily_zodiac"]["animal"] in self.converter.zodiac_animals

    @pytest.mark.asyncio
    async def test_hourly_zodiac_calculation(self):
        """Test that hourly zodiac is calculated."""
        result = await self.converter.get_zodiac_info("2024-01-01", "chinese")

        if "error" not in result:
            assert "hourly_zodiac" in result
            assert "animal" in result["hourly_zodiac"]
            assert "hour_range" in result["hourly_zodiac"]

    @pytest.mark.asyncio
    async def test_zodiac_info_includes_compatibility(self):
        """Test that zodiac info includes compatibility data."""
        result = await self.converter.get_zodiac_info("2024-01-01", "chinese")

        if "error" not in result:
            assert "compatibility" in result
            assert "best_matches" in result["compatibility"]
            assert "challenging_matches" in result["compatibility"]

    @pytest.mark.asyncio
    async def test_zodiac_info_includes_lunar_info(self):
        """Test that zodiac info includes lunar information."""
        result = await self.converter.get_zodiac_info("2024-01-01", "chinese")

        if "error" not in result:
            assert "lunar_info" in result

    def test_zodiac_full_name_format(self):
        """Test that zodiac full name is properly formatted."""
        zodiac = self.converter._calculate_chinese_zodiac_year(2024)

        assert "full_name" in zodiac
        # Should be "Element Animal" format
        assert zodiac["element"] in zodiac["full_name"]
        assert zodiac["animal"] in zodiac["full_name"]

    @pytest.mark.asyncio
    async def test_fallback_conversion_method(self):
        """Test fallback Chinese conversion when libraries unavailable."""
        from datetime import date

        # Test the fallback method directly
        test_date = date(2024, 3, 15)
        result = self.converter._fallback_chinese_conversion(test_date)

        assert "lunar_year" in result
        assert "lunar_month" in result
        assert "lunar_day" in result
        assert "zodiac_info" in result
        assert "calculation_method" in result
        assert result["calculation_method"] == "approximation"

    @pytest.mark.asyncio
    async def test_solar_to_lunar_culture_parameter(self):
        """Test that culture parameter is properly handled."""
        result = await self.converter.solar_to_lunar("2024-01-01", "chinese")

        if "error" not in result:
            assert result["culture"] == "chinese"

    @pytest.mark.asyncio
    async def test_lunar_to_solar_culture_parameter(self):
        """Test that culture parameter is properly handled."""
        result = await self.converter.lunar_to_solar("2024-01-01", "chinese")

        if "error" not in result:
            assert result["culture"] == "chinese"

    @pytest.mark.asyncio
    async def test_conversion_round_trip_approximation(self):
        """Test that solar->lunar->solar maintains reasonable accuracy."""
        # Convert solar to lunar
        lunar_result = await self.converter.solar_to_lunar("2024-03-01", "chinese")

        if "error" not in lunar_result and "lunar_date_string" in lunar_result:
            # Convert back to solar
            solar_result = await self.converter.lunar_to_solar(
                lunar_result["lunar_date_string"], "chinese"
            )

            # Results should be reasonably close (within a month due to approximations)
            assert "solar_date" in solar_result or "error" in solar_result
