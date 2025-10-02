"""Pytest configuration and fixtures."""

import asyncio
from collections.abc import Generator

import pytest


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_dates():
    """Sample dates for testing."""
    return {
        "valid_date": "2024-01-15",
        "invalid_date": "invalid-date",
        "spring_festival": "2024-02-10",
        "mid_autumn": "2024-09-17",
        "christmas": "2024-12-25",
    }


@pytest.fixture
def sample_activities():
    """Sample activities for testing."""
    return [
        "wedding",
        "business_opening",
        "travel",
        "surgery",
        "moving",
        "planting",
        "celebration",
    ]


@pytest.fixture
def sample_cultures():
    """Sample cultures for testing."""
    return ["chinese", "islamic", "hindu", "western"]


@pytest.fixture
def mock_moon_data():
    """Mock moon phase data for testing."""
    return {
        "date": "2024-01-15",
        "phase_name": "Full Moon",
        "illumination": 0.98,
        "lunar_day": 15,
        "zodiac_sign": "Capricorn",
        "influence": {
            "good_for": ["completion", "celebration"],
            "avoid": ["starting new projects"],
            "energy_type": "culmination",
        },
    }


@pytest.fixture
def mock_festival_data():
    """Mock festival data for testing."""
    return {
        "date": "2024-02-10",
        "festivals": [
            {
                "name": "Chinese New Year",
                "culture": "chinese",
                "significance": "Beginning of lunar new year",
                "traditions": ["family reunion", "fireworks"],
                "is_major": True,
            }
        ],
        "festival_count": 1,
        "is_major_festival": True,
    }


@pytest.fixture
def mock_zodiac_data():
    """Mock zodiac data for testing."""
    return {
        "date": "2024-01-15",
        "culture": "chinese",
        "year_zodiac": {"animal": "Dragon", "element": "Wood", "yin_yang": "Yang"},
        "daily_zodiac": {"animal": "Ox", "traits": {"personality": "reliable, strong"}},
    }
