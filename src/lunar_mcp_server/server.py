"""
Main MCP server implementation for Lunar Calendar services.
"""

import asyncio
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.lowlevel import NotificationOptions
from mcp.types import TextContent, Tool

from .auspicious_dates import AuspiciousDateChecker
from .calendar_conversions import CalendarConverter
from .festivals import FestivalManager
from .lunar_calculations import LunarCalculator


class LunarMCPServer:
    """MCP Server for Lunar Calendar operations."""

    def __init__(self) -> None:
        self.server = Server("lunar-mcp-server", version="0.1.0")
        self.lunar_calc = LunarCalculator()
        self.auspicious_checker = AuspiciousDateChecker()
        self.festival_manager = FestivalManager()
        self.calendar_converter = CalendarConverter()
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up MCP server handlers."""

        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="check_auspicious_date",
                    description="Check if a date is favorable for specific activities",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Date in YYYY-MM-DD format",
                            },
                            "activity": {
                                "type": "string",
                                "description": "Activity type (e.g., wedding, business_opening, travel)",
                            },
                            "culture": {
                                "type": "string",
                                "description": "Cultural tradition (chinese)",
                                "default": "chinese",
                            },
                        },
                        "required": ["date", "activity"],
                    },
                ),
                Tool(
                    name="find_good_dates",
                    description="Find optimal dates in a range for specific activities",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start_date": {
                                "type": "string",
                                "description": "Start date in YYYY-MM-DD format",
                            },
                            "end_date": {
                                "type": "string",
                                "description": "End date in YYYY-MM-DD format",
                            },
                            "activity": {
                                "type": "string",
                                "description": "Activity type",
                            },
                            "culture": {
                                "type": "string",
                                "description": "Cultural tradition",
                                "default": "chinese",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of dates to return",
                                "default": 10,
                            },
                        },
                        "required": ["start_date", "end_date", "activity"],
                    },
                ),
                Tool(
                    name="get_daily_fortune",
                    description="Get daily fortune and luck information",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Date in YYYY-MM-DD format",
                            },
                            "culture": {
                                "type": "string",
                                "description": "Cultural tradition",
                                "default": "chinese",
                            },
                        },
                        "required": ["date"],
                    },
                ),
                Tool(
                    name="check_zodiac_compatibility",
                    description="Check compatibility between dates based on zodiac",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "date1": {
                                "type": "string",
                                "description": "First date in YYYY-MM-DD format",
                            },
                            "date2": {
                                "type": "string",
                                "description": "Second date in YYYY-MM-DD format",
                            },
                            "culture": {
                                "type": "string",
                                "description": "Cultural tradition",
                                "default": "chinese",
                            },
                        },
                        "required": ["date1", "date2"],
                    },
                ),
                Tool(
                    name="get_lunar_festivals",
                    description="Get festivals for a specific date",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Date in YYYY-MM-DD format",
                            },
                            "culture": {
                                "type": "string",
                                "description": "Cultural tradition",
                                "default": "chinese",
                            },
                        },
                        "required": ["date"],
                    },
                ),
                Tool(
                    name="get_next_festival",
                    description="Find next upcoming festival",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Reference date in YYYY-MM-DD format",
                            },
                            "culture": {
                                "type": "string",
                                "description": "Cultural tradition",
                                "default": "chinese",
                            },
                        },
                        "required": ["date"],
                    },
                ),
                Tool(
                    name="get_festival_details",
                    description="Get detailed festival information",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "festival_name": {
                                "type": "string",
                                "description": "Name of the festival",
                            },
                            "culture": {
                                "type": "string",
                                "description": "Cultural tradition",
                                "default": "chinese",
                            },
                        },
                        "required": ["festival_name"],
                    },
                ),
                Tool(
                    name="get_annual_festivals",
                    description="Get all festivals for a year",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "year": {"type": "integer", "description": "Year"},
                            "culture": {
                                "type": "string",
                                "description": "Cultural tradition",
                                "default": "chinese",
                            },
                        },
                        "required": ["year"],
                    },
                ),
                Tool(
                    name="get_moon_phase",
                    description="Get current moon phase with details",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Date in YYYY-MM-DD format",
                            },
                            "location": {
                                "type": "string",
                                "description": "Location for calculations (lat,lon or city name)",
                                "default": "0,0",
                            },
                        },
                        "required": ["date"],
                    },
                ),
                Tool(
                    name="get_moon_calendar",
                    description="Get monthly calendar with moon phases",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "month": {"type": "integer", "description": "Month (1-12)"},
                            "year": {"type": "integer", "description": "Year"},
                            "location": {
                                "type": "string",
                                "description": "Location for calculations",
                                "default": "0,0",
                            },
                        },
                        "required": ["month", "year"],
                    },
                ),
                Tool(
                    name="get_moon_influence",
                    description="Get how moon affects specific activities",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Date in YYYY-MM-DD format",
                            },
                            "activity": {
                                "type": "string",
                                "description": "Activity type",
                            },
                        },
                        "required": ["date", "activity"],
                    },
                ),
                Tool(
                    name="predict_moon_phases",
                    description="Predict future moon phases in date range",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start_date": {
                                "type": "string",
                                "description": "Start date in YYYY-MM-DD format",
                            },
                            "end_date": {
                                "type": "string",
                                "description": "End date in YYYY-MM-DD format",
                            },
                        },
                        "required": ["start_date", "end_date"],
                    },
                ),
                Tool(
                    name="solar_to_lunar",
                    description="Convert solar date to lunar date",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "solar_date": {
                                "type": "string",
                                "description": "Solar date in YYYY-MM-DD format",
                            },
                            "culture": {
                                "type": "string",
                                "description": "Cultural tradition",
                                "default": "chinese",
                            },
                        },
                        "required": ["solar_date"],
                    },
                ),
                Tool(
                    name="lunar_to_solar",
                    description="Convert lunar date to solar date",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "lunar_date": {
                                "type": "string",
                                "description": "Lunar date in YYYY-MM-DD format",
                            },
                            "culture": {
                                "type": "string",
                                "description": "Cultural tradition",
                                "default": "chinese",
                            },
                        },
                        "required": ["lunar_date"],
                    },
                ),
                Tool(
                    name="get_zodiac_info",
                    description="Get zodiac animal/sign information for date",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Date in YYYY-MM-DD format",
                            },
                            "culture": {
                                "type": "string",
                                "description": "Cultural tradition",
                                "default": "chinese",
                            },
                        },
                        "required": ["date"],
                    },
                ),
                Tool(
                    name="batch_check_dates",
                    description="Check multiple dates at once for efficiency",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "dates": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Array of dates in YYYY-MM-DD format",
                            },
                            "activity": {
                                "type": "string",
                                "description": "Activity type",
                            },
                            "culture": {
                                "type": "string",
                                "description": "Cultural tradition",
                                "default": "chinese",
                            },
                        },
                        "required": ["dates", "activity"],
                    },
                ),
                Tool(
                    name="compare_dates",
                    description="Compare multiple dates side-by-side",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "dates": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Array of dates to compare",
                            },
                            "activity": {
                                "type": "string",
                                "description": "Activity type for comparison",
                            },
                            "culture": {
                                "type": "string",
                                "description": "Cultural tradition",
                                "default": "chinese",
                            },
                        },
                        "required": ["dates"],
                    },
                ),
                Tool(
                    name="get_lucky_hours",
                    description="Get auspicious hours within a specific day",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Date in YYYY-MM-DD format",
                            },
                            "activity": {
                                "type": "string",
                                "description": "Activity type",
                            },
                            "culture": {
                                "type": "string",
                                "description": "Cultural tradition",
                                "default": "chinese",
                            },
                        },
                        "required": ["date"],
                    },
                ),
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict[str, Any]
        ) -> list[TextContent]:
            """Handle tool calls."""
            try:
                if name == "check_auspicious_date":
                    result = await self._check_auspicious_date(**arguments)
                elif name == "find_good_dates":
                    result = await self._find_good_dates(**arguments)
                elif name == "get_daily_fortune":
                    result = await self._get_daily_fortune(**arguments)
                elif name == "check_zodiac_compatibility":
                    result = await self._check_zodiac_compatibility(**arguments)
                elif name == "get_lunar_festivals":
                    result = await self._get_lunar_festivals(**arguments)
                elif name == "get_next_festival":
                    result = await self._get_next_festival(**arguments)
                elif name == "get_festival_details":
                    result = await self._get_festival_details(**arguments)
                elif name == "get_annual_festivals":
                    result = await self._get_annual_festivals(**arguments)
                elif name == "get_moon_phase":
                    result = await self._get_moon_phase(**arguments)
                elif name == "get_moon_calendar":
                    result = await self._get_moon_calendar(**arguments)
                elif name == "get_moon_influence":
                    result = await self._get_moon_influence(**arguments)
                elif name == "predict_moon_phases":
                    result = await self._predict_moon_phases(**arguments)
                elif name == "solar_to_lunar":
                    result = await self._solar_to_lunar(**arguments)
                elif name == "lunar_to_solar":
                    result = await self._lunar_to_solar(**arguments)
                elif name == "get_zodiac_info":
                    result = await self._get_zodiac_info(**arguments)
                elif name == "batch_check_dates":
                    result = await self._batch_check_dates(**arguments)
                elif name == "compare_dates":
                    result = await self._compare_dates(**arguments)
                elif name == "get_lucky_hours":
                    result = await self._get_lucky_hours(**arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")

                return [TextContent(type="text", text=json.dumps(result, indent=2))]

            except Exception as e:
                error_result = {"error": str(e), "tool": name}
                return [
                    TextContent(type="text", text=json.dumps(error_result, indent=2))
                ]

    async def _check_auspicious_date(
        self, date: str, activity: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Check if a date is auspicious for an activity."""
        return await self.auspicious_checker.check_date(date, activity, culture)

    async def _find_good_dates(
        self,
        start_date: str,
        end_date: str,
        activity: str,
        culture: str = "chinese",
        limit: int = 10,
    ) -> dict[str, Any]:
        """Find good dates in a range."""
        return await self.auspicious_checker.find_good_dates(
            start_date, end_date, activity, culture, limit
        )

    async def _get_daily_fortune(
        self, date: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Get daily fortune information."""
        return await self.auspicious_checker.get_daily_fortune(date, culture)

    async def _check_zodiac_compatibility(
        self, date1: str, date2: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Check zodiac compatibility between dates."""
        return await self.auspicious_checker.check_zodiac_compatibility(
            date1, date2, culture
        )

    async def _get_lunar_festivals(
        self, date: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Get festivals for a date."""
        return await self.festival_manager.get_festivals_for_date(date, culture)

    async def _get_next_festival(
        self, date: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Get next festival after date."""
        return await self.festival_manager.get_next_festival(date, culture)

    async def _get_festival_details(
        self, festival_name: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Get detailed festival information."""
        return await self.festival_manager.get_festival_details(festival_name, culture)

    async def _get_annual_festivals(
        self, year: int, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Get all festivals for a year."""
        return await self.festival_manager.get_annual_festivals(year, culture)

    async def _get_moon_phase(self, date: str, location: str = "0,0") -> dict[str, Any]:
        """Get moon phase for date and location."""
        return await self.lunar_calc.get_moon_phase(date, location)

    async def _get_moon_calendar(
        self, month: int, year: int, location: str = "0,0"
    ) -> dict[str, Any]:
        """Get monthly moon calendar."""
        return await self.lunar_calc.get_moon_calendar(month, year, location)

    async def _get_moon_influence(self, date: str, activity: str) -> dict[str, Any]:
        """Get moon influence on activity."""
        return await self.lunar_calc.get_moon_influence(date, activity)

    async def _predict_moon_phases(
        self, start_date: str, end_date: str
    ) -> dict[str, Any]:
        """Predict moon phases in date range."""
        return await self.lunar_calc.predict_moon_phases(start_date, end_date)

    async def _solar_to_lunar(
        self, solar_date: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Convert solar to lunar date."""
        return await self.calendar_converter.solar_to_lunar(solar_date, culture)

    async def _lunar_to_solar(
        self, lunar_date: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Convert lunar to solar date."""
        return await self.calendar_converter.lunar_to_solar(lunar_date, culture)

    async def _get_zodiac_info(
        self, date: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Get zodiac information for date."""
        return await self.calendar_converter.get_zodiac_info(date, culture)

    async def _batch_check_dates(
        self, dates: list[str], activity: str, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Check multiple dates at once for efficiency."""
        results = []
        for date in dates[:30]:  # Limit to 30 dates to prevent abuse
            try:
                check_result = await self.auspicious_checker.check_date(
                    date, activity, culture
                )
                results.append(
                    {
                        "date": date,
                        "score": check_result.get("score", 0),
                        "level": check_result.get("auspicious_level", "unknown"),
                        "details": check_result,
                    }
                )
            except Exception as e:
                results.append({"date": date, "error": str(e)})

        # Find best and worst dates
        valid_results = [r for r in results if "score" in r]
        best_date = (
            max(valid_results, key=lambda x: x["score"]) if valid_results else None
        )
        worst_date = (
            min(valid_results, key=lambda x: x["score"]) if valid_results else None
        )

        return {
            "total_checked": len(results),
            "results": results,
            "best_date": best_date["date"] if best_date else None,
            "worst_date": worst_date["date"] if worst_date else None,
            "activity": activity,
            "culture": culture,
        }

    async def _compare_dates(
        self, dates: list[str], activity: str | None = None, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Compare multiple dates side-by-side."""
        comparison = {}

        for date in dates[:10]:  # Limit to 10 dates for comparison
            try:
                # Get multiple aspects of the date
                aspects = {}

                if activity:
                    auspicious = await self.auspicious_checker.check_date(
                        date, activity, culture
                    )
                    aspects["auspicious_level"] = auspicious.get("auspicious_level")
                    aspects["score"] = auspicious.get("score")
                    aspects["good_for"] = auspicious.get("good_for", [])
                    aspects["avoid"] = auspicious.get("avoid", [])

                moon = await self.lunar_calc.get_moon_phase(date, "0,0")
                aspects["moon_phase"] = moon.get("phase_name")
                aspects["moon_illumination"] = moon.get("illumination")

                festivals = await self.festival_manager.get_festivals_for_date(
                    date, culture
                )
                aspects["festivals"] = [
                    f.get("name") for f in festivals.get("festivals", [])
                ]

                zodiac = await self.calendar_converter.get_zodiac_info(date, culture)
                aspects["zodiac"] = zodiac.get("zodiac", {})

                comparison[date] = aspects

            except Exception as e:
                comparison[date] = {"error": str(e)}

        # Add recommendation if activity provided
        recommendation = None
        if activity and comparison:
            scores: dict[str, int] = {}
            for d, data in comparison.items():
                if "score" in data:
                    score_val = data.get("score", 0)
                    scores[d] = int(score_val) if score_val is not None else 0
            if scores:
                recommendation = max(scores, key=lambda x: scores[x])

        return {
            "comparison": comparison,
            "recommendation": recommendation,
            "activity": activity,
            "culture": culture,
        }

    async def _get_lucky_hours(
        self, date: str, activity: str | None = None, culture: str = "chinese"
    ) -> dict[str, Any]:
        """Get auspicious hours within a specific day."""
        # Traditional Chinese lucky hours based on stems and branches
        # This is a simplified implementation
        lucky_hours = []

        # Get the daily fortune first to understand the day's energy
        daily_fortune = await self.auspicious_checker.get_daily_fortune(date, culture)

        # Define traditional time periods (12 two-hour periods in Chinese tradition)
        time_periods = [
            ("23:00-01:00", "Zi (子)", "Rat"),
            ("01:00-03:00", "Chou (丑)", "Ox"),
            ("03:00-05:00", "Yin (寅)", "Tiger"),
            ("05:00-07:00", "Mao (卯)", "Rabbit"),
            ("07:00-09:00", "Chen (辰)", "Dragon"),
            ("09:00-11:00", "Si (巳)", "Snake"),
            ("11:00-13:00", "Wu (午)", "Horse"),
            ("13:00-15:00", "Wei (未)", "Goat"),
            ("15:00-17:00", "Shen (申)", "Monkey"),
            ("17:00-19:00", "You (酉)", "Rooster"),
            ("19:00-21:00", "Xu (戌)", "Dog"),
            ("21:00-23:00", "Hai (亥)", "Pig"),
        ]

        # Simplified scoring: some hours are traditionally more auspicious
        # Dragon (07:00-09:00) and Horse (11:00-13:00) hours are generally favorable
        auspicious_indices = [4, 6, 9]  # Dragon, Horse, Rooster hours

        for idx, (time_range, period_name, zodiac_animal) in enumerate(time_periods):
            score = 5  # Base score

            if idx in auspicious_indices:
                score += 3

            if activity:
                # Adjust based on activity type
                if activity in ["business_opening", "signing_contract"] and idx in [
                    4,
                    6,
                ]:
                    score += 2
                elif activity in ["wedding", "celebration"] and idx in [6, 9]:
                    score += 2

            level = "very_good" if score >= 8 else "good" if score >= 6 else "fair"

            lucky_hours.append(
                {
                    "time_range": time_range,
                    "period": period_name,
                    "zodiac_animal": zodiac_animal,
                    "score": score,
                    "level": level,
                    "suitable_for": self._get_suitable_activities(
                        zodiac_animal, activity
                    ),
                }
            )

        # Sort by score
        lucky_hours.sort(
            key=lambda x: int(x["score"]) if isinstance(x["score"], (int, str)) else 0,
            reverse=True,
        )

        # Filter best hours (score >= 7)
        best_hours_list: list[dict[str, Any]] = []
        for h in lucky_hours:
            score_val = h.get("score")
            if isinstance(score_val, int) and score_val >= 7:
                best_hours_list.append(h)

        return {
            "date": date,
            "activity": activity,
            "culture": culture,
            "lucky_hours": lucky_hours,
            "best_hours": best_hours_list,
            "daily_overview": daily_fortune,
        }

    def _get_suitable_activities(
        self, zodiac_animal: str, requested_activity: str | None = None
    ) -> list[str]:
        """Get suitable activities for a zodiac hour."""
        activity_map = {
            "Dragon": ["business_opening", "signing_contract", "important_meetings"],
            "Horse": ["wedding", "celebration", "social_events"],
            "Rooster": ["communication", "negotiation", "presentations"],
            "Tiger": ["starting_new_projects", "bold_initiatives"],
            "Rabbit": ["artistic_work", "meditation", "planning"],
            "Rat": ["financial_planning", "investments"],
            "Ox": ["hard_work", "construction", "farming"],
            "Snake": ["strategy", "research", "wisdom_seeking"],
            "Goat": ["family_matters", "nurturing", "creativity"],
            "Monkey": ["problem_solving", "innovation", "learning"],
            "Dog": ["security_matters", "protection", "loyalty_building"],
            "Pig": ["rest", "enjoyment", "social_gatherings"],
        }

        return activity_map.get(zodiac_animal, ["general_activities"])

    async def run(self, transport_type: str = "stdio") -> None:
        """Run the MCP server."""
        if transport_type == "stdio":
            from mcp.server.stdio import stdio_server

            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options(
                        notification_options=NotificationOptions(tools_changed=True)
                    ),
                )


async def _run_server() -> None:
    """Start the MCP server event loop."""
    server = LunarMCPServer()
    await server.run()


def main() -> None:
    """Synchronous entry point for console scripts."""
    logging.basicConfig(level=logging.INFO)
    asyncio.run(_run_server())


if __name__ == "__main__":
    main()
