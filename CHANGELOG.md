# Changelog

All notable changes to the Lunar Calendar MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-03

### Added
- Initial release of Chinese Lunar Calendar MCP Server
- **18 MCP Tools** across 5 categories
- Focus on traditional Chinese lunar calendar and cultural practices

#### Auspicious Date Tools (4 tools)
- `check_auspicious_date` - Check if dates are favorable for specific activities
- `find_good_dates` - Find optimal dates within a range
- `get_daily_fortune` - Get comprehensive daily fortune information
- `check_zodiac_compatibility` - Check compatibility between dates

#### Festival Tools (4 tools)
- `get_lunar_festivals` - Get festivals for a specific date
- `get_next_festival` - Find the next upcoming festival
- `get_festival_details` - Get detailed festival information
- `get_annual_festivals` - Get all festivals for a year

#### Moon Phase Tools (4 tools)
- `get_moon_phase` - Get current moon phase for a date
- `get_moon_calendar` - Get monthly moon phase calendar
- `get_moon_influence` - Understand moon's influence on activities
- `predict_moon_phases` - Predict moon phases for a date range

#### Calendar Conversion Tools (3 tools)
- `solar_to_lunar` - Convert Gregorian to Chinese lunar date
- `lunar_to_solar` - Convert Chinese lunar to Gregorian date
- `get_zodiac_info` - Get detailed Chinese zodiac information

#### Advanced Tools (3 tools)
- `batch_check_dates` - Check multiple dates at once (up to 30)
- `compare_dates` - Side-by-side comparison of dates
- `get_lucky_hours` - Get auspicious hours within a day (12 Chinese time periods)

### Features

#### Chinese Cultural Elements
- **Lunar Calendar** - Traditional Chinese lunar calendar with accurate conversions
- **12 Zodiac Animals** - Rat, Ox, Tiger, Rabbit, Dragon, Snake, Horse, Goat, Monkey, Rooster, Dog, Pig
- **Five Elements** - Wood, Fire, Earth, Metal, Water with generative/destructive relationships
- **28 Lunar Mansions** (二十八宿) - Traditional stellar mansions for auspiciousness
- **Traditional Festivals** - Spring Festival, Mid-Autumn, Dragon Boat, Lantern Festival, Qingming, and more
- **Sexagenary Cycle** (天干地支) - 60-year cycle with Heavenly Stems and Earthly Branches

#### Intelligence Features
- **Response Explanations** - Detailed "why" explanations for all recommendations
- **Reasoning Breakdown** - Zodiac, elements, moon phase, and lunar mansion analysis
- **Alternative Suggestions** - Automatic better date suggestions when score < 7
- **Score Transparency** - Complete score breakdown showing calculation

#### Technical Features
- Python 3.11+ support
- Async/await throughout for non-blocking operations
- MCP protocol 2024-11-05 compliant
- STDIO transport mode
- Comprehensive test suite (18/18 tests passing - 100%)
- Full type hints and mypy compatibility
- Professional astronomical libraries (Skyfield, Astropy, Ephem)

### Dependencies
- **Core**: mcp, skyfield, ephem, astropy, pydantic
- **Calendar**: lunardate, zhdate, chinese-calendar
- **Utilities**: python-dateutil, pytz, typing-extensions
- **Development**: pytest, black, isort, mypy, ruff, pre-commit

### Documentation
- Complete README with usage examples
- STDIO usage guide in `docs/stdio-usage.md`
- Testing documentation in `docs/testing.md`
- Implementation summaries:
  - `IMPLEMENTATION_SUMMARY.md` - Phase 1 features
  - `IMPLEMENTATION_SUMMARY_PHASE2.md` - Intelligence features
- Future improvements roadmap in `docs/future-improvements.md`

### Testing
- 18/18 tools tested successfully (100% pass rate)
- Categories tested:
  - Auspicious/Fortune: 4/4 ✅
  - Festival: 4/4 ✅
  - Moon/Lunar: 4/4 ✅
  - Calendar Conversion: 3/3 ✅
  - Advanced Tools: 3/3 ✅
- Comprehensive error handling tests
- Chinese cultural context validation

### Known Limitations
- Lunar calendar conversions use approximations when specialized libraries unavailable
- Astronomical data download required for highest accuracy
- Cultural interpretations based on traditional sources (通書/通胜)
- Currently focused on Chinese traditions only

### Removed in This Version
- Multi-cultural support (Islamic, Hindu, Western) - focused exclusively on Chinese traditions
- Dependencies: `convertdate`, `hijri-converter` (no longer needed)

[0.1.0]: https://github.com/AngusHsu/lunar-mcp-server/releases/tag/v0.1.0
