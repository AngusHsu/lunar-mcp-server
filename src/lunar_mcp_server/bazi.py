"""
BaZi (八字) - Four Pillars of Destiny Calculator

This module provides comprehensive BaZi (Eight Characters) calculations based on
traditional Chinese fortune-telling methods. BaZi analyzes the four pillars
(year, month, day, and hour) to determine a person's destiny and characteristics.
"""

from datetime import datetime, timedelta
from typing import Any


class BaZiCalculator:
    """Calculator for BaZi (Four Pillars of Destiny)."""

    def __init__(self) -> None:
        """Initialize the BaZi calculator with traditional Chinese calendar data."""
        # Heavenly Stems (天干) - 10 stems
        self.heavenly_stems = [
            ("甲", "Jia", "Wood", "Yang"),
            ("乙", "Yi", "Wood", "Yin"),
            ("丙", "Bing", "Fire", "Yang"),
            ("丁", "Ding", "Fire", "Yin"),
            ("戊", "Wu", "Earth", "Yang"),
            ("己", "Ji", "Earth", "Yin"),
            ("庚", "Geng", "Metal", "Yang"),
            ("辛", "Xin", "Metal", "Yin"),
            ("壬", "Ren", "Water", "Yang"),
            ("癸", "Gui", "Water", "Yin"),
        ]

        # Earthly Branches (地支) - 12 branches
        self.earthly_branches = [
            ("子", "Zi", "Rat", "Water", "Yang"),
            ("丑", "Chou", "Ox", "Earth", "Yin"),
            ("寅", "Yin", "Tiger", "Wood", "Yang"),
            ("卯", "Mao", "Rabbit", "Wood", "Yin"),
            ("辰", "Chen", "Dragon", "Earth", "Yang"),
            ("巳", "Si", "Snake", "Fire", "Yin"),
            ("午", "Wu", "Horse", "Fire", "Yang"),
            ("未", "Wei", "Goat", "Earth", "Yin"),
            ("申", "Shen", "Monkey", "Metal", "Yang"),
            ("酉", "You", "Rooster", "Metal", "Yin"),
            ("戌", "Xu", "Dog", "Earth", "Yang"),
            ("亥", "Hai", "Pig", "Water", "Yin"),
        ]

        # Reference date for stem-branch calculation
        # February 4, 1984 was 甲子 (Jia-Zi) day
        self.reference_date = datetime(1984, 2, 4)
        self.reference_stem_branch = (0, 0)  # Jia-Zi

    def _get_stem_branch_index(
        self, days_offset: int, reference: tuple[int, int] = (0, 0)
    ) -> tuple[int, int]:
        """
        Calculate stem and branch indices based on days offset.

        Args:
            days_offset: Number of days from reference date
            reference: Reference stem and branch indices (default: Jia-Zi)

        Returns:
            Tuple of (stem_index, branch_index)
        """
        stem_index = (reference[0] + days_offset) % 10
        branch_index = (reference[1] + days_offset) % 12
        return (stem_index, branch_index)

    def _get_year_pillar(self, birth_date: datetime) -> dict[str, Any]:
        """
        Calculate the Year Pillar (年柱).

        The year pillar changes on Chinese New Year (around Feb 4).

        Args:
            birth_date: Birth datetime

        Returns:
            Dictionary containing year pillar information
        """
        year = birth_date.year

        # Check if before spring begins (立春, around Feb 4)
        # If before Feb 4, use previous year's pillar
        spring_begins = datetime(year, 2, 4)
        if birth_date < spring_begins:
            year -= 1

        # Calculate stem and branch for the year
        # Reference: 1984 was 甲子 (Jia-Zi)
        year_offset = year - 1984
        stem_idx = year_offset % 10
        branch_idx = year_offset % 12

        stem = self.heavenly_stems[stem_idx]
        branch = self.earthly_branches[branch_idx]

        return {
            "pillar_type": "Year",
            "chinese_name": "年柱",
            "stem": {
                "chinese": stem[0],
                "pinyin": stem[1],
                "element": stem[2],
                "polarity": stem[3],
            },
            "branch": {
                "chinese": branch[0],
                "pinyin": branch[1],
                "zodiac": branch[2],
                "element": branch[3],
                "polarity": branch[4],
            },
            "pillar": f"{stem[0]}{branch[0]}",
            "pinyin": f"{stem[1]}-{branch[1]}",
            "meaning": "Represents ancestors, early life (0-15 years), and inherited characteristics",
        }

    def _get_month_pillar(self, birth_date: datetime) -> dict[str, Any]:
        """
        Calculate the Month Pillar (月柱).

        The month pillar is based on solar terms, not calendar months.

        Args:
            birth_date: Birth datetime

        Returns:
            Dictionary containing month pillar information
        """
        month = birth_date.month
        day = birth_date.day

        # Solar term boundaries (approximate dates)
        # Format: (month_num, start_day, stem_offset, branch_index)
        solar_terms = [
            (2, 4, 2, 2),  # 立春 Li Chun (Feb 4) - Tiger month
            (3, 6, 3, 3),  # 惊蛰 Jing Zhe (Mar 6) - Rabbit month
            (4, 5, 4, 4),  # 清明 Qing Ming (Apr 5) - Dragon month
            (5, 6, 5, 5),  # 立夏 Li Xia (May 6) - Snake month
            (6, 6, 6, 6),  # 芒种 Mang Zhong (Jun 6) - Horse month
            (7, 7, 7, 7),  # 小暑 Xiao Shu (Jul 7) - Goat month
            (8, 8, 8, 8),  # 立秋 Li Qiu (Aug 8) - Monkey month
            (9, 8, 9, 9),  # 白露 Bai Lu (Sep 8) - Rooster month
            (10, 8, 10, 10),  # 寒露 Han Lu (Oct 8) - Dog month
            (11, 7, 11, 11),  # 立冬 Li Dong (Nov 7) - Pig month
            (12, 7, 0, 0),  # 大雪 Da Xue (Dec 7) - Rat month
            (1, 6, 1, 1),  # 小寒 Xiao Han (Jan 6) - Ox month
        ]

        # Find current solar term month
        branch_idx = 0

        for term_month, term_day, _s_offset, b_idx in solar_terms:
            if (
                month == term_month
                and day >= term_day
                or month == (term_month % 12) + 1
                and day < term_day
            ):
                branch_idx = b_idx
                break

        # Calculate stem based on year stem
        year_pillar = self._get_year_pillar(birth_date)
        year_stem_chinese = year_pillar["stem"]["chinese"]

        # Find year stem index
        year_stem_idx = 0
        for idx, stem in enumerate(self.heavenly_stems):
            if stem[0] == year_stem_chinese:
                year_stem_idx = idx
                break

        # Month stem formula based on year stem
        # 甲己 years: start from 丙 (2)
        # 乙庚 years: start from 戊 (4)
        # 丙辛 years: start from 庚 (6)
        # 丁壬 years: start from 壬 (8)
        # 戊癸 years: start from 甲 (0)
        month_stem_base_map = {
            0: 2,
            1: 4,
            2: 6,
            3: 8,
            4: 0,
            5: 2,
            6: 4,
            7: 6,
            8: 8,
            9: 0,
        }
        month_stem_base = month_stem_base_map[year_stem_idx % 5 * 2]

        stem_idx = (month_stem_base + branch_idx) % 10

        stem = self.heavenly_stems[stem_idx]
        branch = self.earthly_branches[branch_idx]

        return {
            "pillar_type": "Month",
            "chinese_name": "月柱",
            "stem": {
                "chinese": stem[0],
                "pinyin": stem[1],
                "element": stem[2],
                "polarity": stem[3],
            },
            "branch": {
                "chinese": branch[0],
                "pinyin": branch[1],
                "zodiac": branch[2],
                "element": branch[3],
                "polarity": branch[4],
            },
            "pillar": f"{stem[0]}{branch[0]}",
            "pinyin": f"{stem[1]}-{branch[1]}",
            "meaning": "Represents parents, youth (16-30 years), and career development",
        }

    def _get_day_pillar(self, birth_date: datetime) -> dict[str, Any]:
        """
        Calculate the Day Pillar (日柱).

        The day pillar follows a 60-day cycle (Sexagenary cycle).

        Args:
            birth_date: Birth datetime

        Returns:
            Dictionary containing day pillar information
        """
        # Calculate days from reference date
        days_diff = (birth_date.date() - self.reference_date.date()).days

        stem_idx, branch_idx = self._get_stem_branch_index(
            days_diff, self.reference_stem_branch
        )

        stem = self.heavenly_stems[stem_idx]
        branch = self.earthly_branches[branch_idx]

        return {
            "pillar_type": "Day",
            "chinese_name": "日柱",
            "stem": {
                "chinese": stem[0],
                "pinyin": stem[1],
                "element": stem[2],
                "polarity": stem[3],
            },
            "branch": {
                "chinese": branch[0],
                "pinyin": branch[1],
                "zodiac": branch[2],
                "element": branch[3],
                "polarity": branch[4],
            },
            "pillar": f"{stem[0]}{branch[0]}",
            "pinyin": f"{stem[1]}-{branch[1]}",
            "meaning": "Represents self, spouse, middle age (31-45 years), and marriage",
            "day_master": {
                "element": stem[2],
                "polarity": stem[3],
                "description": f"Day Master is {stem[2]} {stem[3]}, representing core self",
            },
        }

    def _get_hour_pillar(self, birth_date: datetime) -> dict[str, Any]:
        """
        Calculate the Hour Pillar (时柱).

        Each Chinese hour is 2 hours, and there are 12 branches for 24 hours.

        Args:
            birth_date: Birth datetime

        Returns:
            Dictionary containing hour pillar information
        """
        hour = birth_date.hour

        # Map hour to branch index
        # 子时 (Zi): 23:00-01:00 -> branch 0
        # 丑时 (Chou): 01:00-03:00 -> branch 1
        # etc.
        if hour == 23:
            branch_idx = 0
        else:
            branch_idx = (hour + 1) // 2

        # Get day stem for hour stem calculation
        day_pillar = self._get_day_pillar(birth_date)
        day_stem_chinese = day_pillar["stem"]["chinese"]

        # Find day stem index
        day_stem_idx = 0
        for idx, stem in enumerate(self.heavenly_stems):
            if stem[0] == day_stem_chinese:
                day_stem_idx = idx
                break

        # Hour stem formula based on day stem
        # Same pattern as month stem calculation
        hour_stem_base_map = {
            0: 0,
            1: 2,
            2: 4,
            3: 6,
            4: 8,
            5: 0,
            6: 2,
            7: 4,
            8: 6,
            9: 8,
        }
        hour_stem_base = hour_stem_base_map[day_stem_idx]

        stem_idx = (hour_stem_base + branch_idx) % 10

        stem = self.heavenly_stems[stem_idx]
        branch = self.earthly_branches[branch_idx]

        # Hour ranges
        hour_ranges = [
            "23:00-01:00",
            "01:00-03:00",
            "03:00-05:00",
            "05:00-07:00",
            "07:00-09:00",
            "09:00-11:00",
            "11:00-13:00",
            "13:00-15:00",
            "15:00-17:00",
            "17:00-19:00",
            "19:00-21:00",
            "21:00-23:00",
        ]

        return {
            "pillar_type": "Hour",
            "chinese_name": "时柱",
            "stem": {
                "chinese": stem[0],
                "pinyin": stem[1],
                "element": stem[2],
                "polarity": stem[3],
            },
            "branch": {
                "chinese": branch[0],
                "pinyin": branch[1],
                "zodiac": branch[2],
                "element": branch[3],
                "polarity": branch[4],
            },
            "pillar": f"{stem[0]}{branch[0]}",
            "pinyin": f"{stem[1]}-{branch[1]}",
            "hour_range": hour_ranges[branch_idx],
            "meaning": "Represents children, later life (46+ years), and legacy",
        }

    def _analyze_elements(self, four_pillars: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Analyze the five elements distribution in the four pillars.

        Args:
            four_pillars: List of four pillar dictionaries

        Returns:
            Dictionary containing element analysis
        """
        element_count = {"Wood": 0, "Fire": 0, "Earth": 0, "Metal": 0, "Water": 0}

        # Count elements from all stems and branches
        for pillar in four_pillars:
            stem_element = pillar["stem"]["element"]
            branch_element = pillar["branch"]["element"]

            element_count[stem_element] += 1
            element_count[branch_element] += 1

        # Determine strongest and weakest elements
        strongest = max(element_count.items(), key=lambda x: x[1])
        weakest = min(element_count.items(), key=lambda x: x[1])

        # Element relationships
        generation_cycle = {
            "Wood": "Fire",
            "Fire": "Earth",
            "Earth": "Metal",
            "Metal": "Water",
            "Water": "Wood",
        }

        control_cycle = {
            "Wood": "Earth",
            "Fire": "Metal",
            "Earth": "Water",
            "Metal": "Wood",
            "Water": "Fire",
        }

        return {
            "element_distribution": element_count,
            "strongest_element": {"element": strongest[0], "count": strongest[1]},
            "weakest_element": {"element": weakest[0], "count": weakest[1]},
            "balance_analysis": self._get_balance_description(element_count),
            "generation_cycle": generation_cycle,
            "control_cycle": control_cycle,
            "recommendations": self._get_element_recommendations(
                element_count, strongest[0], weakest[0]
            ),
        }

    def _get_balance_description(self, element_count: dict[str, int]) -> str:
        """Get description of elemental balance."""
        max_count = max(element_count.values())
        min_count = min(element_count.values())

        if max_count - min_count <= 2:
            return "Well-balanced: Elements are evenly distributed, indicating harmony"
        elif max_count - min_count <= 4:
            return "Moderately balanced: Some elements dominate, but overall acceptable"
        else:
            return "Imbalanced: Significant disparity in elements, may need adjustment"

    def _get_element_recommendations(
        self, element_count: dict[str, int], strongest: str, weakest: str
    ) -> dict[str, Any]:
        """Get recommendations based on element analysis."""
        recommendations = {
            "enhance_element": weakest,
            "reduce_element": strongest if element_count[strongest] > 3 else None,
            "favorable_colors": self._get_element_colors(weakest),
            "favorable_directions": self._get_element_directions(weakest),
            "career_suggestions": self._get_element_careers(strongest),
        }

        return recommendations

    def _get_element_colors(self, element: str) -> list[str]:
        """Get favorable colors for an element."""
        color_map = {
            "Wood": ["green", "cyan", "teal"],
            "Fire": ["red", "orange", "purple"],
            "Earth": ["yellow", "brown", "beige"],
            "Metal": ["white", "gold", "silver"],
            "Water": ["black", "blue", "navy"],
        }
        return color_map.get(element, [])

    def _get_element_directions(self, element: str) -> list[str]:
        """Get favorable directions for an element."""
        direction_map = {
            "Wood": ["East", "Southeast"],
            "Fire": ["South"],
            "Earth": ["Center", "Southwest", "Northeast"],
            "Metal": ["West", "Northwest"],
            "Water": ["North"],
        }
        return direction_map.get(element, [])

    def _get_element_careers(self, element: str) -> list[str]:
        """Get suitable career paths based on element."""
        career_map = {
            "Wood": [
                "education",
                "arts",
                "forestry",
                "textiles",
                "publishing",
                "growth industries",
            ],
            "Fire": [
                "entertainment",
                "media",
                "restaurants",
                "energy",
                "lighting",
                "publicity",
            ],
            "Earth": [
                "real estate",
                "construction",
                "agriculture",
                "mining",
                "ceramics",
                "land management",
            ],
            "Metal": [
                "finance",
                "banking",
                "machinery",
                "automotive",
                "hardware",
                "law enforcement",
            ],
            "Water": [
                "transportation",
                "shipping",
                "communication",
                "beverage",
                "tourism",
                "consulting",
            ],
        }
        return career_map.get(element, [])

    async def calculate_bazi(
        self, birth_datetime_str: str, timezone_offset: int = 8
    ) -> dict[str, Any]:
        """
        Calculate complete BaZi (Four Pillars of Destiny).

        Args:
            birth_datetime_str: Birth datetime in format "YYYY-MM-DD HH:MM"
            timezone_offset: Timezone offset in hours (default: +8 for China)

        Returns:
            Dictionary containing complete BaZi analysis
        """
        try:
            # Parse birth datetime
            birth_dt = datetime.strptime(birth_datetime_str, "%Y-%m-%d %H:%M")

            # Adjust for timezone (convert to China standard time if needed)
            # BaZi is traditionally calculated using China time zone
            birth_dt_adjusted = birth_dt + timedelta(hours=8 - timezone_offset)

            # Calculate four pillars
            year_pillar = self._get_year_pillar(birth_dt_adjusted)
            month_pillar = self._get_month_pillar(birth_dt_adjusted)
            day_pillar = self._get_day_pillar(birth_dt_adjusted)
            hour_pillar = self._get_hour_pillar(birth_dt_adjusted)

            four_pillars = [year_pillar, month_pillar, day_pillar, hour_pillar]

            # Analyze elements
            element_analysis = self._analyze_elements(four_pillars)

            # Get the eight characters (四柱八字)
            eight_characters = "".join([p["pillar"] for p in four_pillars])

            # Get day master (日主/日元)
            day_master = day_pillar["day_master"]

            return {
                "birth_datetime": birth_datetime_str,
                "timezone_offset": timezone_offset,
                "adjusted_datetime": birth_dt_adjusted.strftime("%Y-%m-%d %H:%M"),
                "eight_characters": eight_characters,
                "four_pillars": {
                    "year": year_pillar,
                    "month": month_pillar,
                    "day": day_pillar,
                    "hour": hour_pillar,
                },
                "day_master": day_master,
                "element_analysis": element_analysis,
                "life_stages": {
                    "early_life": f"Influenced by {year_pillar['pillar']} (Year Pillar)",
                    "youth": f"Influenced by {month_pillar['pillar']} (Month Pillar)",
                    "middle_age": f"Influenced by {day_pillar['pillar']} (Day Pillar)",
                    "later_life": f"Influenced by {hour_pillar['pillar']} (Hour Pillar)",
                },
                "interpretation": {
                    "character": f"Day Master {day_master['element']} {day_master['polarity']} suggests "
                    + self._get_day_master_description(
                        day_master["element"], day_master["polarity"]
                    ),
                    "overall": "The Four Pillars reveal the cosmic energies present at birth, "
                    "shaping personality, destiny, and life path.",
                },
            }

        except ValueError as e:
            return {
                "error": f"Invalid datetime format. Use YYYY-MM-DD HH:MM. Error: {str(e)}"
            }
        except Exception as e:
            return {"error": f"Failed to calculate BaZi: {str(e)}"}

    def _get_day_master_description(self, element: str, polarity: str) -> str:
        """Get personality description based on Day Master."""
        descriptions = {
            "Wood": {
                "Yang": "strong growth potential, ambitious, straightforward, and pioneering spirit",
                "Yin": "gentle flexibility, artistic talent, adaptability, and diplomatic nature",
            },
            "Fire": {
                "Yang": "passionate energy, enthusiasm, leadership, and radiant personality",
                "Yin": "warm-hearted, cultural refinement, attention to detail, and nurturing spirit",
            },
            "Earth": {
                "Yang": "stable foundation, reliability, practical wisdom, and protective nature",
                "Yin": "patient cultivation, attention to detail, supportive character, and organizational skills",
            },
            "Metal": {
                "Yang": "strong principles, determination, justice-oriented, and reformative spirit",
                "Yin": "refined elegance, attention to quality, artistic sensibility, and introspective nature",
            },
            "Water": {
                "Yang": "flowing wisdom, adaptability, intelligence, and pioneering communication skills",
                "Yin": "deep intuition, gentle persistence, scholarly nature, and reflective wisdom",
            },
        }
        return descriptions.get(element, {}).get(polarity, "unique characteristics")

    async def get_compatibility(
        self, bazi1_datetime: str, bazi2_datetime: str, timezone_offset: int = 8
    ) -> dict[str, Any]:
        """
        Calculate compatibility between two BaZi charts.

        Args:
            bazi1_datetime: First person's birth datetime
            bazi2_datetime: Second person's birth datetime
            timezone_offset: Timezone offset in hours

        Returns:
            Dictionary containing compatibility analysis
        """
        try:
            # Calculate both BaZi charts
            bazi1 = await self.calculate_bazi(bazi1_datetime, timezone_offset)
            bazi2 = await self.calculate_bazi(bazi2_datetime, timezone_offset)

            if "error" in bazi1 or "error" in bazi2:
                return {"error": "Failed to calculate one or both BaZi charts"}

            # Analyze element compatibility
            dm1 = bazi1["day_master"]["element"]
            dm2 = bazi2["day_master"]["element"]

            # Element relationship scoring
            generation = {
                "Wood": "Fire",
                "Fire": "Earth",
                "Earth": "Metal",
                "Metal": "Water",
                "Water": "Wood",
            }
            control = {
                "Wood": "Earth",
                "Fire": "Metal",
                "Earth": "Water",
                "Metal": "Wood",
                "Water": "Fire",
            }

            score = 5  # Base score

            # Check if elements support each other
            if generation.get(dm1) == dm2:
                score += 3
                relationship = f"{dm1} generates {dm2} - supportive relationship"
            elif generation.get(dm2) == dm1:
                score += 3
                relationship = f"{dm2} generates {dm1} - supportive relationship"
            elif control.get(dm1) == dm2:
                score -= 2
                relationship = f"{dm1} controls {dm2} - challenging dynamic"
            elif control.get(dm2) == dm1:
                score -= 2
                relationship = f"{dm2} controls {dm1} - challenging dynamic"
            elif dm1 == dm2:
                score += 1
                relationship = f"Both are {dm1} - similar nature"
            else:
                relationship = "Neutral relationship"

            # Ensure score is within 0-10
            score = max(0, min(10, score))

            compatibility_level = (
                "Excellent"
                if score >= 8
                else "Good" if score >= 6 else "Fair" if score >= 4 else "Challenging"
            )

            return {
                "person1": {
                    "datetime": bazi1_datetime,
                    "day_master": bazi1["day_master"],
                    "eight_characters": bazi1["eight_characters"],
                },
                "person2": {
                    "datetime": bazi2_datetime,
                    "day_master": bazi2["day_master"],
                    "eight_characters": bazi2["eight_characters"],
                },
                "compatibility_score": score,
                "compatibility_level": compatibility_level,
                "element_relationship": relationship,
                "analysis": {
                    "strengths": self._get_compatibility_strengths(dm1, dm2),
                    "challenges": self._get_compatibility_challenges(dm1, dm2),
                    "recommendations": "Focus on mutual understanding and leveraging complementary strengths",
                },
            }

        except Exception as e:
            return {"error": f"Failed to calculate compatibility: {str(e)}"}

    def _get_compatibility_strengths(self, element1: str, element2: str) -> list[str]:
        """Get relationship strengths based on elements."""
        return [
            "Mutual respect and understanding",
            "Balanced energy exchange",
            "Complementary characteristics",
        ]

    def _get_compatibility_challenges(self, element1: str, element2: str) -> list[str]:
        """Get relationship challenges based on elements."""
        return [
            "Different approaches to life",
            "Need for compromise",
            "Communication is key",
        ]
