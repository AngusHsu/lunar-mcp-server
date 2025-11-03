# Changelog

All notable changes to the Lunar Calendar MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-03

### 🔮 Major Feature: BaZi (八字) Four Pillars of Destiny

This release adds comprehensive traditional Chinese fortune-telling capabilities through the BaZi (Eight Characters) system.

### Added

#### New Features
- **BaZi Calculation System**: Complete Four Pillars of Destiny analysis
  - Year Pillar (年柱): Ancestors and early life (0-15 years)
  - Month Pillar (月柱): Parents and youth (16-30 years)
  - Day Pillar (日柱): Self and middle age (31-45 years)
  - Hour Pillar (时柱): Children and later life (46+ years)
- **Sexagenary Cycle**: Accurate 60-day/year cycle implementation
- **Solar Terms Integration**: Month pillar based on 24 traditional solar terms (节气)
- **Five Elements Analysis**: Complete Wood, Fire, Earth, Metal, Water distribution and balance
- **Day Master (日主)**: Core personality element and characteristic analysis
- **BaZi Compatibility**: Relationship harmony analysis based on element interactions
- **Element Recommendations**:
  - Favorable colors based on element balance
  - Favorable directions (feng shui)
  - Career path suggestions
  - Life stage insights

#### New MCP Tools (2)
- `calculate_bazi`: Calculate complete BaZi chart from birth datetime
  - Input: Birth datetime (YYYY-MM-DD HH:MM), timezone offset
  - Output: Eight characters, four pillars, element analysis, recommendations
- `calculate_bazi_compatibility`: Analyze compatibility between two people
  - Input: Two birth datetimes, timezone offset
  - Output: Compatibility score (0-10), level, element relationships, detailed analysis

#### New Modules
- `src/lunar_mcp_server/bazi.py` (720 lines): Complete BaZi calculation engine
  - 10 Heavenly Stems (天干) with elements and polarity
  - 12 Earthly Branches (地支) with zodiac animals
  - Solar term boundary calculations
  - Element analysis algorithms
  - Compatibility scoring system

#### Documentation
- **Implementation Guide** (`docs/implementation-guide.md`, 468 lines):
  - Comprehensive data sources documentation
  - Algorithm explanations (Sexagenary cycle, solar terms)
  - Traditional Chinese calendar system details
  - Technical implementation notes
  - References to traditional and astronomical sources

### Enhanced

#### Testing
- **162 total tests** (up from 90, +80% increase)
- **77% code coverage** (up from 57%, +20%)
- **New test files**:
  - `tests/test_bazi.py` (586 lines, 52 tests) - 94% coverage
  - `tests/test_calendar_conversions.py` (303 lines, 40 tests) - 75% coverage
  - `tests/test_festivals.py` (250 lines, 30 tests) - 78% coverage
  - Enhanced `tests/test_server.py` (+327 lines, 22 new tests)
- **Test execution time**: 1.74 seconds (all passing)

#### Coverage Improvements
- `bazi.py`: 94% (NEW)
- `auspicious_dates.py`: 85% (up from 81%, +4%)
- `festivals.py`: 78% (up from 17%, +61%)
- `calendar_conversions.py`: 75% (up from 31%, +44%)
- `server.py`: 68% (up from 30%, +38%)

#### README Updates
- Updated tool count: 20 tools (was 18)
- Added comprehensive BaZi section
- Updated feature list and examples
- Added BaZi usage examples

### Technical Details

#### Implementation
- **Timezone-aware calculations**: Adjustable timezone support (defaults to China +8)
- **Spring Begins (立春) handling**: Correct year pillar calculation around Chinese New Year
- **Reference system**: February 4, 1984 (甲子 Jia-Zi) as calculation reference
- **Full type hints**: Complete type safety throughout
- **Async/await pattern**: Non-blocking operations
- **Comprehensive error handling**: Graceful handling of invalid inputs

#### Data Sources
- Traditional Chinese calendar systems
- 24 Solar Terms (节气) for accurate month calculations
- Wu Xing (五行) Five Elements theory
- Generation (生) and Control (克) cycles

### Quality Assurance
- ✅ All 162 tests passing (100% pass rate)
- ✅ Code quality checks passing (black, ruff, mypy)
- ✅ CI/CD pipeline green on all Python versions (3.11, 3.12)
- ✅ MCP server tests passing
- ✅ No breaking changes

### Files Changed
- **New files**: 5 (bazi.py, 3 test files, implementation guide)
- **Modified files**: 4 (.gitignore, README.md, server.py, test_server.py)
- **Total changes**: +2,799 lines, -1 line

### Migration Notes
- No breaking changes
- Purely additive feature
- Existing tools and functionality unchanged
- New tools are optional to use

## [1.0.1] - 2025-10-05

### Changed
- **Enhanced Tool Descriptions**: Updated all 18 MCP tool descriptions with comprehensive documentation
  - Added detailed explanations of functionality, methodology, and return values
  - Included specific use cases and practical applications for each tool
  - Improved context for AI applications and users to understand tool capabilities
  - Better discoverability through richer descriptions

### Improved
- **Documentation Quality**: Tool descriptions now provide clear guidance on:
  - What each tool does and how it works
  - Expected output and data formats
  - When and why to use each tool
  - Special features and limitations

## [1.0.0] - 2025-10-03

### 🎉 First Stable Release

This marks the first production-ready release of the Lunar Calendar MCP Server. The server is now fully tested, documented, and ready for widespread use.

### Added
- **PyPI Publishing**: Now available via `pip install lunar-mcp-server`
- **GitHub Actions Workflow**: Automated PyPI publishing with quality gates
- **Smithery.ai Configuration**: Ready for MCP registry publishing
- **Comprehensive Documentation**:
  - `docs/usage-examples.md` - Practical examples and integration guides
  - `docs/tools-reference.md` - Complete API documentation for all 18 tools
  - `docs/cultural-traditions.md` - Understanding Chinese calendar systems
  - `docs/development.md` - Contributing and development guide
  - `docs/smithery-publishing.md` - Publishing to MCP registry

### Changed
- **Reorganized README**: Streamlined to focus on quick start, now links to detailed docs
- **Improved Documentation Structure**: Moved detailed content to modular docs/ directory

### Removed
- **main.py**: Removed unused placeholder file (entry point properly configured in pyproject.toml)

### Quality Assurance
- ✅ All code quality checks passing (black, isort, ruff, mypy)
- ✅ 18/18 MCP tools tested and validated (100% pass rate)
- ✅ Complete test coverage with pytest
- ✅ Production-ready for PyPI distribution

### Installation
```bash
# Using pip
pip install lunar-mcp-server

# Using uvx (no installation)
uvx lunar-mcp-server

# Claude Desktop integration
# Add to claude_desktop_config.json:
{
  "mcpServers": {
    "lunar-calendar": {
      "command": "uvx",
      "args": ["lunar-mcp-server"]
    }
  }
}
```

## [0.1.1] - 2025-01-03

### Fixed
- **Code Quality**: Fixed all ruff linting issues (124 auto-fixed, 5 noqa comments for intentional imports)
- **Type Safety**: Resolved all 20 mypy type errors for strict type checking compliance
- **Festival Type Checking**: Improved type safety in festival name lookups and regional name handling
- **Import Validation**: Added proper noqa comments for availability-check imports (skyfield, ephem, chinese_calendar)

### Changed
- **Code Formatting**: Applied black formatting to all 13 source files
- **Import Organization**: Sorted imports with isort across 10 files
- **Ruff Configuration**: Updated pyproject.toml to use new `lint` section format (deprecated top-level settings)
- **Mypy Configuration**: Added pytz and skyfield to ignored imports list

### Improved
- **Test Coverage**: Enhanced test_mcp_server.sh to test all 18 tools (previously 15)
  - Added `batch_check_dates` test
  - Added `compare_dates` test
  - Added `get_lucky_hours` test
- **Test Validation**: Improved JSON-RPC 2.0 response structure validation
- **Test Reliability**: Increased initialization delay from 1s to 2s to prevent race conditions
- **Test Documentation**: Added header comments explaining FIFO-based testing approach
- **Tool Count Verification**: Added validation to ensure all 18 tools are present

### Technical Details
- All code now passes professional Python quality standards:
  - ✅ black (code formatting)
  - ✅ isort (import sorting)
  - ✅ ruff (linting - 100% pass rate)
  - ✅ mypy (type checking - strict mode)
- Test suite: 18/18 tools passing with comprehensive validation
- 3 commits: formatting fixes, type error resolution, test improvements

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

[1.0.1]: https://github.com/AngusHsu/lunar-mcp-server/releases/tag/v1.0.1
[1.0.0]: https://github.com/AngusHsu/lunar-mcp-server/releases/tag/v1.0.0
[0.1.1]: https://github.com/AngusHsu/lunar-mcp-server/releases/tag/v0.1.1
[0.1.0]: https://github.com/AngusHsu/lunar-mcp-server/releases/tag/v0.1.0
