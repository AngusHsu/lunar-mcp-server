"""
Main MCP server implementation for Lunar Calendar services.
"""

import asyncio
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.lowlevel import NotificationOptions
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    Resource,
    TextContent,
    Tool,
)

from .auspicious_dates import AuspiciousDateChecker
from .bazi import BaZiCalculator
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
        self.bazi_calculator = BaZiCalculator()
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up MCP server handlers."""

        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="check_auspicious_date",
                    description="Analyzes whether a specific date is favorable for particular activities based on traditional Chinese calendar principles, including zodiac signs, five elements, lunar mansions, and other cultural factors. Returns a comprehensive score (0-10), auspiciousness level (very_good/good/neutral/poor/very_poor), and detailed analysis including what the date is good for and what to avoid.",
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
                    description="Searches through a specified date range to identify the most auspicious dates for a particular activity. This tool evaluates each date in the range using traditional Chinese calendar methods and returns the top favorable dates ranked by their auspiciousness score. Ideal for planning important events like weddings, business openings, or travel. You can limit the number of results to get only the best options.",
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
                    description="Provides comprehensive daily fortune analysis based on traditional Chinese almanac (通胜/黄历). Returns detailed information about the day's general energy, lucky directions, favorable colors, what activities are suitable, what to avoid, and overall fortune predictions. This gives a holistic view of the day's auspiciousness beyond specific activities.",
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
                    description="Analyzes the compatibility between two dates based on their Chinese zodiac animals and five elements. This is traditionally used for checking compatibility between birth dates for relationships, partnerships, or selecting compatible dates for joint ventures. Returns compatibility score, detailed analysis of how the zodiac signs interact, and recommendations.",
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
                    description="Retrieves all traditional festivals and cultural celebrations occurring on a specific date. For Chinese culture, this includes major festivals like Spring Festival (Chinese New Year), Mid-Autumn Festival, Dragon Boat Festival, and many others. Returns festival names, significance, traditional customs, and cultural importance of each celebration.",
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
                    description="Finds the next upcoming traditional festival after a given reference date. Useful for planning ahead and understanding which cultural celebration is approaching. Returns the festival name, exact date when it occurs, days remaining until the festival, and brief information about its significance and traditions.",
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
                    description="Provides in-depth information about a specific traditional festival including its historical origins, cultural significance, traditional customs and practices, symbolic meanings, typical foods, activities, and how it's celebrated. Perfect for learning about cultural traditions or planning authentic festival celebrations.",
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
                    description="Generates a complete calendar of all traditional festivals for an entire year. Returns a chronologically ordered list of all cultural celebrations including their dates (both solar and lunar), names, and brief descriptions. Excellent for creating cultural event calendars, planning year-round celebrations, or understanding the annual rhythm of traditional observances.",
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
                    description="Calculates precise moon phase information for a specific date and location using astronomical algorithms. Returns the moon phase name (new moon, waxing crescent, first quarter, waxing gibbous, full moon, waning gibbous, last quarter, waning crescent), illumination percentage, moon age in days, rise/set times, and position data. Location-aware calculations provide accurate local times.",
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
                    description="Creates a comprehensive monthly calendar showing moon phases for each day of the month. Displays daily moon phase names, illumination percentages, and highlights important lunar events (new moons, full moons, quarters). Perfect for gardening, fishing, photography planning, or any activities influenced by lunar cycles. Provides both visual and detailed numerical moon data.",
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
                    description="Analyzes how the moon's phase on a specific date influences various activities based on traditional beliefs and lunar wisdom. Different moon phases are believed to affect activities differently - e.g., new moons for new beginnings, full moons for completion, waxing moons for growth activities. Returns recommendations on whether the lunar phase supports or hinders the specified activity, with detailed explanations of the lunar influence.",
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
                    description="Predicts and lists all major moon phase transitions (new moons, first quarters, full moons, last quarters) within a specified date range. Provides exact dates and times for each lunar phase event. Useful for planning activities around specific moon phases, scheduling lunar observations, or understanding the lunar cycle progression over time. Includes astronomical accuracy for reliable predictions.",
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
                    description="Converts Gregorian (solar) calendar dates to traditional lunar calendar dates. Returns the corresponding lunar year, month, day, and leap month information if applicable. For Chinese calendar, also includes the year's zodiac animal, heavenly stem and earthly branch designations. Essential for finding lunar dates for traditional festivals, birth dates, or cultural events that follow the lunar calendar.",
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
                    description="Converts traditional lunar calendar dates to Gregorian (solar) calendar dates. Accurately handles leap months and provides the exact solar date equivalent. Useful for determining when lunar-based festivals occur on the solar calendar, converting lunar birth dates to solar dates, or scheduling events based on lunar calendar information. Includes validation for proper lunar date formats.",
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
                    description="Retrieves comprehensive zodiac information for a specific date. For Chinese zodiac, returns the zodiac animal (one of 12: Rat, Ox, Tiger, Rabbit, Dragon, Snake, Horse, Goat, Monkey, Rooster, Dog, Pig), associated element (Wood, Fire, Earth, Metal, Water), personality traits, compatible signs, lucky numbers, colors, and cultural significance. Provides both yearly and daily zodiac information based on the heavenly stems and earthly branches system.",
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
                    description="Efficiently analyzes multiple dates simultaneously for a specific activity's auspiciousness. Processes up to 30 dates in a single request, returning scores and levels for each date. Also identifies and highlights the best and worst dates in the batch. This bulk analysis tool is perfect for quickly evaluating several potential dates for an event, comparing options across a non-continuous date range, or conducting comparative analysis of multiple candidates.",
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
                    description="Performs comprehensive side-by-side comparison of multiple dates (up to 10) across various dimensions. For each date, returns auspiciousness analysis (if activity specified), moon phase details, festivals occurring, and zodiac information. Presents all information in an organized comparative format, making it easy to see differences and similarities. If an activity is specified, also provides a recommendation for which date is most suitable. Ideal for final decision-making between several good options.",
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
                    description="Identifies the most auspicious hours within a specific day based on traditional Chinese time divisions (12 two-hour periods corresponding to the 12 zodiac animals). Each period is analyzed and scored for general favorability and activity-specific suitability. Returns detailed information for each time period including its Chinese name, zodiac animal, auspiciousness score, suitable activities, and recommendations. Perfect for timing important activities, meetings, ceremonies, or decisions within a chosen date for maximum favorable energy.",
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
                Tool(
                    name="calculate_bazi",
                    description="Calculates BaZi (八字, Eight Characters) or Four Pillars of Destiny based on birth date and time. BaZi is a traditional Chinese fortune-telling method that analyzes the cosmic energies present at birth through four pillars (year, month, day, hour), each with a heavenly stem and earthly branch. Returns comprehensive analysis including: the eight characters, day master element, elemental balance, personality insights, life stage influences, favorable colors/directions, and career suggestions. Essential for understanding one's destiny, personality, and life path in Chinese metaphysics.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "birth_datetime": {
                                "type": "string",
                                "description": "Birth date and time in YYYY-MM-DD HH:MM format (24-hour)",
                            },
                            "timezone_offset": {
                                "type": "integer",
                                "description": "Timezone offset in hours from UTC (default: 8 for China Standard Time)",
                                "default": 8,
                            },
                        },
                        "required": ["birth_datetime"],
                    },
                ),
                Tool(
                    name="calculate_bazi_compatibility",
                    description="Analyzes compatibility between two people based on their BaZi (Eight Characters) charts. Compares the four pillars and elemental compositions of both individuals to assess relationship harmony, strengths, and challenges. Returns compatibility score (0-10), compatibility level (Excellent/Good/Fair/Challenging), element relationship analysis, and detailed insights about how the two destinies interact. Traditionally used for marriage compatibility, business partnerships, or understanding relationship dynamics in Chinese culture.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "birth_datetime1": {
                                "type": "string",
                                "description": "First person's birth date and time in YYYY-MM-DD HH:MM format",
                            },
                            "birth_datetime2": {
                                "type": "string",
                                "description": "Second person's birth date and time in YYYY-MM-DD HH:MM format",
                            },
                            "timezone_offset": {
                                "type": "integer",
                                "description": "Timezone offset in hours from UTC",
                                "default": 8,
                            },
                        },
                        "required": ["birth_datetime1", "birth_datetime2"],
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
                elif name == "calculate_bazi":
                    result = await self._calculate_bazi(**arguments)
                elif name == "calculate_bazi_compatibility":
                    result = await self._calculate_bazi_compatibility(**arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")

                return [TextContent(type="text", text=json.dumps(result, indent=2))]

            except Exception as e:
                error_result = {"error": str(e), "tool": name}
                return [
                    TextContent(type="text", text=json.dumps(error_result, indent=2))
                ]

        @self.server.list_prompts()
        async def handle_list_prompts() -> list[Prompt]:
            """List available prompts."""
            return [
                Prompt(
                    name="check_wedding_date",
                    description="Check if a date is auspicious for a wedding ceremony based on traditional Chinese calendar",
                    arguments=[
                        PromptArgument(
                            name="date",
                            description="The date to check in YYYY-MM-DD format",
                            required=True,
                        ),
                    ],
                ),
                Prompt(
                    name="calculate_bazi_chart",
                    description="Calculate BaZi (Four Pillars of Destiny) chart for a person's birth date and time",
                    arguments=[
                        PromptArgument(
                            name="birth_datetime",
                            description="Birth date and time in YYYY-MM-DD HH:MM format",
                            required=True,
                        ),
                        PromptArgument(
                            name="timezone_offset",
                            description="Timezone offset from UTC in hours (default: 8 for China)",
                            required=False,
                        ),
                    ],
                ),
                Prompt(
                    name="find_auspicious_dates",
                    description="Find the most auspicious dates for a specific activity within a date range",
                    arguments=[
                        PromptArgument(
                            name="start_date",
                            description="Start date of the range in YYYY-MM-DD format",
                            required=True,
                        ),
                        PromptArgument(
                            name="end_date",
                            description="End date of the range in YYYY-MM-DD format",
                            required=True,
                        ),
                        PromptArgument(
                            name="activity",
                            description="The activity type (e.g., wedding, business_opening, travel, moving)",
                            required=True,
                        ),
                    ],
                ),
                Prompt(
                    name="get_daily_almanac",
                    description="Get comprehensive daily almanac information including fortune, festivals, and recommendations",
                    arguments=[
                        PromptArgument(
                            name="date",
                            description="The date to check in YYYY-MM-DD format",
                            required=True,
                        ),
                    ],
                ),
                Prompt(
                    name="check_relationship_compatibility",
                    description="Analyze relationship compatibility between two people based on their BaZi charts",
                    arguments=[
                        PromptArgument(
                            name="person1_datetime",
                            description="First person's birth date and time in YYYY-MM-DD HH:MM format",
                            required=True,
                        ),
                        PromptArgument(
                            name="person2_datetime",
                            description="Second person's birth date and time in YYYY-MM-DD HH:MM format",
                            required=True,
                        ),
                    ],
                ),
            ]

        @self.server.get_prompt()
        async def handle_get_prompt(
            name: str, arguments: dict[str, str] | None
        ) -> GetPromptResult:
            """Get a specific prompt."""
            if arguments is None:
                arguments = {}

            if name == "check_wedding_date":
                date = arguments.get("date")
                if not date:
                    raise ValueError("Missing required argument: date")
                return GetPromptResult(
                    description="Check if a date is auspicious for a wedding",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=f"Please check if {date} is an auspicious date for a wedding ceremony. Use the check_auspicious_date tool with activity='wedding' and provide a detailed analysis including the lunar date, zodiac influences, and any recommendations.",
                            ),
                        ),
                    ],
                )
            elif name == "calculate_bazi_chart":
                birth_datetime = arguments.get("birth_datetime")
                if not birth_datetime:
                    raise ValueError("Missing required argument: birth_datetime")
                tz_offset = arguments.get("timezone_offset", "8")
                return GetPromptResult(
                    description="Calculate BaZi chart for birth date and time",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=f"Please calculate the BaZi (Four Pillars of Destiny) chart for someone born on {birth_datetime} with timezone offset {tz_offset}. Use the calculate_bazi tool and provide a comprehensive analysis including:\n1. The four pillars (year, month, day, hour)\n2. The eight characters (Heavenly Stems and Earthly Branches)\n3. Five elements distribution and balance\n4. Day Master analysis\n5. Personality insights\n6. Life recommendations",
                            ),
                        ),
                    ],
                )
            elif name == "find_auspicious_dates":
                start_date = arguments.get("start_date")
                end_date = arguments.get("end_date")
                activity = arguments.get("activity")
                if not start_date:
                    raise ValueError("Missing required argument: start_date")
                if not end_date:
                    raise ValueError("Missing required argument: end_date")
                if not activity:
                    raise ValueError("Missing required argument: activity")
                return GetPromptResult(
                    description="Find auspicious dates for an activity",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=f"Please find the most auspicious dates for '{activity}' between {start_date} and {end_date}. Use the find_good_dates tool and provide:\n1. Top recommended dates with scores\n2. Explanation of why each date is favorable\n3. Any dates to avoid and why\n4. Additional recommendations for the activity",
                            ),
                        ),
                    ],
                )
            elif name == "get_daily_almanac":
                date = arguments.get("date")
                if not date:
                    raise ValueError("Missing required argument: date")
                return GetPromptResult(
                    description="Get daily almanac information",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=f"Please provide a comprehensive daily almanac for {date}. Include:\n1. Daily fortune using get_daily_fortune tool\n2. Any festivals on this date using get_lunar_festivals tool\n3. Moon phase using get_moon_phase tool\n4. Lucky hours using get_lucky_hours tool\n5. Overall recommendations for the day",
                            ),
                        ),
                    ],
                )
            elif name == "check_relationship_compatibility":
                person1 = arguments.get("person1_datetime")
                person2 = arguments.get("person2_datetime")
                if not person1:
                    raise ValueError("Missing required argument: person1_datetime")
                if not person2:
                    raise ValueError("Missing required argument: person2_datetime")
                return GetPromptResult(
                    description="Check relationship compatibility",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=f"Please analyze the relationship compatibility between two people:\n- Person 1: born {person1}\n- Person 2: born {person2}\n\nUse the calculate_bazi_compatibility tool and provide:\n1. Compatibility score and level\n2. Element relationship analysis\n3. Strengths of the relationship\n4. Potential challenges\n5. Recommendations for harmony",
                            ),
                        ),
                    ],
                )
            else:
                raise ValueError(f"Unknown prompt: {name}")

        @self.server.list_resources()
        async def handle_list_resources() -> list[Resource]:
            """List available resources."""
            # Note: MCP Resource expects AnyUrl for uri but accepts string at runtime.
            # The pydantic model coerces strings to AnyUrl automatically.
            return [
                Resource(
                    uri="lunar://zodiac/animals",  # type: ignore[arg-type]
                    name="Chinese Zodiac Animals",
                    description="Information about the 12 Chinese zodiac animals and their characteristics",
                    mimeType="application/json",
                ),
                Resource(
                    uri="lunar://elements/five",  # type: ignore[arg-type]
                    name="Five Elements",
                    description="Information about the Five Elements (Wu Xing) and their relationships",
                    mimeType="application/json",
                ),
                Resource(
                    uri="lunar://festivals/major",  # type: ignore[arg-type]
                    name="Major Chinese Festivals",
                    description="List of major traditional Chinese festivals with descriptions",
                    mimeType="application/json",
                ),
                Resource(
                    uri="lunar://stems-branches/heavenly",  # type: ignore[arg-type]
                    name="Heavenly Stems",
                    description="The 10 Heavenly Stems (Tiangan) used in Chinese calendar",
                    mimeType="application/json",
                ),
                Resource(
                    uri="lunar://stems-branches/earthly",  # type: ignore[arg-type]
                    name="Earthly Branches",
                    description="The 12 Earthly Branches (Dizhi) used in Chinese calendar",
                    mimeType="application/json",
                ),
            ]

        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read a specific resource."""
            # Convert AnyUrl to string if needed
            uri_str = str(uri)
            content: dict[str, Any]
            if uri_str == "lunar://zodiac/animals":
                content = {
                    "zodiac_animals": [
                        {
                            "order": 1,
                            "animal": "Rat",
                            "chinese": "鼠",
                            "element": "Water",
                            "yin_yang": "Yang",
                            "traits": ["clever", "quick-witted", "resourceful"],
                        },
                        {
                            "order": 2,
                            "animal": "Ox",
                            "chinese": "牛",
                            "element": "Earth",
                            "yin_yang": "Yin",
                            "traits": ["diligent", "dependable", "strong"],
                        },
                        {
                            "order": 3,
                            "animal": "Tiger",
                            "chinese": "虎",
                            "element": "Wood",
                            "yin_yang": "Yang",
                            "traits": ["brave", "competitive", "confident"],
                        },
                        {
                            "order": 4,
                            "animal": "Rabbit",
                            "chinese": "兔",
                            "element": "Wood",
                            "yin_yang": "Yin",
                            "traits": ["gentle", "elegant", "alert"],
                        },
                        {
                            "order": 5,
                            "animal": "Dragon",
                            "chinese": "龍",
                            "element": "Earth",
                            "yin_yang": "Yang",
                            "traits": ["confident", "intelligent", "enthusiastic"],
                        },
                        {
                            "order": 6,
                            "animal": "Snake",
                            "chinese": "蛇",
                            "element": "Fire",
                            "yin_yang": "Yin",
                            "traits": ["wise", "enigmatic", "intuitive"],
                        },
                        {
                            "order": 7,
                            "animal": "Horse",
                            "chinese": "馬",
                            "element": "Fire",
                            "yin_yang": "Yang",
                            "traits": ["animated", "active", "energetic"],
                        },
                        {
                            "order": 8,
                            "animal": "Goat",
                            "chinese": "羊",
                            "element": "Earth",
                            "yin_yang": "Yin",
                            "traits": ["calm", "gentle", "sympathetic"],
                        },
                        {
                            "order": 9,
                            "animal": "Monkey",
                            "chinese": "猴",
                            "element": "Metal",
                            "yin_yang": "Yang",
                            "traits": ["sharp", "smart", "curiosity"],
                        },
                        {
                            "order": 10,
                            "animal": "Rooster",
                            "chinese": "雞",
                            "element": "Metal",
                            "yin_yang": "Yin",
                            "traits": ["observant", "hardworking", "courageous"],
                        },
                        {
                            "order": 11,
                            "animal": "Dog",
                            "chinese": "狗",
                            "element": "Earth",
                            "yin_yang": "Yang",
                            "traits": ["loyal", "honest", "prudent"],
                        },
                        {
                            "order": 12,
                            "animal": "Pig",
                            "chinese": "豬",
                            "element": "Water",
                            "yin_yang": "Yin",
                            "traits": ["compassionate", "generous", "diligent"],
                        },
                    ],
                    "cycle_years": "12-year cycle",
                    "description": "The Chinese Zodiac consists of 12 animals that appear in a fixed order, each associated with specific personality traits and elements.",
                }
            elif uri_str == "lunar://elements/five":
                content = {
                    "five_elements": [
                        {
                            "element": "Wood",
                            "chinese": "木",
                            "color": "green",
                            "season": "spring",
                            "direction": "east",
                            "generates": "Fire",
                            "controls": "Earth",
                        },
                        {
                            "element": "Fire",
                            "chinese": "火",
                            "color": "red",
                            "season": "summer",
                            "direction": "south",
                            "generates": "Earth",
                            "controls": "Metal",
                        },
                        {
                            "element": "Earth",
                            "chinese": "土",
                            "color": "yellow",
                            "season": "late summer",
                            "direction": "center",
                            "generates": "Metal",
                            "controls": "Water",
                        },
                        {
                            "element": "Metal",
                            "chinese": "金",
                            "color": "white",
                            "season": "autumn",
                            "direction": "west",
                            "generates": "Water",
                            "controls": "Wood",
                        },
                        {
                            "element": "Water",
                            "chinese": "水",
                            "color": "black",
                            "season": "winter",
                            "direction": "north",
                            "generates": "Wood",
                            "controls": "Fire",
                        },
                    ],
                    "cycles": {
                        "generation": "Wood → Fire → Earth → Metal → Water → Wood (生)",
                        "control": "Wood → Earth → Water → Fire → Metal → Wood (克)",
                    },
                    "description": "Wu Xing (Five Elements) is a fivefold conceptual scheme used in Chinese philosophy, traditional medicine, and calendar systems.",
                }
            elif uri_str == "lunar://festivals/major":
                content = {
                    "festivals": [
                        {
                            "name": "Spring Festival",
                            "chinese": "春節",
                            "lunar_date": "1st month, 1st day",
                            "description": "Chinese New Year, the most important traditional festival",
                        },
                        {
                            "name": "Lantern Festival",
                            "chinese": "元宵節",
                            "lunar_date": "1st month, 15th day",
                            "description": "Marks the end of New Year celebrations with lanterns",
                        },
                        {
                            "name": "Qingming Festival",
                            "chinese": "清明節",
                            "solar_term": "Around April 4-6",
                            "description": "Tomb-sweeping day to honor ancestors",
                        },
                        {
                            "name": "Dragon Boat Festival",
                            "chinese": "端午節",
                            "lunar_date": "5th month, 5th day",
                            "description": "Commemorates poet Qu Yuan with dragon boat races",
                        },
                        {
                            "name": "Qixi Festival",
                            "chinese": "七夕節",
                            "lunar_date": "7th month, 7th day",
                            "description": "Chinese Valentine's Day based on legend of the Cowherd and Weaver Girl",
                        },
                        {
                            "name": "Mid-Autumn Festival",
                            "chinese": "中秋節",
                            "lunar_date": "8th month, 15th day",
                            "description": "Moon worship festival with mooncakes",
                        },
                        {
                            "name": "Double Ninth Festival",
                            "chinese": "重陽節",
                            "lunar_date": "9th month, 9th day",
                            "description": "Climbing heights and honoring elders",
                        },
                        {
                            "name": "Winter Solstice",
                            "chinese": "冬至",
                            "solar_term": "Around December 21-23",
                            "description": "Important solar term for family gatherings",
                        },
                    ],
                    "description": "Major traditional Chinese festivals based on the lunar calendar and solar terms.",
                }
            elif uri_str == "lunar://stems-branches/heavenly":
                content = {
                    "heavenly_stems": [
                        {
                            "order": 1,
                            "stem": "Jia",
                            "chinese": "甲",
                            "element": "Wood",
                            "yin_yang": "Yang",
                        },
                        {
                            "order": 2,
                            "stem": "Yi",
                            "chinese": "乙",
                            "element": "Wood",
                            "yin_yang": "Yin",
                        },
                        {
                            "order": 3,
                            "stem": "Bing",
                            "chinese": "丙",
                            "element": "Fire",
                            "yin_yang": "Yang",
                        },
                        {
                            "order": 4,
                            "stem": "Ding",
                            "chinese": "丁",
                            "element": "Fire",
                            "yin_yang": "Yin",
                        },
                        {
                            "order": 5,
                            "stem": "Wu",
                            "chinese": "戊",
                            "element": "Earth",
                            "yin_yang": "Yang",
                        },
                        {
                            "order": 6,
                            "stem": "Ji",
                            "chinese": "己",
                            "element": "Earth",
                            "yin_yang": "Yin",
                        },
                        {
                            "order": 7,
                            "stem": "Geng",
                            "chinese": "庚",
                            "element": "Metal",
                            "yin_yang": "Yang",
                        },
                        {
                            "order": 8,
                            "stem": "Xin",
                            "chinese": "辛",
                            "element": "Metal",
                            "yin_yang": "Yin",
                        },
                        {
                            "order": 9,
                            "stem": "Ren",
                            "chinese": "壬",
                            "element": "Water",
                            "yin_yang": "Yang",
                        },
                        {
                            "order": 10,
                            "stem": "Gui",
                            "chinese": "癸",
                            "element": "Water",
                            "yin_yang": "Yin",
                        },
                    ],
                    "cycle": "10-stem cycle (Tiangan 天干)",
                    "description": "The Heavenly Stems are used together with Earthly Branches to form the 60-year cycle of the Chinese calendar.",
                }
            elif uri_str == "lunar://stems-branches/earthly":
                content = {
                    "earthly_branches": [
                        {
                            "order": 1,
                            "branch": "Zi",
                            "chinese": "子",
                            "zodiac": "Rat",
                            "hour": "23:00-01:00",
                            "month": 11,
                        },
                        {
                            "order": 2,
                            "branch": "Chou",
                            "chinese": "丑",
                            "zodiac": "Ox",
                            "hour": "01:00-03:00",
                            "month": 12,
                        },
                        {
                            "order": 3,
                            "branch": "Yin",
                            "chinese": "寅",
                            "zodiac": "Tiger",
                            "hour": "03:00-05:00",
                            "month": 1,
                        },
                        {
                            "order": 4,
                            "branch": "Mao",
                            "chinese": "卯",
                            "zodiac": "Rabbit",
                            "hour": "05:00-07:00",
                            "month": 2,
                        },
                        {
                            "order": 5,
                            "branch": "Chen",
                            "chinese": "辰",
                            "zodiac": "Dragon",
                            "hour": "07:00-09:00",
                            "month": 3,
                        },
                        {
                            "order": 6,
                            "branch": "Si",
                            "chinese": "巳",
                            "zodiac": "Snake",
                            "hour": "09:00-11:00",
                            "month": 4,
                        },
                        {
                            "order": 7,
                            "branch": "Wu",
                            "chinese": "午",
                            "zodiac": "Horse",
                            "hour": "11:00-13:00",
                            "month": 5,
                        },
                        {
                            "order": 8,
                            "branch": "Wei",
                            "chinese": "未",
                            "zodiac": "Goat",
                            "hour": "13:00-15:00",
                            "month": 6,
                        },
                        {
                            "order": 9,
                            "branch": "Shen",
                            "chinese": "申",
                            "zodiac": "Monkey",
                            "hour": "15:00-17:00",
                            "month": 7,
                        },
                        {
                            "order": 10,
                            "branch": "You",
                            "chinese": "酉",
                            "zodiac": "Rooster",
                            "hour": "17:00-19:00",
                            "month": 8,
                        },
                        {
                            "order": 11,
                            "branch": "Xu",
                            "chinese": "戌",
                            "zodiac": "Dog",
                            "hour": "19:00-21:00",
                            "month": 9,
                        },
                        {
                            "order": 12,
                            "branch": "Hai",
                            "chinese": "亥",
                            "zodiac": "Pig",
                            "hour": "21:00-23:00",
                            "month": 10,
                        },
                    ],
                    "cycle": "12-branch cycle (Dizhi 地支)",
                    "description": "The Earthly Branches correspond to the 12 zodiac animals and are used for time, dates, and years.",
                }
            else:
                raise ValueError(f"Unknown resource: {uri_str}")

            return json.dumps(content, indent=2, ensure_ascii=False)

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

    async def _calculate_bazi(
        self, birth_datetime: str, timezone_offset: int = 8
    ) -> dict[str, Any]:
        """Calculate BaZi (Eight Characters) for a birth datetime."""
        return await self.bazi_calculator.calculate_bazi(
            birth_datetime, timezone_offset
        )

    async def _calculate_bazi_compatibility(
        self, birth_datetime1: str, birth_datetime2: str, timezone_offset: int = 8
    ) -> dict[str, Any]:
        """Calculate BaZi compatibility between two birth datetimes."""
        return await self.bazi_calculator.get_compatibility(
            birth_datetime1, birth_datetime2, timezone_offset
        )

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
