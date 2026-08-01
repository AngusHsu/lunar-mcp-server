"""Golden Chinese calendar and festival fixtures."""

import pytest

from lunar_mcp_server.calendar_conversions import CalendarConverter
from lunar_mcp_server.festivals import FestivalManager

SOLAR_TO_LUNAR_CASES = [
    ("2023-03-21", (2023, 2, 30, False)),
    ("2023-03-22", (2023, 2, 1, True)),
    ("2023-04-19", (2023, 2, 29, True)),
    ("2023-04-20", (2023, 3, 1, False)),
    ("2024-02-09", (2023, 12, 30, False)),
    ("2024-02-10", (2024, 1, 1, False)),
    ("2024-06-10", (2024, 5, 5, False)),
    ("2024-09-17", (2024, 8, 15, False)),
    ("2025-01-28", (2024, 12, 29, False)),
    ("2025-01-29", (2025, 1, 1, False)),
]

LUNAR_TO_SOLAR_CASES = [
    ("2024-1-1", "2024-02-10"),
    ("2024-5-5", "2024-06-10"),
    ("2024-8-15", "2024-09-17"),
    ("2025-1-1", "2025-01-29"),
]

FESTIVAL_CASES = [
    ("2024-02-10", "Spring Festival (Chinese New Year)"),
    ("2024-06-10", "Dragon Boat Festival"),
    ("2024-09-17", "Mid-Autumn Festival"),
    ("2025-01-29", "Spring Festival (Chinese New Year)"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(("solar_date", "expected"), SOLAR_TO_LUNAR_CASES)
async def test_solar_to_lunar_boundaries(
    solar_date: str, expected: tuple[int, int, int, bool]
) -> None:
    """Preserve new-year, leap-month, and major-festival conversions."""
    result = await CalendarConverter().solar_to_lunar(solar_date)

    assert "error" not in result
    actual = (
        result["lunar_year"],
        result["lunar_month"],
        result["lunar_day"],
        result["is_leap_month"],
    )
    assert actual == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(("lunar_date", "solar_date"), LUNAR_TO_SOLAR_CASES)
async def test_lunar_to_solar_major_dates(lunar_date: str, solar_date: str) -> None:
    """Preserve reverse conversion for major lunar dates across years."""
    result = await CalendarConverter().lunar_to_solar(lunar_date)

    assert "error" not in result
    assert result["solar_date"] == solar_date


@pytest.mark.asyncio
@pytest.mark.parametrize(("solar_date", "festival_name"), FESTIVAL_CASES)
async def test_major_festival_dates(solar_date: str, festival_name: str) -> None:
    """Preserve the validated Gregorian dates of major lunar festivals."""
    result = await FestivalManager().get_festivals_for_date(solar_date)

    assert "error" not in result
    assert festival_name in {festival["name"] for festival in result["festivals"]}


@pytest.mark.asyncio
async def test_zodiac_boundary_follows_lunar_new_year() -> None:
    """Preserve the Rabbit-to-Dragon boundary across Lunar New Year 2024."""
    converter = CalendarConverter()
    before = await converter.solar_to_lunar("2024-02-09")
    after = await converter.solar_to_lunar("2024-02-10")

    assert before["zodiac_info"]["animal"] == "Rabbit"
    assert after["zodiac_info"]["animal"] == "Dragon"
