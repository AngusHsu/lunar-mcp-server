"""Tests for auspicious dates module."""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch

from lunar_mcp_server.auspicious_dates import AuspiciousDateChecker


class TestAuspiciousDateChecker:
    """Test cases for AuspiciousDateChecker."""

    def setup_method(self):
        """Set up test fixtures."""
        self.checker = AuspiciousDateChecker()

    def test_chinese_calendar_info(self):
        """Test Chinese calendar information calculation."""
        test_date = datetime(2024, 1, 15)
        info = self.checker._get_chinese_calendar_info(test_date)

        assert "heavenly_stem" in info
        assert "earthly_branch" in info
        assert "lunar_mansion" in info
        assert "five_element" in info
        assert "zodiac_year" in info
        assert "zodiac_day" in info
        assert "sexagenary_day" in info

        # Check that values are from valid sets
        assert info["heavenly_stem"] in self.checker.chinese_rules["heavenly_stems"]
        assert info["earthly_branch"] in self.checker.chinese_rules["earthly_branches"]
        assert info["five_element"] in self.checker.chinese_rules["five_elements"]
        assert info["zodiac_year"] in self.checker.chinese_rules["zodiac_animals"]
        assert info["zodiac_day"] in self.checker.chinese_rules["zodiac_animals"]

    def test_calculate_auspiciousness(self):
        """Test auspiciousness calculation."""
        test_date = datetime(2024, 1, 15)
        result = self.checker._calculate_auspiciousness(test_date, "wedding", "chinese")

        assert "score" in result
        assert "level" in result
        assert "chinese_info" in result
        assert "factors" in result

        # Score should be between 0 and 10
        assert 0 <= result["score"] <= 10

        # Level should be valid
        valid_levels = ["very_good", "good", "neutral", "poor", "very_poor"]
        assert result["level"] in valid_levels

    @pytest.mark.asyncio
    async def test_check_date(self):
        """Test checking auspicious date."""
        with patch.object(self.checker.lunar_calc, 'get_moon_phase') as mock_moon:
            mock_moon.return_value = {
                "phase_name": "Full Moon",
                "lunar_day": 15,
                "influence": {"good_for": ["celebration"], "avoid": ["conflict"]}
            }

            result = await self.checker.check_date("2024-01-15", "wedding", "chinese")

            assert "date" in result
            assert "auspicious_level" in result
            assert "good_for" in result
            assert "avoid" in result
            assert "zodiac_day" in result
            assert "recommendations" in result
            assert result["date"] == "2024-01-15"

    @pytest.mark.asyncio
    async def test_check_date_invalid(self):
        """Test checking invalid date."""
        result = await self.checker.check_date("invalid-date", "wedding", "chinese")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_find_good_dates(self):
        """Test finding good dates in range."""
        with patch.object(self.checker, 'check_date') as mock_check:
            mock_check.return_value = {
                "auspicious_level": "very_good",
                "score": 8,
                "zodiac_day": "Dragon",
                "lucky_hours": ["09:00-11:00"],
                "moon_phase": "Full Moon"
            }

            result = await self.checker.find_good_dates(
                "2024-01-01", "2024-01-07", "wedding", "chinese", 3
            )

            assert "activity" in result
            assert "good_dates" in result
            assert "found_dates" in result
            assert result["activity"] == "wedding"
            assert len(result["good_dates"]) <= 3

    @pytest.mark.asyncio
    async def test_get_daily_fortune(self):
        """Test getting daily fortune."""
        with patch.object(self.checker.lunar_calc, 'get_moon_phase') as mock_moon:
            mock_moon.return_value = {
                "phase_name": "Full Moon"
            }

            result = await self.checker.get_daily_fortune("2024-01-15", "chinese")

            assert "date" in result
            assert "fortune_level" in result
            assert "fortune_score" in result
            assert "description" in result
            assert "zodiac_day" in result
            assert "lucky_colors" in result
            assert "lucky_numbers" in result
            assert "advice" in result

    @pytest.mark.asyncio
    async def test_check_zodiac_compatibility(self):
        """Test checking zodiac compatibility."""
        result = await self.checker.check_zodiac_compatibility(
            "2024-01-15", "2024-02-15", "chinese"
        )

        assert "date1" in result
        assert "date2" in result
        assert "zodiac1" in result
        assert "zodiac2" in result
        assert "compatibility_level" in result
        assert "description" in result
        assert "recommendations" in result

    def test_generate_recommendations(self):
        """Test recommendation generation."""
        auspiciousness = {"level": "very_good"}
        rec = self.checker._generate_recommendations(auspiciousness, "wedding")

        assert isinstance(rec, str)
        assert "wedding" in rec
        assert len(rec) > 10  # Should be a meaningful recommendation

    def test_get_lucky_colors(self):
        """Test lucky colors based on five elements."""
        colors = self.checker._get_lucky_colors("Fire")
        assert isinstance(colors, list)
        assert len(colors) > 0
        assert "red" in colors or "orange" in colors

    def test_get_lucky_numbers(self):
        """Test lucky numbers calculation."""
        numbers = self.checker._get_lucky_numbers(15)
        assert isinstance(numbers, list)
        assert len(numbers) > 0
        assert all(isinstance(n, int) for n in numbers)

    def test_get_lucky_directions(self):
        """Test lucky directions based on earthly branch."""
        directions = self.checker._get_lucky_directions("子")
        assert isinstance(directions, list)
        assert len(directions) > 0
        assert "North" in directions

    def test_get_daily_advice(self):
        """Test daily advice generation."""
        advice = self.checker._get_daily_advice("excellent", "Fire")
        assert isinstance(advice, str)
        assert len(advice) > 10

    def test_check_element_compatibility(self):
        """Test five elements compatibility checking."""
        result = self.checker._check_element_compatibility("Fire", "Water")
        assert "type" in result
        assert "description" in result
        assert result["type"] in ["generative", "destructive", "supportive", "weakening", "neutral"]

    def test_get_compatibility_recommendations(self):
        """Test compatibility recommendations."""
        rec = self.checker._get_compatibility_recommendations("excellent")
        assert isinstance(rec, str)
        assert len(rec) > 10