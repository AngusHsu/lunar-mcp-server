#!/usr/bin/env python3
"""
Usage examples for the Lunar Calendar MCP Server.

This script demonstrates various features of the lunar calendar server
including auspicious date checking, festival information, moon phases,
and calendar conversions.
"""

import asyncio
import json
from datetime import datetime, timedelta

from lunar_mcp_server import LunarMCPServer


class LunarCalendarDemo:
    """Demonstration class for lunar calendar features."""

    def __init__(self):
        self.server = LunarMCPServer()

    async def demo_auspicious_dates(self):
        """Demo: Check auspicious dates for various activities."""
        print("=" * 60)
        print("🌙 AUSPICIOUS DATE ANALYSIS")
        print("=" * 60)

        # Check specific date for wedding
        print("\n1. Checking Wedding Date Auspiciousness")
        print("-" * 40)
        result = await self.server._check_auspicious_date(
            date="2024-03-15",
            activity="wedding",
            culture="chinese"
        )

        print(f"Date: {result['date']}")
        print(f"Auspiciousness: {result['auspicious_level']}")
        print(f"Score: {result.get('score', 'N/A')}/10")
        print(f"Zodiac Day: {result.get('zodiac_day', 'N/A')}")
        print(f"Good for: {', '.join(result.get('good_for', []))}")
        print(f"Avoid: {', '.join(result.get('avoid', []))}")
        print(f"Lucky Hours: {', '.join(result.get('lucky_hours', []))}")
        print(f"Recommendation: {result.get('recommendations', 'N/A')}")

        # Find good dates for business opening
        print("\n2. Finding Good Dates for Business Opening")
        print("-" * 45)
        result = await self.server._find_good_dates(
            start_date="2024-04-01",
            end_date="2024-04-30",
            activity="business_opening",
            culture="chinese",
            limit=5
        )

        print(f"Searching period: {result['search_period']}")
        print(f"Found {result['found_dates']} good dates:")

        for i, date_info in enumerate(result.get('good_dates', []), 1):
            print(f"  {i}. {date_info['date']} - {date_info['level']} (Score: {date_info['score']})")
            print(f"     Zodiac: {date_info.get('zodiac_day', 'N/A')}, Moon: {date_info.get('moon_phase', 'N/A')}")

        if result.get('best_date'):
            best = result['best_date']
            print(f"\nBest date: {best['date']} ({best['level']})")

    async def demo_daily_fortune(self):
        """Demo: Get daily fortune information."""
        print("\n3. Daily Fortune Analysis")
        print("-" * 30)

        result = await self.server._get_daily_fortune(
            date="2024-02-14",
            culture="chinese"
        )

        print(f"Date: {result['date']}")
        print(f"Fortune Level: {result.get('fortune_level', 'N/A')}")
        print(f"Fortune Score: {result.get('fortune_score', 'N/A')}/10")
        print(f"Zodiac Day: {result.get('zodiac_day', 'N/A')}")
        print(f"Five Element: {result.get('five_element', 'N/A')}")
        print(f"Lucky Colors: {', '.join(result.get('lucky_colors', []))}")
        print(f"Lucky Numbers: {', '.join(map(str, result.get('lucky_numbers', [])))}")
        print(f"Lucky Directions: {', '.join(result.get('lucky_directions', []))}")
        print(f"Description: {result.get('description', 'N/A')}")
        print(f"Advice: {result.get('advice', 'N/A')}")

    async def demo_zodiac_compatibility(self):
        """Demo: Check zodiac compatibility between dates."""
        print("\n4. Zodiac Compatibility Check")
        print("-" * 35)

        result = await self.server._check_zodiac_compatibility(
            date1="2024-01-15",
            date2="2024-02-15",
            culture="chinese"
        )

        print(f"Date 1: {result['date1']} (Zodiac: {result.get('zodiac1', 'N/A')})")
        print(f"Date 2: {result['date2']} (Zodiac: {result.get('zodiac2', 'N/A')})")
        print(f"Compatibility: {result.get('compatibility_level', 'N/A')}")
        print(f"Description: {result.get('description', 'N/A')}")
        print(f"Recommendations: {result.get('recommendations', 'N/A')}")

        element_rel = result.get('element_relationship', {})
        if element_rel:
            print(f"Element Relationship: {element_rel.get('description', 'N/A')}")

    async def demo_festivals(self):
        """Demo: Festival information and discovery."""
        print("\n\n" + "=" * 60)
        print("🎉 FESTIVAL INFORMATION")
        print("=" * 60)

        # Check festivals on Chinese New Year
        print("\n1. Festivals on Chinese New Year 2024")
        print("-" * 40)
        result = await self.server._get_lunar_festivals(
            date="2024-02-10",
            culture="chinese"
        )

        print(f"Date: {result['date']}")
        print(f"Festival Count: {result.get('festival_count', 0)}")
        print(f"Major Festival: {'Yes' if result.get('is_major_festival') else 'No'}")

        for festival in result.get('festivals', []):
            print(f"\nFestival: {festival['name']}")
            print(f"Significance: {festival.get('significance', 'N/A')}")
            print(f"Traditions: {', '.join(festival.get('traditions', []))}")
            print(f"Foods: {', '.join(festival.get('foods', []))}")
            if festival.get('lucky_activities'):
                print(f"Lucky Activities: {', '.join(festival['lucky_activities'])}")

        # Find next festival
        print("\n2. Finding Next Festival")
        print("-" * 30)
        result = await self.server._get_next_festival(
            date="2024-03-01",
            culture="chinese"
        )

        if result.get('next_festival_date'):
            print(f"Next festival date: {result['next_festival_date']}")
            print(f"Days until: {result.get('days_until', 'N/A')}")
            festival = result.get('festival', {})
            print(f"Festival: {festival.get('name', 'N/A')}")
            print(f"Significance: {festival.get('significance', 'N/A')}")
            print(f"Preparation: {result.get('preparation_time', 'N/A')}")

        # Get annual festivals
        print("\n3. Annual Festivals for 2024")
        print("-" * 35)
        result = await self.server._get_annual_festivals(
            year=2024,
            culture="chinese"
        )

        print(f"Year: {result['year']}")
        print(f"Total Festivals: {result.get('total_festivals', 0)}")
        print(f"Major Festivals: {len(result.get('major_festivals', []))}")

        print("\nMajor festivals:")
        for festival in result.get('major_festivals', [])[:5]:  # Show first 5
            est_date = festival.get('estimated_date', {})
            date_str = f"{est_date.get('year', 'N/A')}-{est_date.get('month', 1):02d}-{est_date.get('day', 1):02d}"
            print(f"  • {festival['name']} - {date_str}")

    async def demo_moon_phases(self):
        """Demo: Moon phase analysis and influence."""
        print("\n\n" + "=" * 60)
        print("🌕 MOON PHASE ANALYSIS")
        print("=" * 60)

        # Get moon phase for specific date
        print("\n1. Moon Phase Information")
        print("-" * 30)
        result = await self.server._get_moon_phase(
            date="2024-02-14",
            location="40.7128,-74.0060"  # New York
        )

        print(f"Date: {result['date']}")
        print(f"Phase: {result.get('phase_name', 'N/A')}")
        print(f"Illumination: {result.get('illumination', 0):.1%}")
        print(f"Lunar Day: {result.get('lunar_day', 'N/A')}")
        print(f"Zodiac Sign: {result.get('zodiac_sign', 'N/A')}")
        print(f"Rise Time: {result.get('rise_time', 'N/A')}")
        print(f"Set Time: {result.get('set_time', 'N/A')}")

        influence = result.get('influence', {})
        if influence:
            print(f"Energy Type: {influence.get('energy_type', 'N/A')}")
            print(f"Good for: {', '.join(influence.get('good_for', []))}")
            print(f"Avoid: {', '.join(influence.get('avoid', []))}")

        # Get moon influence on specific activity
        print("\n2. Moon Influence on Activities")
        print("-" * 35)
        activities = ["wedding", "business_opening", "travel", "surgery"]

        for activity in activities:
            result = await self.server._get_moon_influence(
                date="2024-02-14",
                activity=activity
            )

            print(f"\n{activity.replace('_', ' ').title()}:")
            print(f"  Rating: {result.get('activity_rating', 'N/A')}")
            print(f"  Recommendation: {result.get('recommendation', 'N/A')}")

        # Predict moon phases
        print("\n3. Moon Phase Predictions")
        print("-" * 30)
        result = await self.server._predict_moon_phases(
            start_date="2024-02-01",
            end_date="2024-02-29"
        )

        print(f"Period: {result['start_date']} to {result['end_date']}")
        print(f"Major phases found: {result.get('total_phases', 0)}")

        for phase in result.get('major_phases', []):
            print(f"  • {phase['date']}: {phase['phase']} (Day {phase.get('lunar_day', 'N/A')})")

    async def demo_calendar_conversions(self):
        """Demo: Calendar conversions and zodiac information."""
        print("\n\n" + "=" * 60)
        print("📅 CALENDAR CONVERSIONS")
        print("=" * 60)

        # Solar to lunar conversion
        print("\n1. Solar to Lunar Date Conversion")
        print("-" * 40)
        result = await self.server._solar_to_lunar(
            solar_date="2024-02-14",
            culture="chinese"
        )

        print(f"Solar Date: {result.get('solar_date', 'N/A')}")
        print(f"Lunar Year: {result.get('lunar_year', 'N/A')}")
        print(f"Lunar Month: {result.get('lunar_month', 'N/A')}")
        print(f"Lunar Day: {result.get('lunar_day', 'N/A')}")

        zodiac_info = result.get('zodiac_info', {})
        if zodiac_info:
            print(f"Zodiac Animal: {zodiac_info.get('animal', 'N/A')}")
            print(f"Element: {zodiac_info.get('element', 'N/A')}")
            print(f"Yin/Yang: {zodiac_info.get('yin_yang', 'N/A')}")

        # Get detailed zodiac information
        print("\n2. Detailed Zodiac Information")
        print("-" * 35)
        result = await self.server._get_zodiac_info(
            date="2024-02-14",
            culture="chinese"
        )

        print(f"Date: {result['date']}")
        print(f"Culture: {result['culture']}")

        year_zodiac = result.get('year_zodiac', {})
        if year_zodiac:
            print(f"\nYear Zodiac:")
            print(f"  Animal: {year_zodiac.get('animal', 'N/A')}")
            print(f"  Element: {year_zodiac.get('element', 'N/A')}")
            print(f"  Full Name: {year_zodiac.get('full_name', 'N/A')}")

        daily_zodiac = result.get('daily_zodiac', {})
        if daily_zodiac:
            print(f"\nDaily Zodiac:")
            print(f"  Animal: {daily_zodiac.get('animal', 'N/A')}")
            print(f"  Influence: {daily_zodiac.get('influence', 'N/A')}")

        hourly_zodiac = result.get('hourly_zodiac', {})
        if hourly_zodiac:
            print(f"\nHourly Zodiac:")
            print(f"  Animal: {hourly_zodiac.get('animal', 'N/A')}")
            print(f"  Hours: {hourly_zodiac.get('hour_range', 'N/A')}")

        compatibility = result.get('compatibility', {})
        if compatibility:
            print(f"\nCompatibility:")
            print(f"  Best matches: {', '.join(compatibility.get('best_matches', []))}")
            print(f"  Challenging: {', '.join(compatibility.get('challenging_matches', []))}")

        # Western zodiac for comparison
        print("\n3. Western Zodiac Information")
        print("-" * 35)
        result = await self.server._get_zodiac_info(
            date="2024-02-14",
            culture="western"
        )

        print(f"Zodiac Sign: {result.get('zodiac_sign', 'N/A')}")
        print(f"Element: {result.get('element', 'N/A')}")
        print(f"Quality: {result.get('quality', 'N/A')}")
        print(f"Ruling Planet: {result.get('ruling_planet', 'N/A')}")

        traits = result.get('traits', {})
        if traits:
            print(f"Positive Traits: {', '.join(traits.get('positive', [])[:3])}")
            print(f"Challenges: {', '.join(traits.get('negative', [])[:3])}")

        compatible_signs = result.get('compatible_signs', {})
        if isinstance(compatible_signs, dict):
            compat_list = compatible_signs.get('compatible', [])
            challenging_list = compatible_signs.get('challenging', [])
            if compat_list:
                print(f"Compatible Signs: {', '.join(compat_list[:4])}")
            if challenging_list:
                print(f"Challenging Matches: {', '.join(challenging_list[:4])}")
        elif compatible_signs:
            print(f"Compatible Signs: {', '.join(compatible_signs[:4])}")

    async def demo_islamic_features(self):
        """Demo: Islamic calendar features."""
        print("\n\n" + "=" * 60)
        print("☪️ ISLAMIC CALENDAR FEATURES")
        print("=" * 60)

        # Convert to Islamic calendar
        print("\n1. Islamic Calendar Conversion")
        print("-" * 35)
        result = await self.server._solar_to_lunar(
            solar_date="2024-02-14",
            culture="islamic"
        )

        print(f"Solar Date: {result.get('solar_date', 'N/A')}")
        print(f"Hijri Year: {result.get('hijri_year', 'N/A')}")
        print(f"Hijri Month: {result.get('hijri_month', 'N/A')}")
        print(f"Hijri Day: {result.get('hijri_day', 'N/A')}")
        print(f"Month Name: {result.get('month_name', 'N/A')}")

        # Get Islamic festivals
        print("\n2. Islamic Festivals and Observances")
        print("-" * 40)
        result = await self.server._get_annual_festivals(
            year=2024,
            culture="islamic"
        )

        print(f"Islamic festivals in {result['year']}:")
        for festival in result.get('festivals', [])[:5]:
            print(f"  • {festival['name']}")
            if festival.get('estimated_date'):
                est_date = festival['estimated_date']
                print(f"    Estimated: {est_date.get('year')}-{est_date.get('month', 1):02d}-{est_date.get('day', 1):02d}")

    async def run_all_demos(self):
        """Run all demonstration functions."""
        print("🌙 LUNAR CALENDAR MCP SERVER DEMONSTRATION 🌙")
        print("=" * 60)
        print("This demo showcases the comprehensive features of the")
        print("Lunar Calendar MCP Server across multiple cultures.")
        print()

        try:
            await self.demo_auspicious_dates()
            await self.demo_daily_fortune()
            await self.demo_zodiac_compatibility()
            await self.demo_festivals()
            await self.demo_moon_phases()
            await self.demo_calendar_conversions()
            await self.demo_islamic_features()

            print("\n\n" + "=" * 60)
            print("✨ DEMONSTRATION COMPLETE")
            print("=" * 60)
            print("All features demonstrated successfully!")
            print("The Lunar Calendar MCP Server provides comprehensive")
            print("traditional calendar wisdom across multiple cultures.")
            print("\nFor more information, see the README.md file.")

        except Exception as e:
            print(f"\n❌ Error during demonstration: {e}")
            print("This might be due to missing optional dependencies.")
            print("The server will work with available libraries.")


async def main():
    """Main demonstration function."""
    demo = LunarCalendarDemo()
    await demo.run_all_demos()


if __name__ == "__main__":
    asyncio.run(main())
