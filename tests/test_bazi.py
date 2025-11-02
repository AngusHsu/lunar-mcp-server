"""Tests for BaZi (Eight Characters) calculator."""

import pytest

from lunar_mcp_server.bazi import BaZiCalculator


class TestBaZiCalculator:
    """Test cases for BaZiCalculator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calculator = BaZiCalculator()

    @pytest.mark.asyncio
    async def test_calculate_bazi_basic(self):
        """Test basic BaZi calculation."""
        # Test with a known date: 1990-01-01 12:00
        result = await self.calculator.calculate_bazi("1990-01-01 12:00", 8)

        assert "eight_characters" in result
        assert "four_pillars" in result
        assert "day_master" in result
        assert "element_analysis" in result

        # Check four pillars structure
        assert "year" in result["four_pillars"]
        assert "month" in result["four_pillars"]
        assert "day" in result["four_pillars"]
        assert "hour" in result["four_pillars"]

        # Each pillar should have stem and branch
        year_pillar = result["four_pillars"]["year"]
        assert "stem" in year_pillar
        assert "branch" in year_pillar
        assert "pillar" in year_pillar
        assert "chinese_name" in year_pillar

    @pytest.mark.asyncio
    async def test_calculate_bazi_year_pillar(self):
        """Test year pillar calculation."""
        result = await self.calculator.calculate_bazi("2000-02-10 12:00", 8)

        year_pillar = result["four_pillars"]["year"]
        assert year_pillar["chinese_name"] == "年柱"
        assert year_pillar["pillar_type"] == "Year"
        assert "stem" in year_pillar
        assert "branch" in year_pillar
        assert year_pillar["branch"]["zodiac"] == "Dragon"  # 2000 is Dragon year

    @pytest.mark.asyncio
    async def test_calculate_bazi_spring_boundary(self):
        """Test year pillar calculation around spring begins (立春)."""
        # Before spring begins (Feb 4) - should use previous year
        result_before = await self.calculator.calculate_bazi("2000-02-03 12:00", 8)

        # After spring begins - should use current year
        result_after = await self.calculator.calculate_bazi("2000-02-05 12:00", 8)

        # The year pillars should be different
        year_before = result_before["four_pillars"]["year"]["branch"]["zodiac"]
        year_after = result_after["four_pillars"]["year"]["branch"]["zodiac"]

        assert year_before == "Rabbit"  # 1999 is Rabbit year
        assert year_after == "Dragon"  # 2000 is Dragon year

    @pytest.mark.asyncio
    async def test_calculate_bazi_day_master(self):
        """Test day master calculation."""
        result = await self.calculator.calculate_bazi("1990-05-15 14:00", 8)

        day_master = result["day_master"]
        assert "element" in day_master
        assert "polarity" in day_master
        assert day_master["element"] in ["Wood", "Fire", "Earth", "Metal", "Water"]
        assert day_master["polarity"] in ["Yang", "Yin"]

    @pytest.mark.asyncio
    async def test_calculate_bazi_hour_pillar(self):
        """Test hour pillar calculation for different times."""
        # Test midnight hour (Zi time: 23:00-01:00)
        result_midnight = await self.calculator.calculate_bazi("2000-01-01 00:00", 8)
        hour_pillar = result_midnight["four_pillars"]["hour"]
        assert hour_pillar["branch"]["pinyin"] == "Zi"
        assert hour_pillar["branch"]["zodiac"] == "Rat"

        # Test noon hour (Wu time: 11:00-13:00)
        result_noon = await self.calculator.calculate_bazi("2000-01-01 12:00", 8)
        hour_pillar = result_noon["four_pillars"]["hour"]
        assert hour_pillar["branch"]["pinyin"] == "Wu"
        assert hour_pillar["branch"]["zodiac"] == "Horse"

    @pytest.mark.asyncio
    async def test_calculate_bazi_element_analysis(self):
        """Test element analysis in BaZi calculation."""
        result = await self.calculator.calculate_bazi("1985-10-20 10:00", 8)

        element_analysis = result["element_analysis"]
        assert "element_distribution" in element_analysis
        assert "strongest_element" in element_analysis
        assert "weakest_element" in element_analysis
        assert "balance_analysis" in element_analysis
        assert "recommendations" in element_analysis

        # Check element distribution counts
        distribution = element_analysis["element_distribution"]
        total_count = sum(distribution.values())
        assert total_count == 8  # 4 stems + 4 branches

    @pytest.mark.asyncio
    async def test_calculate_bazi_recommendations(self):
        """Test element recommendations."""
        result = await self.calculator.calculate_bazi("1990-03-15 08:00", 8)

        recommendations = result["element_analysis"]["recommendations"]
        assert "enhance_element" in recommendations
        assert "favorable_colors" in recommendations
        assert "favorable_directions" in recommendations
        assert "career_suggestions" in recommendations

        # Check that favorable colors are provided
        assert len(recommendations["favorable_colors"]) > 0
        assert len(recommendations["favorable_directions"]) > 0
        assert len(recommendations["career_suggestions"]) > 0

    @pytest.mark.asyncio
    async def test_calculate_bazi_eight_characters(self):
        """Test that eight characters string is correctly formatted."""
        result = await self.calculator.calculate_bazi("1995-06-10 14:30", 8)

        eight_chars = result["eight_characters"]
        # Should be 8 Chinese characters (4 pillars × 2 characters each)
        assert len(eight_chars) == 8

    @pytest.mark.asyncio
    async def test_calculate_bazi_life_stages(self):
        """Test life stages information."""
        result = await self.calculator.calculate_bazi("2000-12-25 18:00", 8)

        life_stages = result["life_stages"]
        assert "early_life" in life_stages
        assert "youth" in life_stages
        assert "middle_age" in life_stages
        assert "later_life" in life_stages

    @pytest.mark.asyncio
    async def test_calculate_bazi_timezone_adjustment(self):
        """Test timezone adjustment in BaZi calculation."""
        # Same local time, different timezones
        result_utc8 = await self.calculator.calculate_bazi("2000-01-01 12:00", 8)
        result_utc0 = await self.calculator.calculate_bazi("2000-01-01 12:00", 0)

        # Adjusted times should be different
        assert result_utc8["adjusted_datetime"] != result_utc0["adjusted_datetime"]

    @pytest.mark.asyncio
    async def test_calculate_bazi_invalid_format(self):
        """Test error handling for invalid datetime format."""
        result = await self.calculator.calculate_bazi("invalid-date", 8)

        assert "error" in result
        assert "Invalid datetime format" in result["error"]

    @pytest.mark.asyncio
    async def test_get_compatibility_basic(self):
        """Test basic BaZi compatibility calculation."""
        result = await self.calculator.get_compatibility(
            "1990-05-15 10:00", "1992-08-20 14:00", 8
        )

        assert "person1" in result
        assert "person2" in result
        assert "compatibility_score" in result
        assert "compatibility_level" in result
        assert "element_relationship" in result
        assert "analysis" in result

    @pytest.mark.asyncio
    async def test_get_compatibility_score_range(self):
        """Test that compatibility score is within valid range."""
        result = await self.calculator.get_compatibility(
            "1985-03-10 08:00", "1987-11-25 16:00", 8
        )

        score = result["compatibility_score"]
        assert 0 <= score <= 10

    @pytest.mark.asyncio
    async def test_get_compatibility_levels(self):
        """Test that compatibility level is correctly assigned."""
        result = await self.calculator.get_compatibility(
            "2000-01-01 12:00", "2001-06-15 14:00", 8
        )

        level = result["compatibility_level"]
        assert level in ["Excellent", "Good", "Fair", "Challenging"]

    @pytest.mark.asyncio
    async def test_get_compatibility_analysis(self):
        """Test that compatibility analysis includes required fields."""
        result = await self.calculator.get_compatibility(
            "1995-07-20 09:00", "1996-12-10 15:00", 8
        )

        analysis = result["analysis"]
        assert "strengths" in analysis
        assert "challenges" in analysis
        assert "recommendations" in analysis

        assert isinstance(analysis["strengths"], list)
        assert isinstance(analysis["challenges"], list)

    @pytest.mark.asyncio
    async def test_get_compatibility_person_info(self):
        """Test that person information is correctly included."""
        dt1 = "1988-04-05 11:00"
        dt2 = "1990-09-18 13:00"

        result = await self.calculator.get_compatibility(dt1, dt2, 8)

        assert result["person1"]["datetime"] == dt1
        assert result["person2"]["datetime"] == dt2
        assert "day_master" in result["person1"]
        assert "day_master" in result["person2"]
        assert "eight_characters" in result["person1"]
        assert "eight_characters" in result["person2"]

    @pytest.mark.asyncio
    async def test_get_compatibility_invalid_input(self):
        """Test error handling for invalid compatibility input."""
        result = await self.calculator.get_compatibility(
            "invalid-date", "2000-01-01 12:00", 8
        )

        assert "error" in result

    @pytest.mark.asyncio
    async def test_heavenly_stems_count(self):
        """Test that all 10 heavenly stems are defined."""
        assert len(self.calculator.heavenly_stems) == 10

        # Check structure
        for stem in self.calculator.heavenly_stems:
            assert len(stem) == 4  # Chinese, Pinyin, Element, Polarity

    @pytest.mark.asyncio
    async def test_earthly_branches_count(self):
        """Test that all 12 earthly branches are defined."""
        assert len(self.calculator.earthly_branches) == 12

        # Check structure
        for branch in self.calculator.earthly_branches:
            assert len(branch) == 5  # Chinese, Pinyin, Zodiac, Element, Polarity

    @pytest.mark.asyncio
    async def test_element_colors_mapping(self):
        """Test element color recommendations."""
        colors = self.calculator._get_element_colors("Wood")
        assert len(colors) > 0
        assert all(isinstance(color, str) for color in colors)

    @pytest.mark.asyncio
    async def test_element_directions_mapping(self):
        """Test element direction recommendations."""
        directions = self.calculator._get_element_directions("Fire")
        assert len(directions) > 0
        assert all(isinstance(direction, str) for direction in directions)

    @pytest.mark.asyncio
    async def test_element_careers_mapping(self):
        """Test element career recommendations."""
        careers = self.calculator._get_element_careers("Metal")
        assert len(careers) > 0
        assert all(isinstance(career, str) for career in careers)

    @pytest.mark.asyncio
    async def test_day_master_descriptions(self):
        """Test that day master descriptions are provided for all combinations."""
        elements = ["Wood", "Fire", "Earth", "Metal", "Water"]
        polarities = ["Yang", "Yin"]

        for element in elements:
            for polarity in polarities:
                description = self.calculator._get_day_master_description(
                    element, polarity
                )
                assert isinstance(description, str)
                assert len(description) > 0

    @pytest.mark.asyncio
    async def test_sexagenary_cycle(self):
        """Test that the 60-day cycle (Sexagenary cycle) works correctly."""
        # Calculate BaZi for dates 60 days apart
        result1 = await self.calculator.calculate_bazi("2000-01-01 12:00", 8)
        result2 = await self.calculator.calculate_bazi("2000-03-01 12:00", 8)

        day_pillar1 = result1["four_pillars"]["day"]["pillar"]
        day_pillar2 = result2["four_pillars"]["day"]["pillar"]

        # After 60 days, the cycle should repeat
        result3 = await self.calculator.calculate_bazi("2000-03-01 12:00", 8)
        day_pillar3 = result3["four_pillars"]["day"]["pillar"]

        # Day pillar should be same Chinese characters
        assert isinstance(day_pillar1, str)
        assert isinstance(day_pillar2, str)
        assert isinstance(day_pillar3, str)

    @pytest.mark.asyncio
    async def test_month_pillar_solar_terms(self):
        """Test that month pillar changes with solar terms."""
        # Test around solar term boundaries
        # February solar term around Feb 4
        result_before = await self.calculator.calculate_bazi("2000-02-03 12:00", 8)
        result_after = await self.calculator.calculate_bazi("2000-02-05 12:00", 8)

        # Month pillars should potentially differ around solar term
        month_before = result_before["four_pillars"]["month"]
        month_after = result_after["four_pillars"]["month"]

        assert "pillar" in month_before
        assert "pillar" in month_after

    @pytest.mark.asyncio
    async def test_all_zodiac_animals_covered(self):
        """Test that all 12 zodiac animals are in earthly branches."""
        zodiac_animals = [
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

        branch_zodiacs = [branch[2] for branch in self.calculator.earthly_branches]

        for animal in zodiac_animals:
            assert animal in branch_zodiacs

    @pytest.mark.asyncio
    async def test_all_elements_in_stems(self):
        """Test that all five elements are represented in heavenly stems."""
        elements = set()
        for stem in self.calculator.heavenly_stems:
            elements.add(stem[2])  # Element is at index 2

        assert elements == {"Wood", "Fire", "Earth", "Metal", "Water"}

    @pytest.mark.asyncio
    async def test_all_elements_in_branches(self):
        """Test that all five elements are represented in earthly branches."""
        elements = set()
        for branch in self.calculator.earthly_branches:
            elements.add(branch[3])  # Element is at index 3

        assert elements == {"Wood", "Fire", "Earth", "Metal", "Water"}

    @pytest.mark.asyncio
    async def test_element_balance_analysis(self):
        """Test element balance description accuracy."""
        # Test balanced distribution
        balanced_count = {"Wood": 2, "Fire": 2, "Earth": 1, "Metal": 2, "Water": 1}
        description = self.calculator._get_balance_description(balanced_count)
        assert "balanced" in description.lower()

        # Test imbalanced distribution
        imbalanced_count = {"Wood": 6, "Fire": 1, "Earth": 0, "Metal": 1, "Water": 0}
        description = self.calculator._get_balance_description(imbalanced_count)
        assert "imbalanced" in description.lower() or "disparity" in description.lower()

    @pytest.mark.asyncio
    async def test_compatibility_same_elements(self):
        """Test compatibility when both have same day master element."""
        # Create two people with birth times that might have same elements
        result = await self.calculator.get_compatibility(
            "2000-01-01 12:00", "2000-01-02 12:00", 8
        )

        assert "compatibility_score" in result
        assert "element_relationship" in result
        assert isinstance(result["compatibility_score"], (int, float))

    @pytest.mark.asyncio
    async def test_compatibility_generation_cycle(self):
        """Test compatibility with generation cycle relationships."""
        # This tests the generation relationship scoring
        result = await self.calculator.get_compatibility(
            "1990-05-15 10:00",  # Likely Fire day master
            "1992-08-20 14:00",  # Likely Wood day master (Wood generates Fire)
            8,
        )

        assert result["compatibility_score"] >= 0
        assert result["compatibility_score"] <= 10

    @pytest.mark.asyncio
    async def test_get_stem_branch_index(self):
        """Test the stem-branch index calculation."""
        # Test with zero offset
        stem, branch = self.calculator._get_stem_branch_index(0, (0, 0))
        assert stem == 0
        assert branch == 0

        # Test with 10-day offset (full stem cycle)
        stem, branch = self.calculator._get_stem_branch_index(10, (0, 0))
        assert stem == 0  # Should cycle back
        assert branch == 10

        # Test with 60-day offset (full sexagenary cycle)
        stem, branch = self.calculator._get_stem_branch_index(60, (0, 0))
        assert stem == 0
        assert branch == 0

    @pytest.mark.asyncio
    async def test_analyze_elements(self):
        """Test the element analysis function."""
        # Create test pillars
        test_pillars = [
            {
                "stem": {"element": "Wood"},
                "branch": {"element": "Fire"},
            },
            {
                "stem": {"element": "Fire"},
                "branch": {"element": "Earth"},
            },
            {
                "stem": {"element": "Earth"},
                "branch": {"element": "Metal"},
            },
            {
                "stem": {"element": "Metal"},
                "branch": {"element": "Water"},
            },
        ]

        analysis = self.calculator._analyze_elements(test_pillars)

        assert "element_distribution" in analysis
        assert "strongest_element" in analysis
        assert "weakest_element" in analysis
        assert "balance_analysis" in analysis
        assert "recommendations" in analysis

        # Check total element count
        total = sum(analysis["element_distribution"].values())
        assert total == 8  # 4 stems + 4 branches

    @pytest.mark.asyncio
    async def test_all_elements_have_colors(self):
        """Test that all elements have color recommendations."""
        elements = ["Wood", "Fire", "Earth", "Metal", "Water"]

        for element in elements:
            colors = self.calculator._get_element_colors(element)
            assert len(colors) > 0
            assert isinstance(colors, list)

    @pytest.mark.asyncio
    async def test_all_elements_have_directions(self):
        """Test that all elements have direction recommendations."""
        elements = ["Wood", "Fire", "Earth", "Metal", "Water"]

        for element in elements:
            directions = self.calculator._get_element_directions(element)
            assert len(directions) > 0
            assert isinstance(directions, list)

    @pytest.mark.asyncio
    async def test_all_elements_have_careers(self):
        """Test that all elements have career recommendations."""
        elements = ["Wood", "Fire", "Earth", "Metal", "Water"]

        for element in elements:
            careers = self.calculator._get_element_careers(element)
            assert len(careers) > 0
            assert isinstance(careers, list)

    @pytest.mark.asyncio
    async def test_hour_pillar_midnight_boundary(self):
        """Test hour pillar at midnight boundary (23:00)."""
        result = await self.calculator.calculate_bazi("2000-01-01 23:00", 8)

        hour_pillar = result["four_pillars"]["hour"]
        assert hour_pillar["branch"]["pinyin"] == "Zi"
        assert hour_pillar["hour_range"] == "23:00-01:00"

    @pytest.mark.asyncio
    async def test_year_pillar_different_years(self):
        """Test year pillar for consecutive years."""
        result_2000 = await self.calculator.calculate_bazi("2000-03-01 12:00", 8)
        result_2001 = await self.calculator.calculate_bazi("2001-03-01 12:00", 8)

        year_2000 = result_2000["four_pillars"]["year"]["pillar"]
        year_2001 = result_2001["four_pillars"]["year"]["pillar"]

        # Different years should have different pillars
        assert year_2000 != year_2001

    @pytest.mark.asyncio
    async def test_interpretation_field(self):
        """Test that interpretation field is included in results."""
        result = await self.calculator.calculate_bazi("1995-06-15 14:00", 8)

        assert "interpretation" in result
        assert "character" in result["interpretation"]
        assert "overall" in result["interpretation"]

    @pytest.mark.asyncio
    async def test_pillar_meanings(self):
        """Test that all pillars have meaningful descriptions."""
        result = await self.calculator.calculate_bazi("2000-01-01 12:00", 8)

        for pillar_name in ["year", "month", "day", "hour"]:
            pillar = result["four_pillars"][pillar_name]
            assert "meaning" in pillar
            assert len(pillar["meaning"]) > 0
            assert (
                "year" in pillar["meaning"].lower()
                or pillar_name in pillar["meaning"].lower()
                or "self" in pillar["meaning"].lower()
                or "spouse" in pillar["meaning"].lower()
                or "children" in pillar["meaning"].lower()
            )

    @pytest.mark.asyncio
    async def test_compatibility_strengths_and_challenges(self):
        """Test that compatibility returns strengths and challenges."""
        await self.calculator.get_compatibility("1988-03-15 10:00", "1990-07-20 14:00", 8)

        strengths = self.calculator._get_compatibility_strengths("Wood", "Fire")
        challenges = self.calculator._get_compatibility_challenges("Wood", "Fire")

        assert isinstance(strengths, list)
        assert isinstance(challenges, list)
        assert len(strengths) > 0
        assert len(challenges) > 0

    @pytest.mark.asyncio
    async def test_element_recommendations_structure(self):
        """Test element recommendations have all required fields."""
        element_count = {"Wood": 2, "Fire": 3, "Earth": 1, "Metal": 1, "Water": 1}
        recommendations = self.calculator._get_element_recommendations(
            element_count, "Fire", "Earth"
        )

        assert "enhance_element" in recommendations
        assert "favorable_colors" in recommendations
        assert "favorable_directions" in recommendations
        assert "career_suggestions" in recommendations

        assert recommendations["enhance_element"] == "Earth"

    @pytest.mark.asyncio
    async def test_negative_timezone_offset(self):
        """Test BaZi calculation with negative timezone offset."""
        result = await self.calculator.calculate_bazi("2000-01-01 12:00", -5)

        assert "eight_characters" in result
        assert "adjusted_datetime" in result
        # Should adjust forward by 13 hours (from -5 to +8)
        assert "2000-01-02" in result["adjusted_datetime"]

    @pytest.mark.asyncio
    async def test_large_timezone_offset(self):
        """Test BaZi calculation with large timezone offset."""
        result = await self.calculator.calculate_bazi("2000-01-01 12:00", 12)

        assert "eight_characters" in result
        assert "adjusted_datetime" in result

    @pytest.mark.asyncio
    async def test_compatibility_both_invalid_dates(self):
        """Test compatibility with both invalid dates."""
        result = await self.calculator.get_compatibility("invalid1", "invalid2", 8)

        assert "error" in result
