# Implementation Guide

This document provides detailed information about the data sources, algorithms, and implementation approach used in the Lunar Calendar MCP Server.

## Table of Contents

- [Data Sources](#data-sources)
- [Architecture Overview](#architecture-overview)
- [Core Modules](#core-modules)
- [Algorithm Details](#algorithm-details)
- [Calendar Systems](#calendar-systems)
- [Technical Implementation](#technical-implementation)

---

## Data Sources

### Traditional Chinese Calendar Systems

The implementation is based on well-established traditional Chinese calendar systems and astronomical calculations:

#### 1. **Lunar Calendar Data**
- **Source**: Traditional Chinese lunar-solar calendar system
- **Libraries Used**:
  - `lunardate` - Python library for lunar date conversions
  - `zhdate` - Chinese lunar calendar library
  - `chinese-calendar` - Festival and holiday data
- **Method**: These libraries provide accurate lunar calendar calculations based on traditional Chinese astronomical observations and calendar rules

#### 2. **Astronomical Calculations**
- **Source**: NASA JPL ephemeris data (DE421)
- **Libraries Used**:
  - `skyfield` - High-precision astronomy computations
  - `ephem` - Astronomical calculations
  - `astropy` - Professional astronomy library
- **Data File**: `de421.bsp` (Development Ephemeris 421) - NASA's planetary position database
- **Accuracy**: Sub-arcsecond precision for moon phase calculations

#### 3. **BaZi (八字) System**
- **Source**: Traditional Chinese Four Pillars astrology
- **Reference System**:
  - Sexagenary cycle (60-day/year cycle)
  - Solar terms (24 节气) for month calculations
  - Reference date: February 4, 1984 (甲子 Jia-Zi day)
- **Components**:
  - **Heavenly Stems** (天干): 10 stems derived from Five Elements theory
  - **Earthly Branches** (地支): 12 branches corresponding to zodiac animals
  - **Solar Terms**: 24 seasonal markers based on Earth's orbit around the Sun

#### 4. **Five Elements Theory**
- **Source**: Traditional Chinese Wu Xing (五行) philosophy
- **Elements**: Wood (木), Fire (火), Earth (土), Metal (金), Water (水)
- **Cycles**:
  - Generation Cycle (生): Wood → Fire → Earth → Metal → Water → Wood
  - Control Cycle (克): Wood → Earth → Water → Fire → Metal → Wood

#### 5. **Zodiac System**
- **Source**: Traditional Chinese zodiac (生肖)
- **12 Animals**: Rat, Ox, Tiger, Rabbit, Dragon, Snake, Horse, Goat, Monkey, Rooster, Dog, Pig
- **Calculation**: Based on Chinese New Year (Spring Festival), which occurs between January 21 and February 20
- **Daily Zodiac**: Additional 12-day cycle for daily zodiac animal determination

#### 6. **Auspicious Date Calculations**
- **Source**: Traditional Chinese almanac (通胜/黄历)
- **Factors Considered**:
  - Zodiac compatibility
  - Five Elements interactions
  - Lunar mansion positions (28宿)
  - Day stem-branch combinations
  - Activity-specific favorable/unfavorable indicators

#### 7. **Festival Data**
- **Source**: Chinese cultural calendar
- **Coverage**: Major traditional festivals including:
  - Spring Festival (Chinese New Year)
  - Lantern Festival
  - Dragon Boat Festival
  - Mid-Autumn Festival
  - Double Ninth Festival
  - And many others

---

## Architecture Overview

### System Design

The MCP server follows a modular architecture with clear separation of concerns:

```
lunar-mcp-server/
├── src/lunar_mcp_server/
│   ├── server.py              # MCP server implementation
│   ├── bazi.py                # BaZi calculations
│   ├── calendar_conversions.py # Calendar conversion utilities
│   ├── lunar_calculations.py   # Moon phase calculations
│   ├── auspicious_dates.py    # Date analysis
│   ├── festivals.py           # Festival information
│   └── cultural_data/         # Cultural reference data
│       └── chinese.py         # Chinese cultural data
├── tests/                     # Comprehensive test suite
└── docs/                      # Documentation
```

### Design Principles

1. **Modularity**: Each module handles a specific domain (BaZi, moon phases, festivals, etc.)
2. **Accuracy**: Using professional astronomical libraries and traditional reference systems
3. **Fallback Support**: Graceful degradation when optional libraries are unavailable
4. **Type Safety**: Full type hints using Python's typing system
5. **Async-First**: All operations use async/await for optimal performance
6. **Error Handling**: Comprehensive error handling with meaningful error messages

---

## Core Modules

### 1. BaZi Calculator (`bazi.py`)

**Purpose**: Calculate Four Pillars of Destiny and compatibility analysis

**Key Features**:
- Four pillars calculation (Year, Month, Day, Hour)
- Sexagenary cycle implementation
- Solar term-based month pillar
- Timezone-aware calculations
- Element analysis and balance
- Compatibility scoring

**Algorithm Overview**:
```python
# Simplified algorithm flow
1. Parse birth datetime and adjust for timezone
2. Calculate Year Pillar:
   - Check if before Spring Begins (Feb 4)
   - Use appropriate year for stem-branch calculation
3. Calculate Month Pillar:
   - Determine solar term period
   - Calculate stem based on year stem
4. Calculate Day Pillar:
   - Use sexagenary cycle from reference date
5. Calculate Hour Pillar:
   - Map hour to 2-hour period (12 periods)
   - Calculate stem based on day stem
6. Analyze five elements distribution
7. Generate recommendations
```

**Reference System**:
- **Reference Date**: February 4, 1984 = 甲子 (Jia-Zi)
- **Stem Cycle**: 10 days
- **Branch Cycle**: 12 days
- **Full Cycle**: 60 days (LCM of 10 and 12)

### 2. Calendar Conversions (`calendar_conversions.py`)

**Purpose**: Convert between solar and lunar calendars, provide zodiac information

**Implementation Approach**:
1. **Primary**: Use specialized libraries (`zhdate`, `lunardate`)
2. **Fallback**: Approximate calculation when libraries unavailable
3. **Zodiac Calculation**: Based on year offset from reference year (1900)

**Zodiac Algorithm**:
```python
# Year zodiac calculation
year_diff = year - 1900  # Reference year (Rat)
zodiac_index = year_diff % 12
element_cycle = year_diff % 10
element_index = element_cycle // 2
```

### 3. Lunar Calculations (`lunar_calculations.py`)

**Purpose**: Calculate moon phases and astronomical data

**Data Source**: NASA JPL DE421 ephemeris

**Capabilities**:
- Moon phase calculation (illumination percentage, phase name)
- Moon rise/set times
- Monthly moon calendar
- Moon phase predictions
- Activity influence based on moon phase

**Phase Calculation**:
```python
# Moon phase determination
illumination = calculate_illumination(date, observer)
if illumination < 0.01: phase = "New Moon"
elif illumination < 0.47: phase = "Waxing Crescent"
elif illumination < 0.53: phase = "First Quarter"
# ... and so on
```

### 4. Auspicious Dates (`auspicious_dates.py`)

**Purpose**: Analyze date favorability for specific activities

**Scoring Factors**:
1. Zodiac day animal compatibility
2. Five Elements harmony
3. Lunar mansion influence
4. Activity-specific indicators
5. Traditional almanac rules

**Scoring System**:
- Score range: 0-10
- Levels: Very Poor (0-2), Poor (2-4), Neutral (4-6), Good (6-8), Very Good (8-10)

### 5. Festivals (`festivals.py`)

**Purpose**: Provide information about traditional Chinese festivals

**Data Organization**:
- Festival names (Chinese and English)
- Solar and lunar dates
- Cultural significance
- Traditional customs
- Symbolic meanings

---

## Algorithm Details

### Sexagenary Cycle (干支纪年法)

The 60-year/day cycle combines 10 Heavenly Stems with 12 Earthly Branches:

**Heavenly Stems (天干)**:
1. 甲 (Jiǎ) - Yang Wood
2. 乙 (Yǐ) - Yin Wood
3. 丙 (Bǐng) - Yang Fire
4. 丁 (Dīng) - Yin Fire
5. 戊 (Wù) - Yang Earth
6. 己 (Jǐ) - Yin Earth
7. 庚 (Gēng) - Yang Metal
8. 辛 (Xīn) - Yin Metal
9. 壬 (Rén) - Yang Water
10. 癸 (Guǐ) - Yin Water

**Earthly Branches (地支)**:
1. 子 (Zǐ) - Rat, Water
2. 丑 (Chǒu) - Ox, Earth
3. 寅 (Yín) - Tiger, Wood
4. 卯 (Mǎo) - Rabbit, Wood
5. 辰 (Chén) - Dragon, Earth
6. 巳 (Sì) - Snake, Fire
7. 午 (Wǔ) - Horse, Fire
8. 未 (Wèi) - Goat, Earth
9. 申 (Shēn) - Monkey, Metal
10. 酉 (Yǒu) - Rooster, Metal
11. 戌 (Xū) - Dog, Earth
12. 亥 (Hài) - Pig, Water

**Cycle Calculation**:
```python
def get_sexagenary(offset, reference=(0, 0)):
    stem = (reference[0] + offset) % 10
    branch = (reference[1] + offset) % 12
    return (stem, branch)
```

### Solar Terms (节气)

24 solar terms divide the year into seasonal periods:

**Major Terms** (used for month pillar):
- 立春 (Lì Chūn) - Spring Begins (~Feb 4)
- 惊蛰 (Jīng Zhé) - Awakening of Insects (~Mar 6)
- 清明 (Qīng Míng) - Pure Brightness (~Apr 5)
- 立夏 (Lì Xià) - Summer Begins (~May 6)
- 芒种 (Máng Zhòng) - Grain in Ear (~Jun 6)
- 小暑 (Xiǎo Shǔ) - Slight Heat (~Jul 7)
- 立秋 (Lì Qiū) - Autumn Begins (~Aug 8)
- 白露 (Bái Lù) - White Dew (~Sep 8)
- 寒露 (Hán Lù) - Cold Dew (~Oct 8)
- 立冬 (Lì Dōng) - Winter Begins (~Nov 7)
- 大雪 (Dà Xuě) - Major Snow (~Dec 7)
- 小寒 (Xiǎo Hán) - Slight Cold (~Jan 6)

### Moon Phase Calculation

Using astronomical libraries to calculate precise lunar illumination:

```python
# Simplified moon phase calculation
1. Load planetary ephemeris (DE421)
2. Calculate Sun and Moon positions
3. Determine phase angle between Sun-Earth-Moon
4. Calculate illumination percentage
5. Classify into 8 traditional phases
```

---

## Calendar Systems

### Chinese Lunar Calendar

**Characteristics**:
- Lunisolar calendar (months follow moon, years follow sun)
- 12 or 13 months per year (leap months added periodically)
- Months begin on new moon
- Each month has 29 or 30 days
- New Year occurs on second new moon after winter solstice

**Leap Month Rules**:
- Leap months ensure calendar stays aligned with seasons
- Leap month inserted approximately every 3 years
- Maintains synchronization with solar year

### Solar Calendar to Lunar Conversion

**Process**:
1. Determine Chinese New Year date for the year
2. Calculate days since New Year
3. Determine lunar month and day
4. Check for leap month conditions
5. Return lunar date with zodiac information

---

## Technical Implementation

### Error Handling Strategy

**Multi-Level Fallback**:
```python
try:
    # Try primary library (zhdate)
    return accurate_calculation()
except ImportError:
    try:
        # Fallback to alternative (lunardate)
        return alternative_calculation()
    except:
        # Last resort: approximation
        return approximate_calculation()
```

### Performance Optimization

1. **Lazy Loading**: Libraries loaded only when needed
2. **Caching**: Ephemeris data cached in memory
3. **Async Operations**: Non-blocking I/O for all calculations
4. **Batch Processing**: Support for batch date checking

### Type Safety

All functions include comprehensive type hints:
```python
async def calculate_bazi(
    self, birth_datetime_str: str, timezone_offset: int = 8
) -> dict[str, Any]:
    """Calculate complete BaZi with type safety."""
    ...
```

### Testing Strategy

**Coverage Targets**:
- Core calculations: >90%
- Integration tests: >80%
- Error handling: 100%

**Test Categories**:
- Unit tests for individual functions
- Integration tests for module interactions
- End-to-end tests for MCP server
- Edge case and boundary testing

---

## References

### Standards and Specifications

1. **Model Context Protocol (MCP)**
   - Protocol version: 2024-11-05
   - Specification: https://modelcontextprotocol.io

2. **Astronomical Standards**
   - JPL Planetary Ephemeris DE421
   - IAU (International Astronomical Union) standards

3. **Traditional References**
   - Chinese Almanac (通胜/黄历)
   - Four Pillars of Destiny (八字命理)
   - Wu Xing (Five Elements Theory)

### Academic Sources

The algorithms and data are based on established astronomical calculations and traditional Chinese calendar systems that have been used for centuries. The implementation combines:

- Modern astronomical precision (NASA ephemeris data)
- Traditional Chinese calendar rules
- Well-tested Python libraries for calendar conversions
- Cultural knowledge preserved in traditional almanacs

---

## Implementation Notes

### Accuracy vs. Performance

The server balances accuracy with performance:

- **High Precision**: Astronomical calculations use professional-grade ephemeris
- **Practical Approximations**: Traditional calendar rules use established approximations
- **Fallback Methods**: Graceful degradation when precise libraries unavailable

### Cultural Sensitivity

The implementation respects traditional Chinese culture:

- Uses authentic Chinese terminology alongside English translations
- Follows traditional calculation methods
- Preserves cultural context and significance
- Provides educational information about customs and meanings

### Extensibility

The modular design allows for:

- Adding new cultural traditions
- Extending to other Asian lunar calendars
- Incorporating additional astronomical features
- Supporting more festival databases

---

## Maintenance and Updates

### Ephemeris Data

The DE421 ephemeris file covers years 1900-2050. For dates outside this range:
- Update to newer ephemeris (DE430, DE440)
- Download from NASA JPL: https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/

### Library Dependencies

Regular updates required for:
- `lunardate`, `zhdate` - Lunar calendar libraries
- `skyfield`, `astropy` - Astronomy libraries
- `mcp` - Model Context Protocol implementation

### Festival Data

Festival information is maintained in `cultural_data/chinese.py` and can be updated to include:
- New festival entries
- Regional variations
- Modern celebrations
- Historical festivals

---

## Conclusion

The Lunar Calendar MCP Server combines traditional Chinese calendar wisdom with modern astronomical precision. By using established libraries, professional-grade astronomical data, and traditional calculation methods, it provides accurate and culturally authentic information for AI applications.

The implementation is designed to be:
- **Accurate**: Using professional astronomical data and traditional methods
- **Reliable**: Multiple fallback mechanisms ensure availability
- **Educational**: Preserving and sharing traditional cultural knowledge
- **Extensible**: Modular design supports future enhancements

For questions or contributions, please refer to the development guide and testing documentation.
