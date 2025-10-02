"""
Festival database and management for lunar calendar systems.
"""

from datetime import datetime, timedelta
from typing import Any

from .calendar_conversions import CalendarConverter


class FestivalManager:
    """Manager for lunar festivals across different cultures."""

    def __init__(self) -> None:
        """Initialize the festival manager."""
        self.calendar_converter = CalendarConverter()
        self._load_festival_data()

    def _load_festival_data(self) -> None:
        """Load festival data for different cultures."""
        # Chinese festivals
        self.chinese_festivals = {
            "spring_festival": {
                "name": "Spring Festival (Chinese New Year)",
                "lunar_date": "1-1",  # 1st month, 1st day
                "duration": 15,
                "significance": "Beginning of lunar new year, most important Chinese festival",
                "traditions": [
                    "family reunion dinner",
                    "fireworks",
                    "red envelopes (hongbao)",
                    "dragon and lion dances",
                    "visiting relatives",
                ],
                "foods": ["dumplings", "fish", "rice cakes", "spring rolls"],
                "taboos": ["sweeping", "breaking things", "arguing", "crying"],
                "lucky_activities": [
                    "wearing red",
                    "giving gifts",
                    "paying respects to ancestors",
                ],
                "regional_names": ["Chinese New Year", "Lunar New Year", "春节"],
            },
            "lantern_festival": {
                "name": "Lantern Festival",
                "lunar_date": "1-15",
                "duration": 1,
                "significance": "End of Spring Festival celebrations, first full moon of lunar year",
                "traditions": [
                    "lantern displays",
                    "riddles",
                    "lion dances",
                    "family gathering",
                ],
                "foods": ["tangyuan (sweet rice balls)", "yuanxiao"],
                "lucky_activities": [
                    "viewing lanterns",
                    "solving riddles",
                    "eating tangyuan",
                ],
                "regional_names": ["元宵节", "Shangyuan Festival"],
            },
            "qingming": {
                "name": "Qingming Festival",
                "solar_date": "04-04",  # Usually April 4-6
                "duration": 1,
                "significance": "Tomb sweeping day, honoring ancestors",
                "traditions": [
                    "tomb sweeping",
                    "ancestor worship",
                    "outdoor activities",
                ],
                "foods": ["qingtuan (green dumplings)", "cold food"],
                "lucky_activities": [
                    "cleaning graves",
                    "offering flowers",
                    "flying kites",
                ],
                "regional_names": ["Tomb Sweeping Day", "清明节"],
            },
            "dragon_boat": {
                "name": "Dragon Boat Festival",
                "lunar_date": "5-5",
                "duration": 1,
                "significance": "Commemorating poet Qu Yuan, warding off evil",
                "traditions": [
                    "dragon boat racing",
                    "hanging mugwort",
                    "five-color strings",
                ],
                "foods": ["zongzi (sticky rice dumplings)", "realgar wine"],
                "lucky_activities": [
                    "racing boats",
                    "wearing sachets",
                    "drinking wine",
                ],
                "regional_names": ["Duanwu Festival", "端午节"],
            },
            "qixi": {
                "name": "Qixi Festival",
                "lunar_date": "7-7",
                "duration": 1,
                "significance": "Chinese Valentine's Day, celebrating the weaver girl and cowherd",
                "traditions": ["making wishes", "stargazing", "romantic activities"],
                "foods": ["qiaoguo (clever fruits)", "noodles"],
                "lucky_activities": [
                    "praying for love",
                    "making handicrafts",
                    "stargazing",
                ],
                "regional_names": [
                    "Chinese Valentine's Day",
                    "七夕节",
                    "Double Seventh Festival",
                ],
            },
            "mid_autumn": {
                "name": "Mid-Autumn Festival",
                "lunar_date": "8-15",
                "duration": 1,
                "significance": "Moon festival, family reunion, harvest celebration",
                "traditions": ["moon viewing", "lanterns", "family gathering"],
                "foods": ["mooncakes", "pomelos", "osmanthus wine"],
                "lucky_activities": [
                    "moon gazing",
                    "eating mooncakes",
                    "family reunion",
                ],
                "regional_names": ["Moon Festival", "中秋节", "Mooncake Festival"],
            },
            "double_ninth": {
                "name": "Double Ninth Festival",
                "lunar_date": "9-9",
                "duration": 1,
                "significance": "Climbing heights, honoring elderly, ward off evil",
                "traditions": [
                    "mountain climbing",
                    "chrysanthemum viewing",
                    "wearing dogwood",
                ],
                "foods": ["chrysanthemum wine", "chongyang cake"],
                "lucky_activities": [
                    "climbing mountains",
                    "honoring elders",
                    "viewing flowers",
                ],
                "regional_names": [
                    "Chongyang Festival",
                    "重阳节",
                    "Senior Citizens Day",
                ],
            },
        }

    async def get_festivals_for_date(
        self, date_str: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Get all festivals occurring on a specific date."""
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            festivals_found = []

            if culture == "chinese":
                # Convert to lunar date
                lunar_info = await self.calendar_converter.solar_to_lunar(
                    date_str, culture
                )
                lunar_month = lunar_info.get("lunar_month", 0)
                lunar_day = lunar_info.get("lunar_day", 0)
                lunar_date_str = f"{lunar_month}-{lunar_day}"

                # Check Chinese festivals
                for festival_id, festival_data in self.chinese_festivals.items():
                    if festival_data.get("lunar_date") == lunar_date_str:
                        festivals_found.append(
                            {
                                "id": festival_id,
                                "name": festival_data["name"],
                                "culture": "chinese",
                                "significance": festival_data["significance"],
                                "traditions": festival_data["traditions"],
                                "foods": festival_data["foods"],
                                "duration": festival_data["duration"],
                                "lucky_activities": festival_data.get(
                                    "lucky_activities", []
                                ),
                                "taboos": festival_data.get("taboos", []),
                                "is_major": festival_id
                                in ["spring_festival", "mid_autumn", "dragon_boat"],
                            }
                        )

                # Check solar-based Chinese festivals
                month_day = f"{target_date.month:02d}-{target_date.day:02d}"
                for festival_id, festival_data in self.chinese_festivals.items():
                    if festival_data.get("solar_date") == month_day:
                        festivals_found.append(
                            {
                                "id": festival_id,
                                "name": festival_data["name"],
                                "culture": "chinese",
                                "significance": festival_data["significance"],
                                "traditions": festival_data["traditions"],
                                "foods": festival_data["foods"],
                                "duration": festival_data["duration"],
                                "lucky_activities": festival_data.get(
                                    "lucky_activities", []
                                ),
                                "is_major": True,
                            }
                        )

            # Determine if any major festival
            is_major_festival = any(f.get("is_major", False) for f in festivals_found)

            return {
                "date": date_str,
                "culture": culture,
                "festivals": festivals_found,
                "festival_count": len(festivals_found),
                "is_major_festival": is_major_festival,
                "celebration_level": self._get_celebration_level(festivals_found),
            }

        except Exception as e:
            return {"error": f"Failed to get festivals for date: {str(e)}"}

    def _get_celebration_level(self, festivals: list[dict[str, Any]]) -> str:
        """Determine celebration level based on festivals."""
        if not festivals:
            return "none"

        major_count = sum(1 for f in festivals if f.get("is_major", False))
        total_count = len(festivals)

        if major_count > 0:
            return "major"
        elif total_count > 1:
            return "multiple"
        else:
            return "minor"

    async def get_next_festival(
        self, date_str: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Find the next upcoming festival after a given date."""
        try:
            start_date = datetime.strptime(date_str, "%Y-%m-%d")
            search_limit = 365  # Search within next year

            current_date = start_date + timedelta(days=1)  # Start from next day
            days_searched = 0

            while days_searched < search_limit:
                check_date_str = current_date.strftime("%Y-%m-%d")
                festivals_result = await self.get_festivals_for_date(
                    check_date_str, culture
                )

                if festivals_result.get("festivals"):
                    next_festival = festivals_result["festivals"][
                        0
                    ]  # Get first festival
                    days_until = (current_date - start_date).days

                    return {
                        "search_date": date_str,
                        "next_festival_date": check_date_str,
                        "days_until": days_until,
                        "festival": next_festival,
                        "culture": culture,
                        "preparation_time": self._get_preparation_advice(
                            days_until, next_festival
                        ),
                    }

                current_date += timedelta(days=1)
                days_searched += 1

            return {
                "search_date": date_str,
                "culture": culture,
                "message": f"No festivals found in the next {search_limit} days",
            }

        except Exception as e:
            return {"error": f"Failed to find next festival: {str(e)}"}

    def _get_preparation_advice(self, days_until: int, festival: dict[str, Any]) -> str:
        """Get preparation advice based on time until festival."""
        if days_until <= 3:
            return f"Festival is very soon! Time for final preparations: {', '.join(festival.get('traditions', [])[:2])}"
        elif days_until <= 7:
            return f"Festival is next week. Start preparing: {', '.join(festival.get('traditions', [])[:3])}"
        elif days_until <= 30:
            return f"Festival is in {days_until} days. Plan ahead for: {festival.get('significance', 'celebration')}"
        else:
            return f"Festival is in {days_until} days. Early planning recommended."

    async def get_festival_details(
        self, festival_name: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Get detailed information about a specific festival."""
        try:
            festival_data = None
            festival_id = None

            # Search by name or ID in Chinese festivals
            for fid, fdata in self.chinese_festivals.items():
                fest_name: str = str(fdata.get("name", ""))
                regional = fdata.get("regional_names", [])
                regional_list: list[Any] = regional if isinstance(regional, list) else []
                if (
                    fest_name.lower() == festival_name.lower()
                    or fid.lower() == festival_name.lower()
                    or any(
                        str(name).lower() == festival_name.lower()
                        for name in regional_list
                    )
                ):
                    festival_data = fdata
                    festival_id = fid
                    break

            if not festival_data or festival_id is None:
                return {
                    "error": f"Festival '{festival_name}' not found in {culture} calendar",
                    "available_festivals": self._get_available_festivals(culture),
                }

            # Calculate next occurrence
            next_occurrence = await self._calculate_next_occurrence(
                festival_id, festival_data, culture
            )

            return {
                "festival_id": festival_id,
                "name": festival_data["name"],
                "culture": culture,
                "significance": festival_data["significance"],
                "duration": festival_data["duration"],
                "traditions": festival_data["traditions"],
                "foods": festival_data["foods"],
                "lucky_activities": festival_data.get("lucky_activities", []),
                "taboos": festival_data.get("taboos", []),
                "regional_names": festival_data.get("regional_names", []),
                "next_occurrence": next_occurrence,
                "preparation_guide": self._get_preparation_guide(festival_data),
                "cultural_context": self._get_cultural_context(festival_id, culture),
            }

        except Exception as e:
            return {"error": f"Failed to get festival details: {str(e)}"}

    def _get_available_festivals(self, culture: str) -> list[str]:
        """Get list of available festivals for Chinese culture."""
        return [str(data.get("name", "")) for data in self.chinese_festivals.values()]

    async def _calculate_next_occurrence(
        self, festival_id: str, festival_data: dict[str, Any], culture: str
    ) -> dict[str, Any]:
        """Calculate the next occurrence of a festival."""
        try:
            current_year = datetime.now().year

            # For lunar-based festivals, we need to convert
            if culture == "chinese" and "lunar_date" in festival_data:
                # This would require proper lunar calendar calculation
                # For now, return approximate date
                return {
                    "year": current_year,
                    "approximate_date": "Calculation requires lunar calendar conversion",
                    "note": "Exact date varies each year based on lunar calendar",
                }

            else:
                return {
                    "note": "Next occurrence calculation not available for this festival type"
                }

        except Exception:
            return {"error": "Failed to calculate next occurrence"}

    def _get_preparation_guide(
        self, festival_data: dict[str, Any]
    ) -> dict[str, list[str]]:
        """Get preparation guide for a festival."""
        return {
            "1_week_before": [
                "Plan gatherings and invitations",
                "Shop for special foods and decorations",
                "Prepare traditional items",
            ],
            "3_days_before": [
                "Complete major preparations",
                "Confirm family plans",
                "Prepare ceremonial items",
            ],
            "day_of_festival": festival_data.get("traditions", []),
            "foods_to_prepare": festival_data.get("foods", []),
            "activities": festival_data.get("lucky_activities", []),
        }

    def _get_cultural_context(self, festival_id: str, culture: str) -> str:
        """Get cultural context and historical background for Chinese festivals."""
        context_map = {
            "spring_festival": "The most important festival in Chinese culture, marking the lunar new year with over 4000 years of history.",
            "mid_autumn": "Ancient harvest festival celebrating family unity and the full moon, dating back over 1000 years.",
            "dragon_boat": "Commemorates the ancient poet Qu Yuan and traditionally wards off evil spirits.",
            "lantern_festival": "Marks the end of Spring Festival celebrations and the first full moon of the lunar year.",
        }

        return context_map.get(festival_id, "Cultural context not available.")

    async def get_annual_festivals(
        self, year: int, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Get all festivals for a specific year."""
        try:
            annual_festivals = []
            festival_calendar: dict[int, list[dict[str, Any]]] = {}
            festivals_to_calculate = self.chinese_festivals

            # For demonstration, create a simplified calendar
            # In a full implementation, you'd calculate exact dates based on lunar/solar calendars
            for festival_id, festival_data in festivals_to_calculate.items():
                estimated_date = self._estimate_festival_date(
                    festival_data, year, culture
                )
                if estimated_date:
                    month = estimated_date.get("month", 1)
                    if month not in festival_calendar:
                        festival_calendar[month] = []

                    festival_calendar[month].append(
                        {
                            "id": festival_id,
                            "name": festival_data["name"],
                            "estimated_date": estimated_date,
                            "duration": festival_data["duration"],
                            "significance": festival_data["significance"],
                            "is_major": festival_id
                            in self._get_major_festivals(culture),
                        }
                    )

                    annual_festivals.append(
                        {
                            "id": festival_id,
                            "name": festival_data["name"],
                            "estimated_date": estimated_date,
                            "culture": culture,
                            "significance": festival_data["significance"],
                        }
                    )

            return {
                "year": year,
                "culture": culture,
                "total_festivals": len(annual_festivals),
                "festivals": annual_festivals,
                "calendar_view": festival_calendar,
                "major_festivals": [
                    f
                    for f in annual_festivals
                    if f["id"] in self._get_major_festivals(culture)
                ],
                "note": "Dates are estimated. Actual dates may vary based on lunar observations.",
            }

        except Exception as e:
            return {"error": f"Failed to get annual festivals: {str(e)}"}

    def _estimate_festival_date(
        self, festival_data: dict[str, Any], year: int, culture: str
    ) -> dict[str, Any] | None:
        """Estimate festival date for a given year."""
        if "solar_date" in festival_data:
            month, day = map(int, festival_data["solar_date"].split("-"))
            return {"year": year, "month": month, "day": day, "type": "solar"}

        elif "lunar_date" in festival_data and culture == "chinese":
            lunar_month, lunar_day = map(int, festival_data["lunar_date"].split("-"))
            # Simplified estimation - in reality, you'd need proper lunar calendar conversion
            estimated_solar_month = min(12, max(1, lunar_month + 1))
            return {
                "year": year,
                "month": estimated_solar_month,
                "day": min(28, lunar_day + 10),
                "type": "lunar_estimated",
                "lunar_month": lunar_month,
                "lunar_day": lunar_day,
            }

        return None

    def _get_major_festivals(self, culture: str) -> list[str]:
        """Get list of major Chinese festivals."""
        return ["spring_festival", "mid_autumn", "dragon_boat", "lantern_festival"]
