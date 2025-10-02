"""
Calendar conversion utilities for Chinese lunar calendar system.
"""

from datetime import date, datetime
from typing import Any

try:
    from lunardate import LunarDate

    LUNARDATE_AVAILABLE = True
except ImportError:
    LUNARDATE_AVAILABLE = False

try:
    from zhdate import ZhDate

    ZHDATE_AVAILABLE = True
except ImportError:
    ZHDATE_AVAILABLE = False

try:
    import chinese_calendar

    CHINESE_CALENDAR_AVAILABLE = True
except ImportError:
    CHINESE_CALENDAR_AVAILABLE = False


class CalendarConverter:
    """Converter between different calendar systems."""

    def __init__(self) -> None:
        """Initialize the calendar converter."""
        self.zodiac_animals = [
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

        self.zodiac_elements = ["Wood", "Fire", "Earth", "Metal", "Water"]

        # Traditional Chinese zodiac start years (Rat years)
        self.rat_years = [
            1900,
            1912,
            1924,
            1936,
            1948,
            1960,
            1972,
            1984,
            1996,
            2008,
            2020,
            2032,
        ]

    def _calculate_chinese_zodiac_year(self, year: int) -> dict[str, Any]:
        """Calculate Chinese zodiac animal and element for a year."""
        # Find the closest rat year
        base_year = 1900
        year_diff = year - base_year
        zodiac_index = year_diff % 12

        # Calculate element (each animal has 2 years of same element)
        element_cycle = year_diff % 10
        element_index = element_cycle // 2

        # Determine yin/yang
        is_yang = (year_diff % 2) == 0

        return {
            "animal": self.zodiac_animals[zodiac_index],
            "element": self.zodiac_elements[element_index],
            "yin_yang": "Yang" if is_yang else "Yin",
            "full_name": f"{self.zodiac_elements[element_index]} {self.zodiac_animals[zodiac_index]}",
            "cycle_position": year_diff % 60,
        }

    def _fallback_chinese_conversion(self, solar_date: date) -> dict[str, Any]:
        """Fallback Chinese lunar conversion when libraries are unavailable."""
        # Simplified lunar calendar calculation
        # This is an approximation - real lunar calendar conversion is more complex

        # Average lunar month is 29.53059 days
        lunar_month_days = 29.53059

        # Reference new year dates (approximate)
        chinese_new_years = {
            2020: date(2020, 1, 25),
            2021: date(2021, 2, 12),
            2022: date(2022, 2, 1),
            2023: date(2023, 1, 22),
            2024: date(2024, 2, 10),
            2025: date(2025, 1, 29),
            2026: date(2026, 2, 17),
        }

        year = solar_date.year
        chinese_new_year = chinese_new_years.get(year)

        if not chinese_new_year:
            # Estimate based on pattern (Chinese New Year is typically between Jan 21 - Feb 20)
            estimated_ny = date(year, 1, 25) if year % 4 == 0 else date(year, 2, 1)
            chinese_new_year = estimated_ny

        # Determine lunar year
        if solar_date < chinese_new_year:
            lunar_year = year - 1
            # Days since previous Chinese New Year
            prev_ny = chinese_new_years.get(year - 1, date(year - 1, 2, 1))
            days_since_ny = (solar_date - prev_ny).days
        else:
            lunar_year = year
            days_since_ny = (solar_date - chinese_new_year).days

        # Calculate lunar month and day (approximation)
        lunar_month = min(12, max(1, int(days_since_ny / lunar_month_days) + 1))
        lunar_day = min(30, max(1, int(days_since_ny % lunar_month_days) + 1))

        result: dict[str, Any] = {
            "lunar_year": lunar_year,
            "lunar_month": lunar_month,
            "lunar_day": lunar_day,
            "chinese_new_year": chinese_new_year.strftime("%Y-%m-%d"),
            "days_since_new_year": days_since_ny,
            "zodiac_info": self._calculate_chinese_zodiac_year(lunar_year),
            "calculation_method": "approximation",
        }
        return result

    async def solar_to_lunar(
        self, solar_date_str: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Convert solar date to Chinese lunar date."""
        try:
            solar_date = datetime.strptime(solar_date_str, "%Y-%m-%d").date()
            return await self._solar_to_chinese_lunar(solar_date)

        except Exception as e:
            return {"error": f"Failed to convert solar to lunar date: {str(e)}"}

    async def _solar_to_chinese_lunar(self, solar_date: date) -> dict[str, Any]:
        """Convert solar date to Chinese lunar date."""
        try:
            result: dict[str, Any] = {
                "solar_date": solar_date.strftime("%Y-%m-%d"),
                "culture": "chinese",
            }

            # Try using specialized libraries first
            if ZHDATE_AVAILABLE:
                try:
                    zh_date = ZhDate.from_datetime(
                        datetime.combine(solar_date, datetime.min.time())
                    )
                    zodiac_info = self._calculate_chinese_zodiac_year(
                        zh_date.lunar_year
                    )

                    result.update(
                        {
                            "lunar_year": zh_date.lunar_year,
                            "lunar_month": zh_date.lunar_month,
                            "lunar_day": zh_date.lunar_day,
                            "is_leap_month": zh_date.leap_month,
                            "zodiac_info": zodiac_info,
                            "lunar_date_string": f"{zh_date.lunar_year}-{zh_date.lunar_month}-{zh_date.lunar_day}",
                            "calculation_method": "zhdate",
                        }
                    )
                    return result
                except Exception:
                    pass

            if LUNARDATE_AVAILABLE:
                try:
                    lunar_date = LunarDate.fromSolarDate(
                        solar_date.year, solar_date.month, solar_date.day
                    )
                    zodiac_info = self._calculate_chinese_zodiac_year(lunar_date.year)

                    result.update(
                        {
                            "lunar_year": lunar_date.year,
                            "lunar_month": lunar_date.month,
                            "lunar_day": lunar_date.day,
                            "is_leap_month": getattr(lunar_date, "isLeapMonth", False),
                            "zodiac_info": zodiac_info,
                            "lunar_date_string": f"{lunar_date.year}-{lunar_date.month}-{lunar_date.day}",
                            "calculation_method": "lunardate",
                        }
                    )
                    return result
                except Exception:
                    pass

            # Fallback to approximation
            fallback_result = self._fallback_chinese_conversion(solar_date)
            result.update(fallback_result)
            return result

        except Exception as e:
            return {"error": f"Failed to convert to Chinese lunar date: {str(e)}"}

    async def lunar_to_solar(
        self, lunar_date_str: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Convert Chinese lunar date to solar date."""
        try:
            return await self._chinese_lunar_to_solar(lunar_date_str)

        except Exception as e:
            return {"error": f"Failed to convert lunar to solar date: {str(e)}"}

    async def _chinese_lunar_to_solar(self, lunar_date_str: str) -> dict[str, Any]:
        """Convert Chinese lunar date to solar date."""
        try:
            # Parse lunar date string (format: YYYY-MM-DD)
            parts = lunar_date_str.split("-")
            if len(parts) != 3:
                return {"error": "Invalid lunar date format. Use YYYY-MM-DD"}

            lunar_year, lunar_month, lunar_day = map(int, parts)

            result = {
                "lunar_date": lunar_date_str,
                "culture": "chinese",
                "lunar_year": lunar_year,
                "lunar_month": lunar_month,
                "lunar_day": lunar_day,
            }

            # Try using specialized libraries
            if ZHDATE_AVAILABLE:
                try:
                    zh_date = ZhDate(lunar_year, lunar_month, lunar_day)
                    solar_date = zh_date.to_datetime().date()

                    result.update(
                        {
                            "solar_date": solar_date.strftime("%Y-%m-%d"),
                            "solar_year": solar_date.year,
                            "solar_month": solar_date.month,
                            "solar_day": solar_date.day,
                            "calculation_method": "zhdate",
                        }
                    )
                    return result
                except Exception:
                    pass

            if LUNARDATE_AVAILABLE:
                try:
                    lunar_date = LunarDate(lunar_year, lunar_month, lunar_day)
                    solar_date = lunar_date.toSolarDate()

                    result.update(
                        {
                            "solar_date": solar_date.strftime("%Y-%m-%d"),
                            "solar_year": solar_date.year,
                            "solar_month": solar_date.month,
                            "solar_day": solar_date.day,
                            "calculation_method": "lunardate",
                        }
                    )
                    return result
                except Exception:
                    pass

            # Fallback approximation
            # This is a very rough estimate
            estimated_solar_month = min(12, max(1, lunar_month + 1))
            estimated_solar_day = min(28, lunar_day)

            result.update(
                {
                    "solar_date": f"{lunar_year}-{estimated_solar_month:02d}-{estimated_solar_day:02d}",
                    "solar_year": lunar_year,
                    "solar_month": estimated_solar_month,
                    "solar_day": estimated_solar_day,
                    "calculation_method": "approximation",
                    "warning": "This is a rough approximation. Actual conversion requires lunar calendar libraries.",
                }
            )
            return result

        except Exception as e:
            return {"error": f"Failed to convert Chinese lunar to solar date: {str(e)}"}

    async def get_zodiac_info(
        self, date_str: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Get Chinese zodiac information for a date."""
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return await self._get_chinese_zodiac_info(target_date)

        except Exception as e:
            return {"error": f"Failed to get zodiac info: {str(e)}"}

    async def _get_chinese_zodiac_info(self, target_date: date) -> dict[str, Any]:
        """Get Chinese zodiac information."""
        try:
            # Get lunar conversion for more accurate zodiac calculation
            lunar_info = await self.solar_to_lunar(
                target_date.strftime("%Y-%m-%d"), "chinese"
            )

            year_zodiac = self._calculate_chinese_zodiac_year(target_date.year)

            # Calculate daily zodiac animal (12-day cycle)
            # Reference: January 1, 2000 was a Rat day
            reference_date = date(2000, 1, 1)  # Rat day
            days_diff = (target_date - reference_date).days
            daily_zodiac_index = days_diff % 12

            # Calculate hourly zodiac for current hour
            current_hour = datetime.now().hour
            hourly_zodiac_index = ((current_hour + 1) // 2) % 12

            # Chinese zodiac characteristics
            zodiac_traits = {
                "Rat": {
                    "personality": "clever, adaptable, charming",
                    "lucky_colors": ["blue", "gold", "green"],
                    "lucky_numbers": [2, 3],
                },
                "Ox": {
                    "personality": "reliable, strong, determined",
                    "lucky_colors": ["white", "yellow", "green"],
                    "lucky_numbers": [1, 9],
                },
                "Tiger": {
                    "personality": "brave, competitive, confident",
                    "lucky_colors": ["orange", "gray", "white"],
                    "lucky_numbers": [1, 3, 4],
                },
                "Rabbit": {
                    "personality": "gentle, quiet, elegant",
                    "lucky_colors": ["pink", "purple", "blue"],
                    "lucky_numbers": [3, 4, 9],
                },
                "Dragon": {
                    "personality": "energetic, intelligent, gifted",
                    "lucky_colors": ["gold", "silver", "gray"],
                    "lucky_numbers": [1, 6, 7],
                },
                "Snake": {
                    "personality": "wise, elegant, intuitive",
                    "lucky_colors": ["black", "red", "yellow"],
                    "lucky_numbers": [2, 8, 9],
                },
                "Horse": {
                    "personality": "animated, active, energetic",
                    "lucky_colors": ["yellow", "green", "purple"],
                    "lucky_numbers": [2, 3, 7],
                },
                "Goat": {
                    "personality": "calm, gentle, sympathetic",
                    "lucky_colors": ["green", "red", "purple"],
                    "lucky_numbers": [3, 9, 4],
                },
                "Monkey": {
                    "personality": "sharp, smart, curious",
                    "lucky_colors": ["white", "gold", "blue"],
                    "lucky_numbers": [1, 8, 7],
                },
                "Rooster": {
                    "personality": "observant, hardworking, courageous",
                    "lucky_colors": ["gold", "brown", "yellow"],
                    "lucky_numbers": [5, 7, 8],
                },
                "Dog": {
                    "personality": "lovely, honest, responsible",
                    "lucky_colors": ["green", "red", "purple"],
                    "lucky_numbers": [3, 4, 9],
                },
                "Pig": {
                    "personality": "honest, generous, reliable",
                    "lucky_colors": ["yellow", "gray", "brown"],
                    "lucky_numbers": [2, 5, 8],
                },
            }

            year_animal = year_zodiac["animal"]
            daily_animal = self.zodiac_animals[daily_zodiac_index]
            hourly_animal = self.zodiac_animals[hourly_zodiac_index]

            return {
                "date": target_date.strftime("%Y-%m-%d"),
                "culture": "chinese",
                "year_zodiac": year_zodiac,
                "daily_zodiac": {
                    "animal": daily_animal,
                    "traits": zodiac_traits.get(daily_animal, {}),
                    "influence": f"Today is a {daily_animal} day, bringing {zodiac_traits.get(daily_animal, {}).get('personality', 'special')} energy",
                },
                "hourly_zodiac": {
                    "animal": hourly_animal,
                    "hour_range": f"{(hourly_zodiac_index * 2 - 1) % 24:02d}:00-{(hourly_zodiac_index * 2 + 1) % 24:02d}:00",
                    "influence": f"Current hours favor {hourly_animal} characteristics",
                },
                "lunar_info": lunar_info,
                "compatibility": {
                    "best_matches": self._get_zodiac_compatibility(year_animal)["best"],
                    "challenging_matches": self._get_zodiac_compatibility(year_animal)[
                        "challenging"
                    ],
                },
            }

        except Exception as e:
            return {"error": f"Failed to get Chinese zodiac info: {str(e)}"}

    def _get_zodiac_compatibility(self, animal: str) -> dict[str, list[str]]:
        """Get Chinese zodiac compatibility."""
        compatibility_map = {
            "Rat": {
                "best": ["Dragon", "Monkey", "Ox"],
                "challenging": ["Horse", "Goat"],
            },
            "Ox": {
                "best": ["Snake", "Rooster", "Rat"],
                "challenging": ["Goat", "Horse"],
            },
            "Tiger": {
                "best": ["Horse", "Dog", "Pig"],
                "challenging": ["Monkey", "Snake"],
            },
            "Rabbit": {
                "best": ["Goat", "Pig", "Dog"],
                "challenging": ["Rooster", "Dragon"],
            },
            "Dragon": {
                "best": ["Rat", "Monkey", "Rooster"],
                "challenging": ["Dog", "Rabbit"],
            },
            "Snake": {
                "best": ["Ox", "Rooster", "Monkey"],
                "challenging": ["Pig", "Tiger"],
            },
            "Horse": {"best": ["Tiger", "Dog", "Goat"], "challenging": ["Rat", "Ox"]},
            "Goat": {"best": ["Rabbit", "Pig", "Horse"], "challenging": ["Ox", "Rat"]},
            "Monkey": {
                "best": ["Rat", "Dragon", "Snake"],
                "challenging": ["Tiger", "Pig"],
            },
            "Rooster": {
                "best": ["Ox", "Snake", "Dragon"],
                "challenging": ["Rabbit", "Dog"],
            },
            "Dog": {
                "best": ["Tiger", "Horse", "Rabbit"],
                "challenging": ["Dragon", "Rooster"],
            },
            "Pig": {
                "best": ["Rabbit", "Goat", "Tiger"],
                "challenging": ["Snake", "Monkey"],
            },
        }
        return compatibility_map.get(animal, {"best": [], "challenging": []})
