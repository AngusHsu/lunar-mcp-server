# MCP Tools Reference

Complete reference for all 18 MCP tools across 5 categories.

## Auspicious Date Tools (4 tools)

### `check_auspicious_date`

Check if a date is favorable for specific activities.

**Parameters:**
- `date` (string): Date in YYYY-MM-DD format
- `activity` (string): Activity type (e.g., wedding, business_opening, travel)
- `culture` (string, optional): Cultural tradition (default: "chinese")

**Response:**
```json
{
  "date": "2024-02-14",
  "lunar_date": "2024-1-5",
  "auspicious_level": "very_good",
  "score": 8,
  "good_for": ["wedding", "business_opening", "travel"],
  "avoid": ["funeral", "major_surgery"],
  "lucky_hours": ["9:00-11:00", "13:00-15:00"],
  "zodiac_day": "dragon",
  "five_elements": "wood",
  "recommendations": "Excellent day for new beginnings"
}
```

### `find_good_dates`

Find optimal dates within a date range for specific activities.

**Parameters:**
- `start_date` (string): Start date in YYYY-MM-DD format
- `end_date` (string): End date in YYYY-MM-DD format
- `activity` (string): Activity type
- `culture` (string, optional): Cultural tradition (default: "chinese")
- `limit` (integer, optional): Maximum number of dates to return (default: 10)

**Response:**
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "activity": "wedding",
  "good_dates": [
    {
      "date": "2024-01-15",
      "level": "very_good",
      "score": 9,
      "zodiac_day": "dragon",
      "lucky_hours": ["9:00-11:00"],
      "moon_phase": "Full Moon"
    }
  ],
  "total_found": 5,
  "best_date": {...}
}
```

### `get_daily_fortune`

Get comprehensive daily fortune and luck information.

**Parameters:**
- `date` (string): Date in YYYY-MM-DD format
- `culture` (string, optional): Cultural tradition (default: "chinese")

**Response:**
```json
{
  "date": "2024-01-01",
  "fortune_level": "good",
  "lucky_colors": ["red", "gold"],
  "lucky_numbers": [8, 18],
  "lucky_directions": ["East", "Southeast"],
  "zodiac_day": "rat",
  "five_elements": "wood",
  "advice": "Good day for new beginnings..."
}
```

### `check_zodiac_compatibility`

Check compatibility between two dates based on zodiac systems.

**Parameters:**
- `date1` (string): First date in YYYY-MM-DD format
- `date2` (string): Second date in YYYY-MM-DD format
- `culture` (string, optional): Cultural tradition (default: "chinese")

**Response:**
```json
{
  "date1": "1990-01-01",
  "date2": "1992-01-01",
  "compatibility_level": "excellent",
  "score": 9,
  "zodiac1": "Horse",
  "zodiac2": "Monkey",
  "element_compatibility": "harmonious",
  "recommendations": "Very compatible pair..."
}
```

## Festival Tools (4 tools)

### `get_lunar_festivals`

Get festivals occurring on a specific date.

**Parameters:**
- `date` (string): Date in YYYY-MM-DD format
- `culture` (string, optional): Cultural tradition (default: "chinese")

**Response:**
```json
{
  "date": "2024-02-10",
  "festivals": [
    {
      "name": "Spring Festival (Chinese New Year)",
      "significance": "Beginning of lunar new year",
      "traditions": ["family reunion", "fireworks"],
      "foods": ["dumplings", "fish"],
      "is_major": true
    }
  ],
  "festival_count": 1
}
```

### `get_next_festival`

Find the next upcoming festival after a given date.

**Parameters:**
- `date` (string): Starting date in YYYY-MM-DD format
- `culture` (string, optional): Cultural tradition (default: "chinese")

**Response:**
```json
{
  "search_date": "2024-01-01",
  "next_festival_date": "2024-02-10",
  "days_until": 40,
  "festival": {
    "name": "Spring Festival",
    "significance": "...",
    "traditions": [...]
  }
}
```

### `get_festival_details`

Get detailed information about a specific festival.

**Parameters:**
- `festival_name` (string): Name of the festival
- `culture` (string, optional): Cultural tradition (default: "chinese")

**Response:**
```json
{
  "festival_id": "spring_festival",
  "name": "Spring Festival (Chinese New Year)",
  "significance": "Beginning of lunar new year",
  "duration": 15,
  "traditions": ["family reunion", "fireworks"],
  "foods": ["dumplings", "fish"],
  "lucky_activities": ["visiting relatives"],
  "taboos": ["sweeping on first day"],
  "preparation_guide": {...}
}
```

### `get_annual_festivals`

Get all festivals for a specific year.

**Parameters:**
- `year` (integer): Year (e.g., 2024)
- `culture` (string, optional): Cultural tradition (default: "chinese")

**Response:**
```json
{
  "year": 2024,
  "culture": "chinese",
  "total_festivals": 8,
  "major_festivals": ["spring_festival", "mid_autumn"],
  "calendar": {
    "1": [...],
    "2": [...],
    ...
  }
}
```

## Moon Phase Tools (4 tools)

### `get_moon_phase`

Get moon phase information for a specific date and location.

**Parameters:**
- `date` (string): Date in YYYY-MM-DD format
- `location` (string, optional): Coordinates "lat,lon" (default: "0,0")

**Response:**
```json
{
  "date": "2024-01-01",
  "phase_name": "Full Moon",
  "illumination": 0.98,
  "lunar_day": 15,
  "influence": {
    "good_for": ["celebrations", "completion"],
    "avoid": ["starting new projects"],
    "luck_level": "very good"
  }
}
```

### `get_moon_calendar`

Get monthly calendar with moon phases.

**Parameters:**
- `month` (integer): Month (1-12)
- `year` (integer): Year
- `location` (string, optional): Coordinates (default: "0,0")

**Response:**
```json
{
  "month": 1,
  "year": 2024,
  "calendar": [
    {
      "date": "2024-01-01",
      "phase_name": "Waning Crescent",
      "illumination": 0.15,
      "lunar_day": 20
    },
    ...
  ]
}
```

### `get_moon_influence`

Get how moon phase affects specific activities.

**Parameters:**
- `date` (string): Date in YYYY-MM-DD format
- `activity` (string): Activity type

**Response:**
```json
{
  "date": "2024-01-01",
  "activity": "planting",
  "moon_phase": "New Moon",
  "influence": "favorable",
  "recommendation": "Good time for planting seeds..."
}
```

### `predict_moon_phases`

Predict moon phases within a date range.

**Parameters:**
- `start_date` (string): Start date in YYYY-MM-DD format
- `end_date` (string): End date in YYYY-MM-DD format

**Response:**
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "phases": [
    {
      "date": "2024-01-11",
      "phase": "New Moon",
      "illumination": 0.0
    },
    {
      "date": "2024-01-25",
      "phase": "Full Moon",
      "illumination": 1.0
    }
  ]
}
```

## Calendar Conversion Tools (3 tools)

### `solar_to_lunar`

Convert Gregorian (solar) date to Chinese lunar date.

**Parameters:**
- `solar_date` (string): Solar date in YYYY-MM-DD format
- `culture` (string, optional): Cultural tradition (default: "chinese")

**Response:**
```json
{
  "solar_date": "2024-01-01",
  "lunar_year": 2023,
  "lunar_month": 11,
  "lunar_day": 20,
  "zodiac_info": {
    "animal": "Rabbit",
    "element": "Water",
    "yin_yang": "Yin"
  }
}
```

### `lunar_to_solar`

Convert Chinese lunar date to Gregorian (solar) date.

**Parameters:**
- `lunar_date` (string): Lunar date in YYYY-MM-DD format
- `culture` (string, optional): Cultural tradition (default: "chinese")

**Response:**
```json
{
  "lunar_date": "2024-01-01",
  "solar_date": "2024-02-10",
  "festival": "Spring Festival",
  "zodiac_info": {...}
}
```

### `get_zodiac_info`

Get detailed Chinese zodiac information for a date.

**Parameters:**
- `date` (string): Date in YYYY-MM-DD format
- `culture` (string, optional): Cultural tradition (default: "chinese")

**Response:**
```json
{
  "date": "1990-01-01",
  "zodiac": {
    "animal": "Horse",
    "element": "Earth",
    "yin_yang": "Yang",
    "traits": {
      "personality": "energetic, independent",
      "strengths": ["charismatic", "confident"],
      "weaknesses": ["impatient", "stubborn"]
    },
    "compatibility": {
      "best": ["Tiger", "Dog", "Goat"],
      "challenging": ["Rat", "Ox"]
    }
  }
}
```

## Advanced Tools (3 tools)

### `batch_check_dates`

Check multiple dates at once for efficiency.

**Parameters:**
- `dates` (array): List of dates in YYYY-MM-DD format (max 30)
- `activity` (string): Activity type
- `culture` (string, optional): Cultural tradition (default: "chinese")

**Response:**
```json
{
  "total_checked": 5,
  "results": [
    {
      "date": "2024-01-01",
      "score": 7,
      "level": "good",
      "details": {...}
    },
    ...
  ],
  "best_date": "2024-01-15",
  "worst_date": "2024-01-03"
}
```

### `compare_dates`

Compare multiple dates side-by-side.

**Parameters:**
- `dates` (array): List of dates to compare (max 10)
- `activity` (string, optional): Activity for context
- `culture` (string, optional): Cultural tradition (default: "chinese")

**Response:**
```json
{
  "comparison": {
    "2024-01-01": {
      "auspicious_level": "good",
      "score": 7,
      "moon_phase": "New Moon",
      "zodiac": {...},
      "festivals": []
    },
    "2024-01-15": {...}
  },
  "recommendation": "2024-01-15",
  "activity": "wedding"
}
```

### `get_lucky_hours`

Get auspicious hours within a specific day (12 Chinese time periods).

**Parameters:**
- `date` (string): Date in YYYY-MM-DD format
- `activity` (string, optional): Activity for context
- `culture` (string, optional): Cultural tradition (default: "chinese")

**Response:**
```json
{
  "date": "2024-01-01",
  "activity": "signing_contract",
  "lucky_hours": [
    {
      "time_range": "07:00-09:00",
      "period": "Chen (辰)",
      "zodiac_animal": "Dragon",
      "score": 9,
      "level": "very_good",
      "suitable_for": ["business", "signing contracts"]
    },
    ...
  ],
  "best_hours": [...]
}
```

## Error Responses

All tools return error responses in this format:

```json
{
  "error": "Error message describing what went wrong"
}
```

Common errors:
- Invalid date format
- Missing required parameters
- Invalid cultural tradition
- Date out of range

## See Also

- [Usage Examples](./usage-examples.md) - Practical examples
- [Cultural Traditions](./cultural-traditions.md) - Understanding the system
- [Development Guide](./development.md) - API development
