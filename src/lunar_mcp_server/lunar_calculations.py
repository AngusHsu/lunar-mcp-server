"""
Astronomical calculations for lunar calendar operations.
"""

import math
from datetime import datetime, timedelta
from typing import Any

try:
    from skyfield.api import load, utc  # noqa: F401
    from skyfield.searchlib import find_discrete, find_maxima  # noqa: F401

    SKYFIELD_AVAILABLE = True
except ImportError:
    SKYFIELD_AVAILABLE = False

try:
    import ephem  # noqa: F401

    EPHEM_AVAILABLE = True
except ImportError:
    EPHEM_AVAILABLE = False


class LunarCalculator:
    """Calculator for lunar phases and astronomical data."""

    def __init__(self) -> None:
        """Initialize the lunar calculator."""
        self._cache: dict[str, Any] = {}

        if SKYFIELD_AVAILABLE:
            self.ts = load.timescale()
            self.eph = load("de421.bsp")
            self.earth = self.eph["earth"]
            self.moon = self.eph["moon"]
            self.sun = self.eph["sun"]

    def _parse_location(self, location: str) -> tuple[float, float]:
        """Parse location string to lat/lon coordinates."""
        if location == "0,0":
            return 0.0, 0.0

        if "," in location:
            try:
                parts = location.split(",")
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())
                return lat, lon
            except (ValueError, IndexError):
                return 0.0, 0.0

        # For city names, return default coordinates
        # In a full implementation, you'd use a geocoding service
        city_coords = {
            "beijing": (39.9042, 116.4074),
            "shanghai": (31.2304, 121.4737),
            "london": (51.5074, -0.1278),
            "new york": (40.7128, -74.0060),
            "tokyo": (35.6762, 139.6503),
        }

        return city_coords.get(location.lower(), (0.0, 0.0))

    def _get_moon_phase_name(self, illumination: float, phase_angle: float) -> str:
        """Get moon phase name from illumination percentage and phase angle."""
        if illumination < 0.01:
            return "New Moon"
        elif illumination < 0.25:
            return "Waxing Crescent"
        elif 0.25 <= illumination < 0.75:
            if phase_angle < 180:
                return (
                    "First Quarter"
                    if abs(illumination - 0.5) < 0.1
                    else "Waxing Gibbous"
                )
            else:
                return (
                    "Third Quarter"
                    if abs(illumination - 0.5) < 0.1
                    else "Waning Gibbous"
                )
        elif illumination < 0.99:
            return "Waning Crescent" if phase_angle > 180 else "Waxing Gibbous"
        else:
            return "Full Moon"

    def _calculate_lunar_day(self, target_date: datetime) -> int:
        """Calculate lunar day (1-30) for given date."""
        # Approximate lunar day calculation based on synodic month (29.5 days)
        lunar_cycle_start = datetime(2000, 1, 6, 18, 14)  # Known New Moon
        days_since = (target_date - lunar_cycle_start).total_seconds() / 86400
        lunar_months = days_since / 29.530588853
        lunar_day = int((lunar_months % 1) * 29.530588853) + 1
        return min(lunar_day, 30)

    def _get_moon_influence_traditional(
        self, phase_name: str, lunar_day: int
    ) -> dict[str, Any]:
        """Get traditional moon influence based on phase and lunar day."""
        influences = {
            "New Moon": {
                "good_for": [
                    "new beginnings",
                    "planting seeds",
                    "setting intentions",
                    "meditation",
                ],
                "avoid": ["harvesting", "major decisions", "surgery"],
                "energy_type": "introspective, new potential",
                "luck_level": "neutral",
            },
            "Waxing Crescent": {
                "good_for": ["starting projects", "learning", "building", "healing"],
                "avoid": ["letting go", "ending relationships", "major cuts"],
                "energy_type": "growing, building momentum",
                "luck_level": "good",
            },
            "First Quarter": {
                "good_for": [
                    "making decisions",
                    "taking action",
                    "overcoming obstacles",
                ],
                "avoid": ["passive activities", "waiting"],
                "energy_type": "active, challenging",
                "luck_level": "mixed",
            },
            "Waxing Gibbous": {
                "good_for": ["refining", "adjusting", "editing", "improving"],
                "avoid": ["starting completely new things", "major changes"],
                "energy_type": "refining, perfecting",
                "luck_level": "good",
            },
            "Full Moon": {
                "good_for": [
                    "completion",
                    "celebration",
                    "manifestation",
                    "emotional release",
                ],
                "avoid": ["starting new projects", "making major life changes"],
                "energy_type": "culmination, intense energy",
                "luck_level": "very good",
            },
            "Waning Gibbous": {
                "good_for": ["gratitude", "sharing knowledge", "teaching"],
                "avoid": ["accumulating", "hoarding"],
                "energy_type": "sharing, giving thanks",
                "luck_level": "good",
            },
            "Third Quarter": {
                "good_for": ["releasing", "forgiving", "letting go", "breaking habits"],
                "avoid": ["holding on", "starting new ventures"],
                "energy_type": "release, forgiveness",
                "luck_level": "mixed",
            },
            "Waning Crescent": {
                "good_for": ["rest", "reflection", "clearing out", "preparation"],
                "avoid": ["intense activities", "major commitments"],
                "energy_type": "surrender, rest",
                "luck_level": "neutral",
            },
        }

        base_influence = influences.get(phase_name, influences["New Moon"])

        # Adjust based on lunar day
        if lunar_day in [1, 15]:  # New and Full Moon days
            base_influence["luck_level"] = "very good"
        elif lunar_day in [8, 22]:  # Quarter days
            base_influence["luck_level"] = "mixed"

        return base_influence

    async def get_moon_phase(
        self, date_str: str, location: str = "0,0"
    ) -> dict[str, Any]:
        """Get detailed moon phase information for a specific date and location."""
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            lat, lon = self._parse_location(location)

            # Use Skyfield if available, otherwise fall back to approximation
            if SKYFIELD_AVAILABLE:
                t = self.ts.utc(target_date.year, target_date.month, target_date.day)

                # Calculate moon phase
                earth_moon = self.earth.at(t).observe(self.moon)
                earth_sun = self.earth.at(t).observe(self.sun)

                # Phase angle calculation
                phase_angle = earth_moon.separation_from(earth_sun).degrees
                illumination = (1 + math.cos(math.radians(phase_angle))) / 2

                # Moon rise/set times (simplified)
                rise_time = "06:30"  # Placeholder - would need more complex calculation
                set_time = "18:30"  # Placeholder

            else:
                # Fallback calculation using simple astronomical formulas
                days_since_new_moon = (target_date - datetime(2000, 1, 6)).days % 29.5
                phase_angle = (days_since_new_moon / 29.5) * 360
                illumination = (1 + math.cos(math.radians(phase_angle))) / 2

                rise_time = "06:30"
                set_time = "18:30"

            lunar_day = self._calculate_lunar_day(target_date)
            phase_name = self._get_moon_phase_name(illumination, phase_angle)

            # Get zodiac sign (simplified)
            zodiac_signs = [
                "Aries",
                "Taurus",
                "Gemini",
                "Cancer",
                "Leo",
                "Virgo",
                "Libra",
                "Scorpio",
                "Sagittarius",
                "Capricorn",
                "Aquarius",
                "Pisces",
            ]
            zodiac_index = int((target_date.timetuple().tm_yday + lunar_day) / 30) % 12
            zodiac_sign = zodiac_signs[zodiac_index]

            influence = self._get_moon_influence_traditional(phase_name, lunar_day)

            return {
                "date": date_str,
                "phase_name": phase_name,
                "illumination": round(illumination, 3),
                "phase_angle": round(phase_angle, 1),
                "lunar_day": lunar_day,
                "rise_time": rise_time,
                "set_time": set_time,
                "zodiac_sign": zodiac_sign,
                "location": f"{lat},{lon}",
                "influence": influence,
            }

        except Exception as e:
            return {"error": f"Failed to calculate moon phase: {str(e)}"}

    async def get_moon_calendar(
        self, month: int, year: int, location: str = "0,0"
    ) -> dict[str, Any]:
        """Get monthly calendar with moon phases."""
        try:
            calendar_data = []

            # Generate data for each day of the month
            start_date = datetime(year, month, 1)

            # Find the last day of the month
            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(days=1)

            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                moon_data = await self.get_moon_phase(date_str, location)
                calendar_data.append(
                    {
                        "date": date_str,
                        "day": current_date.day,
                        "phase_name": moon_data.get("phase_name"),
                        "illumination": moon_data.get("illumination"),
                        "lunar_day": moon_data.get("lunar_day"),
                    }
                )
                current_date += timedelta(days=1)

            return {
                "month": month,
                "year": year,
                "location": location,
                "calendar": calendar_data,
            }

        except Exception as e:
            return {"error": f"Failed to generate moon calendar: {str(e)}"}

    async def get_moon_influence(self, date_str: str, activity: str) -> dict[str, Any]:
        """Get how moon phase affects specific activities."""
        try:
            moon_data = await self.get_moon_phase(date_str)
            base_influence = moon_data.get("influence", {})

            # Activity-specific adjustments
            activity_adjustments = {
                "wedding": {
                    "Full Moon": "excellent",
                    "Waxing Gibbous": "very good",
                    "New Moon": "avoid",
                    "Waning Crescent": "poor",
                },
                "business_opening": {
                    "New Moon": "excellent",
                    "Waxing Crescent": "very good",
                    "Full Moon": "good",
                    "Waning Gibbous": "poor",
                },
                "travel": {
                    "Waxing Crescent": "excellent",
                    "First Quarter": "good",
                    "Third Quarter": "avoid",
                    "Waning Crescent": "poor",
                },
                "surgery": {
                    "Third Quarter": "good",
                    "Waning Crescent": "good",
                    "New Moon": "avoid",
                    "Full Moon": "avoid",
                },
                "planting": {
                    "New Moon": "excellent",
                    "Waxing Crescent": "very good",
                    "Full Moon": "poor",
                    "Waning Gibbous": "poor",
                },
            }

            phase_name = moon_data.get("phase_name", "Unknown")
            activity_rating = activity_adjustments.get(activity, {}).get(
                phase_name, "neutral"
            )

            return {
                "date": date_str,
                "activity": activity,
                "moon_phase": phase_name,
                "activity_rating": activity_rating,
                "general_influence": base_influence,
                "recommendation": self._get_activity_recommendation(
                    activity, phase_name, activity_rating
                ),
            }

        except Exception as e:
            return {"error": f"Failed to calculate moon influence: {str(e)}"}

    def _get_activity_recommendation(
        self, activity: str, phase: str, rating: str
    ) -> str:
        """Get detailed recommendation for activity based on moon phase."""
        if rating == "excellent":
            return f"The {phase} is highly favorable for {activity}. This is an optimal time to proceed."
        elif rating == "very good":
            return f"The {phase} provides good energy for {activity}. A favorable time to act."
        elif rating == "good":
            return f"The {phase} offers reasonable conditions for {activity}. Proceed with confidence."
        elif rating == "poor":
            return f"The {phase} is not ideal for {activity}. Consider waiting for a better time."
        elif rating == "avoid":
            return f"The {phase} is unfavorable for {activity}. It's best to postpone if possible."
        else:
            return f"The {phase} has neutral influence on {activity}. Normal considerations apply."

    async def predict_moon_phases(
        self, start_date_str: str, end_date_str: str
    ) -> dict[str, Any]:
        """Predict moon phases in a date range."""
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            phases = []
            current_date = start_date

            while current_date <= end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                moon_data = await self.get_moon_phase(date_str)

                # Include major phase transitions
                phase_name = moon_data.get("phase_name")
                if phase_name in [
                    "New Moon",
                    "First Quarter",
                    "Full Moon",
                    "Third Quarter",
                ]:
                    phases.append(
                        {
                            "date": date_str,
                            "phase": phase_name,
                            "illumination": moon_data.get("illumination"),
                            "lunar_day": moon_data.get("lunar_day"),
                        }
                    )

                current_date += timedelta(days=1)

            return {
                "start_date": start_date_str,
                "end_date": end_date_str,
                "major_phases": phases,
                "total_phases": len(phases),
            }

        except Exception as e:
            return {"error": f"Failed to predict moon phases: {str(e)}"}
