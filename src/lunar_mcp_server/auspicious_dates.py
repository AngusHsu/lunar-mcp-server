"""
Traditional auspicious date checking and fortune calculation.
"""

from datetime import datetime, timedelta
from typing import Any

from .calendar_conversions import CalendarConverter
from .lunar_calculations import LunarCalculator


class AuspiciousDateChecker:
    """Checker for auspicious dates based on traditional calendars."""

    def __init__(self) -> None:
        """Initialize the auspicious date checker."""
        self.lunar_calc = LunarCalculator()
        self.calendar_converter = CalendarConverter()
        self._load_traditional_data()

    def _load_traditional_data(self) -> None:
        """Load traditional auspicious date rules and data."""
        # Traditional Chinese Tong Shu (almanac) data
        self.chinese_rules = {
            "heavenly_stems": [
                "甲",
                "乙",
                "丙",
                "丁",
                "戊",
                "己",
                "庚",
                "辛",
                "壬",
                "癸",
            ],
            "earthly_branches": [
                "子",
                "丑",
                "寅",
                "卯",
                "辰",
                "巳",
                "午",
                "未",
                "申",
                "酉",
                "戌",
                "亥",
            ],
            "zodiac_animals": [
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
            ],
            "five_elements": ["Wood", "Fire", "Earth", "Metal", "Water"],
            "lunar_mansions": [
                "角",
                "亢",
                "氐",
                "房",
                "心",
                "尾",
                "箕",  # Eastern Azure Dragon
                "斗",
                "牛",
                "女",
                "虛",
                "危",
                "室",
                "壁",  # Northern Black Tortoise
                "奎",
                "婁",
                "胃",
                "昴",
                "畢",
                "觜",
                "參",  # Western White Tiger
                "井",
                "鬼",
                "柳",
                "星",
                "張",
                "翼",
                "軫",  # Southern Vermilion Bird
            ],
        }

        # Activity recommendations by lunar mansion
        self.mansion_activities = {
            "角": {
                "good": ["wedding", "construction", "moving"],
                "bad": ["funeral", "medical"],
            },
            "亢": {"good": ["business", "education"], "bad": ["travel", "litigation"]},
            "氐": {"good": ["marriage", "planting"], "bad": ["building", "hunting"]},
            "房": {"good": ["ceremony", "offering"], "bad": ["moving", "burial"]},
            "心": {
                "good": ["worship", "meditation"],
                "bad": ["construction", "business"],
            },
            "尾": {"good": ["fishing", "hunting"], "bad": ["marriage", "celebration"]},
            "箕": {"good": ["demolition", "cleaning"], "bad": ["wedding", "opening"]},
        }

        # Lucky hours by zodiac animal
        self.zodiac_hours = {
            "Rat": ["23:00-01:00"],
            "Ox": ["01:00-03:00"],
            "Tiger": ["03:00-05:00"],
            "Rabbit": ["05:00-07:00"],
            "Dragon": ["07:00-09:00"],
            "Snake": ["09:00-11:00"],
            "Horse": ["11:00-13:00"],
            "Goat": ["13:00-15:00"],
            "Monkey": ["15:00-17:00"],
            "Rooster": ["17:00-19:00"],
            "Dog": ["19:00-21:00"],
            "Pig": ["21:00-23:00"],
        }

        # Five elements relationships
        self.element_relationships = {
            "Wood": {
                "generates": "Fire",
                "destroys": "Earth",
                "generated_by": "Water",
                "destroyed_by": "Metal",
            },
            "Fire": {
                "generates": "Earth",
                "destroys": "Metal",
                "generated_by": "Wood",
                "destroyed_by": "Water",
            },
            "Earth": {
                "generates": "Metal",
                "destroys": "Water",
                "generated_by": "Fire",
                "destroyed_by": "Wood",
            },
            "Metal": {
                "generates": "Water",
                "destroys": "Wood",
                "generated_by": "Earth",
                "destroyed_by": "Fire",
            },
            "Water": {
                "generates": "Wood",
                "destroys": "Fire",
                "generated_by": "Metal",
                "destroyed_by": "Earth",
            },
        }

    def _get_chinese_calendar_info(self, date_obj: datetime) -> dict[str, Any]:
        """Get Chinese calendar information for a date."""
        # Calculate days since a known reference date
        reference_date = datetime(1900, 1, 31)  # Reference Chinese New Year
        days_diff = (date_obj - reference_date).days

        # Calculate sexagenary cycle (60-day cycle)
        stem_index = days_diff % 10
        branch_index = days_diff % 12

        # Calculate lunar mansion (simplified)
        mansion_index = days_diff % 28

        # Calculate five elements for the day
        element_index = stem_index % 5

        # Calculate zodiac year animal
        year_diff = date_obj.year - 1900
        zodiac_year_index = year_diff % 12

        # Calculate zodiac day animal
        zodiac_day_index = days_diff % 12

        return {
            "heavenly_stem": self.chinese_rules["heavenly_stems"][stem_index],
            "earthly_branch": self.chinese_rules["earthly_branches"][branch_index],
            "lunar_mansion": self.chinese_rules["lunar_mansions"][mansion_index],
            "five_element": self.chinese_rules["five_elements"][element_index],
            "zodiac_year": self.chinese_rules["zodiac_animals"][zodiac_year_index],
            "zodiac_day": self.chinese_rules["zodiac_animals"][zodiac_day_index],
            "sexagenary_day": days_diff % 60,
        }

    def _calculate_auspiciousness(
        self, date_obj: datetime, activity: str, culture: str
    ) -> dict[str, Any]:
        """Calculate auspiciousness level for a date and activity."""
        chinese_info = self._get_chinese_calendar_info(date_obj)
        lunar_mansion = chinese_info["lunar_mansion"]
        five_element = chinese_info["five_element"]
        zodiac_day = chinese_info["zodiac_day"]

        # Base auspiciousness from lunar mansion
        mansion_data = self.mansion_activities.get(
            lunar_mansion, {"good": [], "bad": []}
        )

        if activity in mansion_data["good"]:
            base_score = 8
        elif activity in mansion_data["bad"]:
            base_score = 2
        else:
            base_score = 5

        # Adjust based on five elements
        element_bonus = 0
        if activity == "wedding" and five_element in ["Fire", "Earth"]:
            element_bonus = 2
        elif activity == "business_opening" and five_element in ["Metal", "Water"]:
            element_bonus = 2
        elif activity == "construction" and five_element in ["Earth", "Metal"]:
            element_bonus = 2

        # Adjust based on zodiac animal
        zodiac_bonus = 0
        favorable_animals = {
            "wedding": ["Dragon", "Rooster", "Rabbit"],
            "business_opening": ["Dragon", "Tiger", "Horse"],
            "travel": ["Horse", "Monkey", "Rooster"],
            "moving": ["Dragon", "Snake", "Pig"],
            "medical": ["Rabbit", "Ox", "Dog"],
        }

        if zodiac_day in favorable_animals.get(activity, []):
            zodiac_bonus = 1

        final_score = min(10, base_score + element_bonus + zodiac_bonus)

        # Convert score to level
        if final_score >= 9:
            level = "very_good"
        elif final_score >= 7:
            level = "good"
        elif final_score >= 5:
            level = "neutral"
        elif final_score >= 3:
            level = "poor"
        else:
            level = "very_poor"

        return {
            "score": final_score,
            "level": level,
            "chinese_info": chinese_info,
            "factors": {
                "lunar_mansion_effect": base_score,
                "five_element_bonus": element_bonus,
                "zodiac_bonus": zodiac_bonus,
            },
        }

    async def check_date(
        self,
        date_str: str,
        activity: str,
        culture: str = "chinese",
        find_alternatives: bool = True,
    ) -> dict[str, Any]:
        """Check if a date is auspicious for an activity."""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            # Get moon phase information
            moon_data = await self.lunar_calc.get_moon_phase(date_str)

            # Calculate auspiciousness
            if culture == "chinese":
                auspiciousness = self._calculate_auspiciousness(
                    date_obj, activity, culture
                )
            else:
                # For other cultures, use simplified calculation
                auspiciousness = {"score": 5, "level": "neutral", "factors": {}}

            chinese_info = auspiciousness.get("chinese_info", {})
            zodiac_day = chinese_info.get("zodiac_day", "Unknown")

            # Get lucky hours
            lucky_hours = self.zodiac_hours.get(
                zodiac_day, ["09:00-11:00", "13:00-15:00"]
            )

            # Generate recommendations
            good_activities = []
            avoid_activities = []

            if auspiciousness["level"] in ["very_good", "good"]:
                good_activities = [activity, "celebration", "important meetings"]
                avoid_activities = ["conflicts", "major endings"]
            elif auspiciousness["level"] == "poor":
                good_activities = ["rest", "planning", "preparation"]
                avoid_activities = [
                    activity,
                    "important decisions",
                    "major investments",
                ]
            else:
                good_activities = ["routine activities", "daily tasks"]
                avoid_activities = ["high-risk activities"]

            # Convert lunar date using calendar converter when possible
            lunar_date = "Unknown"
            try:
                lunar_info = await self.calendar_converter.solar_to_lunar(
                    date_str, culture
                )
            except Exception:
                lunar_info = {"error": "conversion failed"}

            if isinstance(lunar_info, dict) and "error" not in lunar_info:
                if culture == "chinese":
                    lunar_year = lunar_info.get("lunar_year")
                    lunar_month = lunar_info.get("lunar_month")
                    lunar_day = lunar_info.get("lunar_day")
                    lunar_date = lunar_info.get("lunar_date_string") or "-".join(
                        str(part)
                        for part in (lunar_year, lunar_month, lunar_day)
                        if part is not None
                    )

            if not lunar_date or lunar_date == "Unknown":
                lunar_day = moon_data.get("lunar_day")
                lunar_date = (
                    f"{date_obj.year}-{lunar_day}"
                    if lunar_day is not None
                    else date_str
                )

            # Generate detailed explanation
            explanation = self._generate_explanation(
                auspiciousness, chinese_info, moon_data, activity
            )

            # Find alternative dates if score is low (and alternatives are requested)
            alternatives = []
            if find_alternatives and auspiciousness["score"] < 7:
                alternatives = await self._find_alternative_dates(
                    date_obj, activity, culture
                )

            return {
                "date": date_str,
                "lunar_date": lunar_date,
                "auspicious_level": auspiciousness["level"],
                "score": auspiciousness["score"],
                "good_for": good_activities,
                "avoid": avoid_activities,
                "lucky_hours": lucky_hours,
                "zodiac_day": zodiac_day,
                "five_elements": chinese_info.get("five_element", "Unknown"),
                "lunar_mansion": chinese_info.get("lunar_mansion", "Unknown"),
                "moon_phase": moon_data.get("phase_name", "Unknown"),
                "moon_influence": moon_data.get("influence", {}),
                "recommendations": self._generate_recommendations(
                    auspiciousness, activity
                ),
                "calculation_factors": auspiciousness.get("factors", {}),
                "explanation": explanation["summary"],
                "reasoning": explanation["reasoning"],
                "better_alternatives": alternatives if alternatives else None,
            }

        except Exception as e:
            return {"error": f"Failed to check auspicious date: {str(e)}"}

    def _generate_recommendations(
        self, auspiciousness: dict[str, Any], activity: str
    ) -> str:
        """Generate detailed recommendations based on auspiciousness."""
        level = auspiciousness["level"]

        if level == "very_good":
            return f"Excellent day for {activity}. All traditional factors align favorably. Proceed with confidence and expect positive outcomes."
        elif level == "good":
            return f"Good day for {activity}. Most factors are favorable. A suitable time to move forward with your plans."
        elif level == "neutral":
            return f"Average day for {activity}. Neither particularly favorable nor unfavorable. Normal precautions apply."
        elif level == "poor":
            return f"Challenging day for {activity}. Consider postponing if possible, or take extra precautions if you must proceed."
        else:
            return f"Unfavorable day for {activity}. Traditional wisdom suggests avoiding this activity today. Consider waiting for a more auspicious time."

    def _generate_explanation(
        self,
        auspiciousness: dict[str, Any],
        chinese_info: dict[str, Any],
        moon_data: dict[str, Any],
        activity: str,
    ) -> dict[str, Any]:
        """Generate detailed explanation of why a date is auspicious or not."""
        reasoning = []
        level = auspiciousness["level"]
        factors = auspiciousness.get("factors", {})

        # Zodiac day explanation
        zodiac_day = chinese_info.get("zodiac_day", "Unknown")
        zodiac_desc = {
            "Dragon": "powerful and ambitious energy, excellent for important ventures",
            "Tiger": "bold and courageous energy, good for taking initiative",
            "Horse": "dynamic and social energy, favorable for celebrations",
            "Rooster": "precise and communicative energy, good for negotiations",
            "Rabbit": "gentle and artistic energy, favorable for creative work",
            "Rat": "clever and resourceful energy, good for financial planning",
            "Ox": "steady and hardworking energy, excellent for construction",
            "Snake": "wise and strategic energy, good for planning",
            "Goat": "nurturing and creative energy, favorable for family matters",
            "Monkey": "innovative and playful energy, good for problem-solving",
            "Dog": "loyal and protective energy, favorable for security matters",
            "Pig": "generous and peaceful energy, good for rest and enjoyment",
        }
        if zodiac_day in zodiac_desc:
            reasoning.append(f"Zodiac day: {zodiac_day} - {zodiac_desc[zodiac_day]}")

        # Five element explanation
        five_element = chinese_info.get("five_element", "Unknown")
        element_bonus = factors.get("five_element_bonus", 0)
        element_desc = {
            "Wood": "represents growth, expansion, and new beginnings",
            "Fire": "represents energy, passion, and transformation",
            "Earth": "represents stability, grounding, and nurturing",
            "Metal": "represents precision, clarity, and refinement",
            "Water": "represents flow, adaptability, and wisdom",
        }
        if five_element in element_desc:
            effect = (
                "enhances"
                if element_bonus > 0
                else "neutral for" if element_bonus == 0 else "challenges"
            )
            reasoning.append(
                f"Five element: {five_element} - {element_desc[five_element]}, which {effect} your activity"
            )

        # Moon phase explanation
        moon_phase = moon_data.get("phase_name", "Unknown")
        moon_illumination = moon_data.get("illumination", 0)
        if moon_phase != "Unknown":
            if "Waxing" in moon_phase or "Full" in moon_phase:
                moon_effect = "increasing energy, favorable for growth and expansion"
            elif "Waning" in moon_phase or "New" in moon_phase:
                moon_effect = "decreasing energy, better for completion and reflection"
            else:
                moon_effect = "transitional energy"
            reasoning.append(
                f"Moon phase: {moon_phase} ({moon_illumination:.0%} illuminated) - {moon_effect}"
            )

        # Lunar mansion explanation
        lunar_mansion = chinese_info.get("lunar_mansion", "Unknown")
        mansion_effect = factors.get("lunar_mansion_effect", 5)
        if mansion_effect >= 8:
            reasoning.append(
                f"Lunar mansion: {lunar_mansion} - highly favorable for this activity"
            )
        elif mansion_effect <= 2:
            reasoning.append(
                f"Lunar mansion: {lunar_mansion} - not recommended for this activity"
            )
        else:
            reasoning.append(f"Lunar mansion: {lunar_mansion} - neutral influence")

        # Generate summary
        if level in ["very_good", "good"]:
            summary = f"This is a {level.replace('_', ' ')} day for {activity} because multiple traditional factors align favorably."
        elif level == "neutral":
            summary = (
                f"This is an average day for {activity} with mixed traditional factors."
            )
        else:
            summary = f"This is a {level.replace('_', ' ')} day for {activity} as traditional factors suggest caution."

        return {
            "summary": summary,
            "reasoning": reasoning,
            "score_breakdown": {
                "base_score": factors.get("lunar_mansion_effect", 0),
                "element_bonus": factors.get("five_element_bonus", 0),
                "zodiac_bonus": factors.get("zodiac_bonus", 0),
                "final_score": auspiciousness.get("score", 0),
            },
        }

    async def _find_alternative_dates(
        self,
        reference_date: datetime,
        activity: str,
        culture: str,
        days_to_check: int = 14,
    ) -> list[dict[str, Any]]:
        """Find better alternative dates near the reference date."""
        alternatives = []

        # Check dates within 2 weeks before and after
        for offset in range(1, days_to_check + 1):
            for direction in [1, -1]:  # Forward and backward
                check_date = reference_date + timedelta(days=offset * direction)
                date_str = check_date.strftime("%Y-%m-%d")

                try:
                    # Prevent recursive alternative searches
                    result = await self.check_date(
                        date_str, activity, culture, find_alternatives=False
                    )

                    # Only include dates with score >= 7
                    if result.get("score", 0) >= 7:
                        # Generate reason for being better
                        reason_parts = []
                        if result.get("zodiac_day"):
                            reason_parts.append(f"{result['zodiac_day']} day")
                        if result.get("five_elements"):
                            reason_parts.append(f"{result['five_elements']} element")
                        if result.get("moon_phase"):
                            reason_parts.append(f"{result['moon_phase']}")

                        reason = (
                            ", ".join(reason_parts)
                            if reason_parts
                            else "favorable traditional factors"
                        )

                        alternatives.append(
                            {
                                "date": date_str,
                                "score": result.get("score", 0),
                                "level": result.get("auspicious_level", "unknown"),
                                "reason": reason,
                                "days_away": offset * direction,
                            }
                        )

                except Exception:
                    continue

                # Stop after finding 3 good alternatives
                if len(alternatives) >= 3:
                    break

            if len(alternatives) >= 3:
                break

        # Sort by score (highest first)
        alternatives.sort(key=lambda x: x["score"], reverse=True)

        return alternatives[:3]  # Return top 3

    async def find_good_dates(
        self,
        start_date_str: str,
        end_date_str: str,
        activity: str,
        culture: str = "chinese",
        limit: int = 10,
    ) -> dict[str, Any]:
        """Find good dates for an activity within a date range."""
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            good_dates: list[dict[str, Any]] = []
            current_date = start_date

            while current_date <= end_date and len(good_dates) < limit:
                date_str = current_date.strftime("%Y-%m-%d")
                check_result = await self.check_date(date_str, activity, culture)

                if check_result.get("auspicious_level") in ["very_good", "good"]:
                    good_dates.append(
                        {
                            "date": date_str,
                            "level": check_result["auspicious_level"],
                            "score": check_result.get("score", 0),
                            "zodiac_day": check_result.get("zodiac_day"),
                            "lucky_hours": check_result.get("lucky_hours", []),
                            "moon_phase": check_result.get("moon_phase"),
                        }
                    )

                current_date += timedelta(days=1)

            # Sort by score (highest first)
            good_dates.sort(key=lambda x: x["score"], reverse=True)

            return {
                "activity": activity,
                "culture": culture,
                "search_period": f"{start_date_str} to {end_date_str}",
                "found_dates": len(good_dates),
                "good_dates": good_dates[:limit],
                "best_date": good_dates[0] if good_dates else None,
            }

        except Exception as e:
            return {"error": f"Failed to find good dates: {str(e)}"}

    async def get_daily_fortune(
        self, date_str: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Get daily fortune and luck information."""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            # Get Chinese calendar info
            chinese_info = self._get_chinese_calendar_info(date_obj)

            # Get moon phase info
            moon_data = await self.lunar_calc.get_moon_phase(date_str)

            # Calculate overall fortune
            fortune_score = 5  # Base score

            # Adjust based on lunar mansion
            lunar_mansion = chinese_info["lunar_mansion"]
            if lunar_mansion in [
                "角",
                "房",
                "心",
                "井",
            ]:  # Generally auspicious mansions
                fortune_score += 2
            elif lunar_mansion in [
                "尾",
                "箕",
                "危",
                "室",
            ]:  # Generally inauspicious mansions
                fortune_score -= 2

            # Adjust based on five elements
            five_element = chinese_info["five_element"]
            element_fortune = {
                "Wood": 1,  # Growth and vitality
                "Fire": 2,  # Energy and passion
                "Earth": 0,  # Stability (neutral)
                "Metal": -1,  # Cutting, separation
                "Water": 1,  # Flow and adaptability
            }
            fortune_score += element_fortune.get(five_element, 0)

            # Adjust based on moon phase
            moon_phase = moon_data.get("phase_name", "")
            if moon_phase in ["Full Moon", "Waxing Gibbous"]:
                fortune_score += 1
            elif moon_phase in ["New Moon", "Waning Crescent"]:
                fortune_score -= 1

            fortune_score = max(1, min(10, fortune_score))

            # Generate fortune level
            if fortune_score >= 8:
                fortune_level = "excellent"
                fortune_description = "A very auspicious day with excellent fortune. Great opportunities await."
            elif fortune_score >= 6:
                fortune_level = "good"
                fortune_description = (
                    "A favorable day with good fortune. Positive developments likely."
                )
            elif fortune_score >= 4:
                fortune_level = "average"
                fortune_description = (
                    "A balanced day with average fortune. Steady progress expected."
                )
            elif fortune_score >= 2:
                fortune_level = "challenging"
                fortune_description = (
                    "A challenging day requiring extra care. Proceed with caution."
                )
            else:
                fortune_level = "difficult"
                fortune_description = (
                    "A difficult day with obstacles. Best to wait for better times."
                )

            return {
                "date": date_str,
                "culture": culture,
                "fortune_level": fortune_level,
                "fortune_score": fortune_score,
                "description": fortune_description,
                "zodiac_day": chinese_info["zodiac_day"],
                "five_element": five_element,
                "lunar_mansion": lunar_mansion,
                "moon_phase": moon_phase,
                "lucky_colors": self._get_lucky_colors(five_element),
                "lucky_numbers": self._get_lucky_numbers(
                    chinese_info["sexagenary_day"]
                ),
                "lucky_directions": self._get_lucky_directions(
                    chinese_info["earthly_branch"]
                ),
                "advice": self._get_daily_advice(fortune_level, five_element),
            }

        except Exception as e:
            return {"error": f"Failed to get daily fortune: {str(e)}"}

    def _get_lucky_colors(self, element: str) -> list[str]:
        """Get lucky colors based on five elements."""
        color_map = {
            "Wood": ["green", "brown"],
            "Fire": ["red", "orange", "purple"],
            "Earth": ["yellow", "beige", "brown"],
            "Metal": ["white", "gold", "silver"],
            "Water": ["blue", "black", "gray"],
        }
        return color_map.get(element, ["white"])

    def _get_lucky_numbers(self, sexagenary_day: int) -> list[int]:
        """Get lucky numbers based on sexagenary cycle."""
        digits = [sexagenary_day % 10, (sexagenary_day + 5) % 10]
        normalized = {(digit or 10) for digit in digits}
        extended = {value + 10 for value in normalized if value + 10 <= 20}
        lucky_numbers = sorted(normalized.union(extended))
        return lucky_numbers if lucky_numbers else [8]

    def _get_lucky_directions(self, branch: str) -> list[str]:
        """Get lucky directions based on earthly branch."""
        direction_map = {
            "子": ["North"],
            "丑": ["Northeast"],
            "寅": ["Northeast"],
            "卯": ["East"],
            "辰": ["Southeast"],
            "巳": ["Southeast"],
            "午": ["South"],
            "未": ["Southwest"],
            "申": ["Southwest"],
            "酉": ["West"],
            "戌": ["Northwest"],
            "亥": ["Northwest"],
        }
        return direction_map.get(branch, ["Center"])

    def _get_daily_advice(self, fortune_level: str, element: str) -> str:
        """Get daily advice based on fortune and element."""
        base_advice = {
            "excellent": "Take advantage of this auspicious energy. Start important projects and make significant decisions.",
            "good": "A favorable day for progress. Focus on positive actions and maintain optimism.",
            "average": "Maintain steady effort. Good day for routine tasks and careful planning.",
            "challenging": "Exercise patience and caution. Avoid major decisions and conflicts.",
            "difficult": "Practice mindfulness and restraint. Focus on internal cultivation and preparation.",
        }

        element_advice = {
            "Wood": "Nurture growth and new beginnings. Plant seeds for future success.",
            "Fire": "Channel your energy positively. Good for communication and creative endeavors.",
            "Earth": "Focus on stability and grounding. Good for consolidation and organization.",
            "Metal": "Time for clarity and precision. Good for analysis and refinement.",
            "Water": "Embrace flexibility and flow. Good for adaptation and intuitive decisions.",
        }

        return f"{base_advice.get(fortune_level, '')} {element_advice.get(element, '')}"

    async def check_zodiac_compatibility(
        self, date1_str: str, date2_str: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Check zodiac compatibility between two dates."""
        try:
            date1_obj = datetime.strptime(date1_str, "%Y-%m-%d")
            date2_obj = datetime.strptime(date2_str, "%Y-%m-%d")

            chinese_info1 = self._get_chinese_calendar_info(date1_obj)
            chinese_info2 = self._get_chinese_calendar_info(date2_obj)

            zodiac1 = chinese_info1["zodiac_day"]
            zodiac2 = chinese_info2["zodiac_day"]

            # Traditional zodiac compatibility matrix
            compatibility_matrix = {
                "Rat": {
                    "best": ["Dragon", "Monkey"],
                    "good": ["Ox"],
                    "conflict": ["Horse"],
                    "harm": ["Goat"],
                },
                "Ox": {
                    "best": ["Snake", "Rooster"],
                    "good": ["Rat"],
                    "conflict": ["Goat"],
                    "harm": ["Horse"],
                },
                "Tiger": {
                    "best": ["Horse", "Dog"],
                    "good": ["Pig"],
                    "conflict": ["Monkey"],
                    "harm": ["Snake"],
                },
                "Rabbit": {
                    "best": ["Goat", "Pig"],
                    "good": ["Dog"],
                    "conflict": ["Rooster"],
                    "harm": ["Dragon"],
                },
                "Dragon": {
                    "best": ["Rat", "Monkey"],
                    "good": ["Rooster"],
                    "conflict": ["Dog"],
                    "harm": ["Rabbit"],
                },
                "Snake": {
                    "best": ["Ox", "Rooster"],
                    "good": ["Monkey"],
                    "conflict": ["Pig"],
                    "harm": ["Tiger"],
                },
                "Horse": {
                    "best": ["Tiger", "Dog"],
                    "good": ["Goat"],
                    "conflict": ["Rat"],
                    "harm": ["Ox"],
                },
                "Goat": {
                    "best": ["Rabbit", "Pig"],
                    "good": ["Horse"],
                    "conflict": ["Ox"],
                    "harm": ["Rat"],
                },
                "Monkey": {
                    "best": ["Rat", "Dragon"],
                    "good": ["Snake"],
                    "conflict": ["Tiger"],
                    "harm": ["Pig"],
                },
                "Rooster": {
                    "best": ["Ox", "Snake"],
                    "good": ["Dragon"],
                    "conflict": ["Rabbit"],
                    "harm": ["Dog"],
                },
                "Dog": {
                    "best": ["Tiger", "Horse"],
                    "good": ["Rabbit"],
                    "conflict": ["Dragon"],
                    "harm": ["Rooster"],
                },
                "Pig": {
                    "best": ["Rabbit", "Goat"],
                    "good": ["Tiger"],
                    "conflict": ["Snake"],
                    "harm": ["Monkey"],
                },
            }

            compatibility = compatibility_matrix.get(zodiac1, {})

            if zodiac2 in compatibility.get("best", []):
                level = "excellent"
                description = f"{zodiac1} and {zodiac2} form an excellent compatibility. Perfect harmony and mutual support."
            elif zodiac2 in compatibility.get("good", []):
                level = "good"
                description = f"{zodiac1} and {zodiac2} have good compatibility. Generally harmonious relationship."
            elif zodiac2 in compatibility.get("conflict", []):
                level = "conflict"
                description = f"{zodiac1} and {zodiac2} may experience conflicts. Requires understanding and compromise."
            elif zodiac2 in compatibility.get("harm", []):
                level = "challenging"
                description = f"{zodiac1} and {zodiac2} may face challenges. Extra care needed in interactions."
            else:
                level = "neutral"
                description = f"{zodiac1} and {zodiac2} have neutral compatibility. Average relationship dynamics."

            return {
                "date1": date1_str,
                "date2": date2_str,
                "zodiac1": zodiac1,
                "zodiac2": zodiac2,
                "compatibility_level": level,
                "description": description,
                "culture": culture,
                "element1": chinese_info1["five_element"],
                "element2": chinese_info2["five_element"],
                "element_relationship": self._check_element_compatibility(
                    chinese_info1["five_element"], chinese_info2["five_element"]
                ),
                "recommendations": self._get_compatibility_recommendations(level),
            }

        except Exception as e:
            return {"error": f"Failed to check zodiac compatibility: {str(e)}"}

    def _check_element_compatibility(
        self, element1: str, element2: str
    ) -> dict[str, str]:
        """Check five elements compatibility."""
        relation1 = self.element_relationships.get(element1, {})

        if element2 == relation1.get("generates"):
            return {
                "type": "generative",
                "description": f"{element1} generates {element2} - very harmonious",
            }
        elif element2 == relation1.get("generated_by"):
            return {
                "type": "supportive",
                "description": f"{element1} is supported by {element2} - harmonious",
            }
        elif element2 == relation1.get("destroys"):
            return {
                "type": "destructive",
                "description": f"{element1} destroys {element2} - conflicting",
            }
        elif element2 == relation1.get("destroyed_by"):
            return {
                "type": "weakening",
                "description": f"{element1} is weakened by {element2} - challenging",
            }
        else:
            return {
                "type": "neutral",
                "description": f"{element1} and {element2} have neutral relationship",
            }

    def _get_compatibility_recommendations(self, level: str) -> str:
        """Get recommendations based on compatibility level."""
        recommendations = {
            "excellent": "Perfect match! Proceed with confidence. This combination brings out the best in both parties.",
            "good": "Good compatibility. Communication and mutual respect will enhance the relationship.",
            "neutral": "Average compatibility. Success depends on effort and understanding from both sides.",
            "conflict": "Potential challenges ahead. Focus on compromise and finding common ground.",
            "challenging": "Difficult combination. Consider whether the benefits outweigh the challenges.",
        }
        return recommendations.get(level, "No specific recommendations available.")
