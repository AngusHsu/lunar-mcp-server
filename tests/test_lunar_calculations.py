"""Tests for lunar calculations module."""

from datetime import datetime

import pytest

from lunar_mcp_server.lunar_calculations import LunarCalculator


class TestLunarCalculator:
    """Test cases for LunarCalculator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calculator = LunarCalculator()

    def test_parse_location_coordinates(self):
        """Test parsing coordinate location strings."""
        lat, lon = self.calculator._parse_location("40.7128,-74.0060")
        assert lat == 40.7128
        assert lon == -74.0060

    def test_parse_location_default(self):
        """Test parsing default location."""
        lat, lon = self.calculator._parse_location("0,0")
        assert lat == 0.0
        assert lon == 0.0

    def test_parse_location_city(self):
        """Test parsing known city location."""
        lat, lon = self.calculator._parse_location("beijing")
        assert lat == 39.9042
        assert lon == 116.4074

    def test_parse_location_invalid(self):
        """Test parsing invalid location returns default."""
        lat, lon = self.calculator._parse_location("invalid,location")
        assert lat == 0.0
        assert lon == 0.0

    def test_get_moon_phase_name(self):
        """Test moon phase name calculation."""
        # New Moon
        phase = self.calculator._get_moon_phase_name(0.001, 0)
        assert phase == "New Moon"

        # Full Moon
        phase = self.calculator._get_moon_phase_name(0.99, 180)
        assert phase == "Full Moon"

        # Waxing Crescent
        phase = self.calculator._get_moon_phase_name(0.15, 45)
        assert phase == "Waxing Crescent"

        # First Quarter (more precise)
        phase = self.calculator._get_moon_phase_name(0.49, 90)
        assert phase == "First Quarter"

    def test_calculate_lunar_day(self):
        """Test lunar day calculation."""
        test_date = datetime(2024, 1, 15)
        lunar_day = self.calculator._calculate_lunar_day(test_date)
        assert 1 <= lunar_day <= 30

    @pytest.mark.asyncio
    async def test_get_moon_phase(self):
        """Test getting moon phase for a date."""
        result = await self.calculator.get_moon_phase("2024-01-15", "0,0")

        assert "date" in result
        assert "phase_name" in result
        assert "illumination" in result
        assert "lunar_day" in result
        assert "zodiac_sign" in result
        assert "influence" in result
        assert result["date"] == "2024-01-15"

    @pytest.mark.asyncio
    async def test_get_moon_phase_invalid_date(self):
        """Test moon phase with invalid date."""
        result = await self.calculator.get_moon_phase("invalid-date", "0,0")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_moon_calendar(self):
        """Test getting monthly moon calendar."""
        result = await self.calculator.get_moon_calendar(1, 2024, "0,0")

        assert "month" in result
        assert "year" in result
        assert "calendar" in result
        assert result["month"] == 1
        assert result["year"] == 2024
        assert len(result["calendar"]) == 31  # January has 31 days

    @pytest.mark.asyncio
    async def test_get_moon_influence(self):
        """Test getting moon influence on activities."""
        result = await self.calculator.get_moon_influence("2024-01-15", "wedding")

        assert "date" in result
        assert "activity" in result
        assert "moon_phase" in result
        assert "activity_rating" in result
        assert "recommendation" in result
        assert result["activity"] == "wedding"

    def test_get_activity_recommendation(self):
        """Test activity recommendation generation."""
        rec = self.calculator._get_activity_recommendation(
            "wedding", "Full Moon", "excellent"
        )
        assert "Full Moon" in rec
        assert "wedding" in rec
        assert "excellent" in rec.lower() or "optimal" in rec.lower()

    @pytest.mark.asyncio
    async def test_predict_moon_phases(self):
        """Test predicting moon phases in date range."""
        result = await self.calculator.predict_moon_phases("2024-01-01", "2024-01-31")

        assert "start_date" in result
        assert "end_date" in result
        assert "major_phases" in result
        assert "total_phases" in result
        assert result["start_date"] == "2024-01-01"
        assert result["end_date"] == "2024-01-31"

    def test_get_moon_influence_traditional(self):
        """Test traditional moon influence calculation."""
        influence = self.calculator._get_moon_influence_traditional("Full Moon", 15)

        assert "good_for" in influence
        assert "avoid" in influence
        assert "energy_type" in influence
        assert "luck_level" in influence
        assert isinstance(influence["good_for"], list)
        assert isinstance(influence["avoid"], list)
