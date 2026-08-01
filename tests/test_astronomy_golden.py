"""Golden fixtures for the astronomy dependency upgrade.

The public API accepts calendar dates, which Skyfield evaluates at 00:00 UTC.
Locations are currently normalized and echoed but do not alter the placeholder
rise/set calculation. These fixtures intentionally preserve those v1.2.0
semantics while dependency versions change.
"""

from pathlib import Path

import pytest
from skyfield.iokit import Loader

from lunar_mcp_server.lunar_calculations import LunarCalculator


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("date", "phase_name", "illumination", "phase_angle"),
    [
        ("2024-01-11", "Full Moon", 0.995, 8.4),
        ("2024-01-18", "First Quarter", 0.518, 87.9),
        ("2024-01-25", "New Moon", 0.007, 170.3),
        ("2024-02-02", "First Quarter", 0.405, 100.9),
        ("2024-03-10", "Full Moon", 0.997, 6.0),
        ("2024-03-17", "First Quarter", 0.518, 87.9),
        ("2024-03-25", "New Moon", 0.001, 176.6),
        ("2024-04-02", "First Quarter", 0.485, 91.7),
    ],
)
async def test_phase_boundaries_preserve_v1_2_0_outputs(
    date: str, phase_name: str, illumination: float, phase_angle: float
) -> None:
    """Preserve phase labels and rounded numerical outputs at key boundaries."""
    result = await LunarCalculator().get_moon_phase(date)

    assert result["phase_name"] == phase_name
    assert result["illumination"] == illumination
    assert result["phase_angle"] == phase_angle


@pytest.mark.asyncio
async def test_utc_date_boundary_and_taipei_coordinates_are_stable() -> None:
    """Preserve consecutive 00:00 UTC results and coordinate normalization."""
    calculator = LunarCalculator()
    dec_31 = await calculator.get_moon_phase("2024-12-31", "25.033,121.5654")
    jan_1 = await calculator.get_moon_phase("2025-01-01", "25.033,121.5654")

    assert (dec_31["phase_name"], dec_31["illumination"], dec_31["phase_angle"]) == (
        "Full Moon",
        0.998,
        5.0,
    )
    assert (jan_1["phase_name"], jan_1["illumination"], jan_1["phase_angle"]) == (
        "Waxing Gibbous",
        0.985,
        13.9,
    )
    assert dec_31["location"] == jan_1["location"] == "25.033,121.5654"


def test_bundled_ephemeris_loads_offline(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Initialization must use packaged DE421 data without a download or CWD file."""

    def fail_download(*args: object, **kwargs: object) -> None:
        raise AssertionError("an offline initialization attempted a download")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Loader, "download", fail_download)

    calculator = LunarCalculator()

    assert calculator.eph.path.endswith("lunar_mcp_server/data/de421.bsp")
