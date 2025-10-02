"""
Chinese cultural data and traditional calendar information.
"""

from typing import Dict, List, Any
from datetime import datetime


class ChineseData:
    """Chinese cultural and calendar data."""

    def __init__(self) -> None:
        """Initialize Chinese cultural data."""
        self.setup_traditional_data()

    def setup_traditional_data(self) -> None:
        """Set up traditional Chinese calendar data."""

        # Twenty-Eight Lunar Mansions (二十八宿)
        self.lunar_mansions = {
            # Eastern Azure Dragon (东方青龙)
            "角": {"name": "Jiao", "english": "Horn", "element": "Wood", "animal": "Dragon", "direction": "East"},
            "亢": {"name": "Kang", "english": "Neck", "element": "Wood", "animal": "Dragon", "direction": "East"},
            "氐": {"name": "Di", "english": "Root", "element": "Earth", "animal": "Raccoon", "direction": "East"},
            "房": {"name": "Fang", "english": "Room", "element": "Sun", "animal": "Rabbit", "direction": "East"},
            "心": {"name": "Xin", "english": "Heart", "element": "Moon", "animal": "Fox", "direction": "East"},
            "尾": {"name": "Wei", "english": "Tail", "element": "Fire", "animal": "Tiger", "direction": "East"},
            "箕": {"name": "Ji", "english": "Winnowing Basket", "element": "Water", "animal": "Leopard", "direction": "East"},

            # Northern Black Tortoise (北方玄武)
            "斗": {"name": "Dou", "english": "Dipper", "element": "Wood", "animal": "Unicorn", "direction": "North"},
            "牛": {"name": "Niu", "english": "Ox", "element": "Earth", "animal": "Ox", "direction": "North"},
            "女": {"name": "Nu", "english": "Girl", "element": "Earth", "animal": "Bat", "direction": "North"},
            "虛": {"name": "Xu", "english": "Emptiness", "element": "Sun", "animal": "Rat", "direction": "North"},
            "危": {"name": "Wei", "english": "Rooftop", "element": "Moon", "animal": "Swallow", "direction": "North"},
            "室": {"name": "Shi", "english": "Encampment", "element": "Fire", "animal": "Pig", "direction": "North"},
            "壁": {"name": "Bi", "english": "Wall", "element": "Water", "animal": "Porcupine", "direction": "North"},

            # Western White Tiger (西方白虎)
            "奎": {"name": "Kui", "english": "Legs", "element": "Wood", "animal": "Wolf", "direction": "West"},
            "婁": {"name": "Lou", "english": "Bond", "element": "Metal", "animal": "Dog", "direction": "West"},
            "胃": {"name": "Wei", "english": "Stomach", "element": "Earth", "animal": "Pheasant", "direction": "West"},
            "昴": {"name": "Mao", "english": "Hairy Head", "element": "Sun", "animal": "Cock", "direction": "West"},
            "畢": {"name": "Bi", "english": "Net", "element": "Moon", "animal": "Crow", "direction": "West"},
            "觜": {"name": "Zi", "english": "Turtle Beak", "element": "Fire", "animal": "Monkey", "direction": "West"},
            "參": {"name": "Shen", "english": "Three Stars", "element": "Water", "animal": "Ape", "direction": "West"},

            # Southern Vermilion Bird (南方朱雀)
            "井": {"name": "Jing", "english": "Well", "element": "Wood", "animal": "Tapir", "direction": "South"},
            "鬼": {"name": "Gui", "english": "Ghost", "element": "Metal", "animal": "Sheep", "direction": "South"},
            "柳": {"name": "Liu", "english": "Willow", "element": "Earth", "animal": "Deer", "direction": "South"},
            "星": {"name": "Xing", "english": "Star", "element": "Sun", "animal": "Horse", "direction": "South"},
            "張": {"name": "Zhang", "english": "Extended Net", "element": "Moon", "animal": "Deer", "direction": "South"},
            "翼": {"name": "Yi", "english": "Wings", "element": "Fire", "animal": "Snake", "direction": "South"},
            "軫": {"name": "Zhen", "english": "Chariot", "element": "Water", "animal": "Earthworm", "direction": "South"}
        }

        # Traditional activities and their auspiciousness by mansion
        self.mansion_activities = {
            "角": {
                "auspicious": ["weddings", "ceremonies", "construction", "moving", "planting"],
                "inauspicious": ["funerals", "medical procedures", "lawsuits"],
                "neutral": ["travel", "business meetings"]
            },
            "亢": {
                "auspicious": ["education", "learning", "teaching", "business opening"],
                "inauspicious": ["travel", "litigation", "medical procedures"],
                "neutral": ["routine work", "planning"]
            },
            "氐": {
                "auspicious": ["marriage", "planting", "building foundations"],
                "inauspicious": ["hunting", "cutting", "demolition"],
                "neutral": ["cooking", "crafting"]
            },
            "房": {
                "auspicious": ["ceremonies", "offerings", "worship", "meditation"],
                "inauspicious": ["moving", "burial", "major changes"],
                "neutral": ["reading", "studying"]
            },
            "心": {
                "auspicious": ["spiritual practices", "meditation", "healing"],
                "inauspicious": ["construction", "business", "heavy work"],
                "neutral": ["rest", "contemplation"]
            },
            "尾": {
                "auspicious": ["fishing", "hunting", "martial arts"],
                "inauspicious": ["marriage", "celebration", "formal ceremonies"],
                "neutral": ["exercise", "competition"]
            },
            "箕": {
                "auspicious": ["cleaning", "organizing", "demolition", "ending projects"],
                "inauspicious": ["weddings", "opening ceremonies", "new beginnings"],
                "neutral": ["maintenance", "repairs"]
            }
        }

        # Five Elements interactions
        self.five_elements = {
            "Wood": {
                "generates": "Fire",
                "destroys": "Earth",
                "generated_by": "Water",
                "destroyed_by": "Metal",
                "characteristics": ["growth", "expansion", "flexibility", "creativity"],
                "colors": ["green", "cyan"],
                "direction": "East",
                "season": "Spring",
                "emotions": ["kindness", "patience"]
            },
            "Fire": {
                "generates": "Earth",
                "destroys": "Metal",
                "generated_by": "Wood",
                "destroyed_by": "Water",
                "characteristics": ["energy", "passion", "transformation", "illumination"],
                "colors": ["red", "purple"],
                "direction": "South",
                "season": "Summer",
                "emotions": ["joy", "excitement"]
            },
            "Earth": {
                "generates": "Metal",
                "destroys": "Water",
                "generated_by": "Fire",
                "destroyed_by": "Wood",
                "characteristics": ["stability", "grounding", "nurturing", "support"],
                "colors": ["yellow", "brown"],
                "direction": "Center",
                "season": "Late Summer",
                "emotions": ["thoughtfulness", "care"]
            },
            "Metal": {
                "generates": "Water",
                "destroys": "Wood",
                "generated_by": "Earth",
                "destroyed_by": "Fire",
                "characteristics": ["precision", "clarity", "strength", "organization"],
                "colors": ["white", "silver", "gold"],
                "direction": "West",
                "season": "Autumn",
                "emotions": ["grief", "letting go"]
            },
            "Water": {
                "generates": "Wood",
                "destroys": "Fire",
                "generated_by": "Metal",
                "destroyed_by": "Earth",
                "characteristics": ["flow", "adaptability", "wisdom", "depth"],
                "colors": ["black", "blue"],
                "direction": "North",
                "season": "Winter",
                "emotions": ["fear", "will"]
            }
        }

        # Zodiac animal detailed information
        self.zodiac_animals_detailed = {
            "Rat": {
                "years": [1924, 1936, 1948, 1960, 1972, 1984, 1996, 2008, 2020, 2032],
                "element_cycle": ["Wood", "Fire", "Earth", "Metal", "Water"],
                "personality": ["intelligent", "adaptable", "charming", "ambitious"],
                "lucky_colors": ["blue", "gold", "green"],
                "lucky_numbers": [2, 3],
                "lucky_flowers": ["lily", "african violet"],
                "best_matches": ["Dragon", "Monkey", "Ox"],
                "worst_matches": ["Horse", "Goat"],
                "famous_people": ["William Shakespeare", "Mozart", "Truman Capote"],
                "career_suits": ["business", "politics", "literature", "research"]
            },
            "Ox": {
                "years": [1925, 1937, 1949, 1961, 1973, 1985, 1997, 2009, 2021, 2033],
                "element_cycle": ["Wood", "Fire", "Earth", "Metal", "Water"],
                "personality": ["reliable", "strong", "determined", "honest"],
                "lucky_colors": ["white", "yellow", "green"],
                "lucky_numbers": [1, 9],
                "lucky_flowers": ["tulip", "evergreen"],
                "best_matches": ["Snake", "Rooster", "Rat"],
                "worst_matches": ["Goat", "Horse"],
                "famous_people": ["Napoleon", "Van Gogh", "Walt Disney"],
                "career_suits": ["agriculture", "engineering", "medicine", "teaching"]
            },
            "Tiger": {
                "years": [1926, 1938, 1950, 1962, 1974, 1986, 1998, 2010, 2022, 2034],
                "element_cycle": ["Fire", "Earth", "Metal", "Water", "Wood"],
                "personality": ["brave", "competitive", "confident", "charismatic"],
                "lucky_colors": ["orange", "gray", "white"],
                "lucky_numbers": [1, 3, 4],
                "lucky_flowers": ["cineraria", "anthurium"],
                "best_matches": ["Horse", "Dog", "Pig"],
                "worst_matches": ["Monkey", "Snake"],
                "famous_people": ["Marco Polo", "Beethoven", "Queen Elizabeth II"],
                "career_suits": ["leadership", "military", "adventure", "entertainment"]
            },
            "Rabbit": {
                "years": [1927, 1939, 1951, 1963, 1975, 1987, 1999, 2011, 2023, 2035],
                "element_cycle": ["Fire", "Earth", "Metal", "Water", "Wood"],
                "personality": ["gentle", "quiet", "elegant", "responsible"],
                "lucky_colors": ["pink", "purple", "blue"],
                "lucky_numbers": [3, 4, 9],
                "lucky_flowers": ["snapdragon", "jasmine"],
                "best_matches": ["Goat", "Pig", "Dog"],
                "worst_matches": ["Rooster", "Dragon"],
                "famous_people": ["Einstein", "Confucius", "Moon"],
                "career_suits": ["arts", "literature", "medicine", "fashion"]
            },
            "Dragon": {
                "years": [1928, 1940, 1952, 1964, 1976, 1988, 2000, 2012, 2024, 2036],
                "element_cycle": ["Earth", "Metal", "Water", "Wood", "Fire"],
                "personality": ["energetic", "intelligent", "gifted", "lucky"],
                "lucky_colors": ["gold", "silver", "gray"],
                "lucky_numbers": [1, 6, 7],
                "lucky_flowers": ["bleeding heart", "larkspur"],
                "best_matches": ["Rat", "Monkey", "Rooster"],
                "worst_matches": ["Dog", "Rabbit"],
                "famous_people": ["Bruce Lee", "John Lennon", "Salvador Dali"],
                "career_suits": ["leadership", "innovation", "arts", "entrepreneurship"]
            },
            "Snake": {
                "years": [1929, 1941, 1953, 1965, 1977, 1989, 2001, 2013, 2025, 2037],
                "element_cycle": ["Earth", "Metal", "Water", "Wood", "Fire"],
                "personality": ["wise", "elegant", "intuitive", "mysterious"],
                "lucky_colors": ["black", "red", "yellow"],
                "lucky_numbers": [2, 8, 9],
                "lucky_flowers": ["orchid", "cactus"],
                "best_matches": ["Ox", "Rooster", "Monkey"],
                "worst_matches": ["Pig", "Tiger"],
                "famous_people": ["Gandhi", "JFK", "Abraham Lincoln"],
                "career_suits": ["philosophy", "psychology", "investigation", "finance"]
            },
            "Horse": {
                "years": [1930, 1942, 1954, 1966, 1978, 1990, 2002, 2014, 2026, 2038],
                "element_cycle": ["Metal", "Water", "Wood", "Fire", "Earth"],
                "personality": ["animated", "active", "energetic", "independent"],
                "lucky_colors": ["yellow", "green", "purple"],
                "lucky_numbers": [2, 3, 7],
                "lucky_flowers": ["calla lily", "jasmine"],
                "best_matches": ["Tiger", "Dog", "Goat"],
                "worst_matches": ["Rat", "Ox"],
                "famous_people": ["Rembrandt", "Chopin", "Neil Armstrong"],
                "career_suits": ["sports", "travel", "sales", "communication"]
            },
            "Goat": {
                "years": [1931, 1943, 1955, 1967, 1979, 1991, 2003, 2015, 2027, 2039],
                "element_cycle": ["Metal", "Water", "Wood", "Fire", "Earth"],
                "personality": ["calm", "gentle", "sympathetic", "artistic"],
                "lucky_colors": ["green", "red", "purple"],
                "lucky_numbers": [3, 9, 4],
                "lucky_flowers": ["carnation", "primrose"],
                "best_matches": ["Rabbit", "Pig", "Horse"],
                "worst_matches": ["Ox", "Rat"],
                "famous_people": ["Michelangelo", "Mark Twain", "Steve Jobs"],
                "career_suits": ["arts", "literature", "music", "design"]
            },
            "Monkey": {
                "years": [1932, 1944, 1956, 1968, 1980, 1992, 2004, 2016, 2028, 2040],
                "element_cycle": ["Water", "Wood", "Fire", "Earth", "Metal"],
                "personality": ["sharp", "smart", "curious", "mischievous"],
                "lucky_colors": ["white", "gold", "blue"],
                "lucky_numbers": [1, 8, 7],
                "lucky_flowers": ["chrysanthemum", "crape-myrtle"],
                "best_matches": ["Rat", "Dragon", "Snake"],
                "worst_matches": ["Tiger", "Pig"],
                "famous_people": ["Leonardo da Vinci", "Charles Dickens", "Tom Hanks"],
                "career_suits": ["science", "technology", "entertainment", "business"]
            },
            "Rooster": {
                "years": [1933, 1945, 1957, 1969, 1981, 1993, 2005, 2017, 2029, 2041],
                "element_cycle": ["Water", "Wood", "Fire", "Earth", "Metal"],
                "personality": ["observant", "hardworking", "courageous", "talented"],
                "lucky_colors": ["gold", "brown", "yellow"],
                "lucky_numbers": [5, 7, 8],
                "lucky_flowers": ["gladiola", "impatiens"],
                "best_matches": ["Ox", "Snake", "Dragon"],
                "worst_matches": ["Rabbit", "Dog"],
                "famous_people": ["Confucius", "Rudyard Kipling", "Serena Williams"],
                "career_suits": ["public relations", "journalism", "military", "restaurant"]
            },
            "Dog": {
                "years": [1934, 1946, 1958, 1970, 1982, 1994, 2006, 2018, 2030, 2042],
                "element_cycle": ["Wood", "Fire", "Earth", "Metal", "Water"],
                "personality": ["lovely", "honest", "responsible", "reliable"],
                "lucky_colors": ["green", "red", "purple"],
                "lucky_numbers": [3, 4, 9],
                "lucky_flowers": ["rose", "cymbidium orchids"],
                "best_matches": ["Tiger", "Horse", "Rabbit"],
                "worst_matches": ["Dragon", "Rooster"],
                "famous_people": ["Winston Churchill", "Mother Teresa", "Michael Jackson"],
                "career_suits": ["law", "medicine", "education", "social work"]
            },
            "Pig": {
                "years": [1935, 1947, 1959, 1971, 1983, 1995, 2007, 2019, 2031, 2043],
                "element_cycle": ["Wood", "Fire", "Earth", "Metal", "Water"],
                "personality": ["honest", "generous", "reliable", "optimistic"],
                "lucky_colors": ["yellow", "gray", "brown"],
                "lucky_numbers": [2, 5, 8],
                "lucky_flowers": ["hydrangea", "pitcher plant"],
                "best_matches": ["Rabbit", "Goat", "Tiger"],
                "worst_matches": ["Snake", "Monkey"],
                "famous_people": ["Ernest Hemingway", "Ronald Reagan", "Arnold Schwarzenegger"],
                "career_suits": ["retail", "hospitality", "entertainment", "healthcare"]
            }
        }

        # Traditional Chinese calendar terms
        self.calendar_terms = {
            "jieqi": {  # 24 Solar Terms
                "立春": {"name": "Lichun", "english": "Beginning of Spring", "date": "Feb 4-5"},
                "雨水": {"name": "Yushui", "english": "Rain Water", "date": "Feb 19-20"},
                "惊蛰": {"name": "Jingzhe", "english": "Awakening of Insects", "date": "Mar 5-6"},
                "春分": {"name": "Chunfen", "english": "Spring Equinox", "date": "Mar 20-21"},
                "清明": {"name": "Qingming", "english": "Pure Brightness", "date": "Apr 4-5"},
                "谷雨": {"name": "Guyu", "english": "Grain Rain", "date": "Apr 19-20"},
                "立夏": {"name": "Lixia", "english": "Beginning of Summer", "date": "May 5-6"},
                "小满": {"name": "Xiaoman", "english": "Lesser Fullness", "date": "May 20-21"},
                "芒种": {"name": "Mangzhong", "english": "Grain in Ear", "date": "Jun 5-6"},
                "夏至": {"name": "Xiazhi", "english": "Summer Solstice", "date": "Jun 21-22"},
                "小暑": {"name": "Xiaoshu", "english": "Lesser Heat", "date": "Jul 6-7"},
                "大暑": {"name": "Dashu", "english": "Greater Heat", "date": "Jul 22-23"},
                "立秋": {"name": "Liqiu", "english": "Beginning of Autumn", "date": "Aug 7-8"},
                "处暑": {"name": "Chushu", "english": "Stopping the Heat", "date": "Aug 22-23"},
                "白露": {"name": "Bailu", "english": "White Dew", "date": "Sep 7-8"},
                "秋分": {"name": "Qiufen", "english": "Autumn Equinox", "date": "Sep 22-23"},
                "寒露": {"name": "Hanlu", "english": "Cold Dew", "date": "Oct 8-9"},
                "霜降": {"name": "Shuangjiang", "english": "Frost's Descent", "date": "Oct 23-24"},
                "立冬": {"name": "Lidong", "english": "Beginning of Winter", "date": "Nov 7-8"},
                "小雪": {"name": "Xiaoxue", "english": "Lesser Snow", "date": "Nov 22-23"},
                "大雪": {"name": "Daxue", "english": "Greater Snow", "date": "Dec 6-7"},
                "冬至": {"name": "Dongzhi", "english": "Winter Solstice", "date": "Dec 21-22"},
                "小寒": {"name": "Xiaohan", "english": "Lesser Cold", "date": "Jan 5-6"},
                "大寒": {"name": "Dahan", "english": "Greater Cold", "date": "Jan 20-21"}
            }
        }

        # Traditional taboos and customs
        self.cultural_practices = {
            "spring_festival": {
                "preparations": [
                    "Clean house thoroughly before New Year",
                    "Prepare red decorations and couplets",
                    "Buy new clothes (preferably red)",
                    "Stock up on food for family reunion"
                ],
                "taboos": [
                    "No sweeping on New Year's Day (sweeps away luck)",
                    "No breaking dishes or glasses",
                    "No arguing or crying",
                    "No wearing white or black clothes",
                    "No cutting hair during first month"
                ],
                "activities": [
                    "Family reunion dinner on New Year's Eve",
                    "Give red envelopes (hongbao) to children",
                    "Visit temples and pray for good fortune",
                    "Watch lion and dragon dances",
                    "Set off firecrackers to scare away evil spirits"
                ]
            },
            "general_practices": {
                "daily_taboos": [
                    "Avoid number 4 (sounds like death)",
                    "Don't give clocks as gifts (symbolizes death)",
                    "Don't give white flowers (for funerals)",
                    "Don't point with one finger",
                    "Don't stick chopsticks upright in rice"
                ],
                "lucky_practices": [
                    "Use number 8 (sounds like prosperity)",
                    "Face favorable directions when sleeping",
                    "Keep plants in eastern parts of home",
                    "Use feng shui principles in home arrangement",
                    "Wear jade for protection and luck"
                ]
            }
        }

    def get_mansion_for_date(self, date_obj: datetime) -> Dict[str, Any]:
        """Get lunar mansion for a specific date."""
        # Calculate days since reference date
        reference_date = datetime(2000, 1, 1)
        days_diff = (date_obj - reference_date).days
        mansion_index = days_diff % 28

        mansion_list = list(self.lunar_mansions.keys())
        mansion_char = mansion_list[mansion_index]

        return {
            "mansion_character": mansion_char,
            "mansion_info": self.lunar_mansions[mansion_char],
            "activities": self.mansion_activities.get(mansion_char, {}),
            "day_index": mansion_index + 1
        }

    def get_element_for_date(self, date_obj: datetime) -> Dict[str, Any]:
        """Get five element for a specific date."""
        # Simplified calculation based on year and day
        year_element_index = (date_obj.year - 1900) % 5
        day_element_index = date_obj.timetuple().tm_yday % 5

        elements = list(self.five_elements.keys())
        year_element = elements[year_element_index]
        day_element = elements[day_element_index]

        return {
            "year_element": year_element,
            "day_element": day_element,
            "year_element_info": self.five_elements[year_element],
            "day_element_info": self.five_elements[day_element],
            "interaction": self._get_element_interaction(year_element, day_element)
        }

    def _get_element_interaction(self, element1: str, element2: str) -> Dict[str, str]:
        """Get interaction between two elements."""
        element1_info = self.five_elements[element1]

        if element2 == element1_info["generates"]:
            return {"type": "generative", "description": f"{element1} generates {element2}"}
        elif element2 == element1_info["destroys"]:
            return {"type": "destructive", "description": f"{element1} destroys {element2}"}
        elif element2 == element1_info["generated_by"]:
            return {"type": "supportive", "description": f"{element1} is generated by {element2}"}
        elif element2 == element1_info["destroyed_by"]:
            return {"type": "weakening", "description": f"{element1} is destroyed by {element2}"}
        else:
            return {"type": "neutral", "description": f"{element1} and {element2} are neutral"}

    def get_zodiac_details(self, animal: str) -> Dict[str, Any]:
        """Get detailed zodiac animal information."""
        return self.zodiac_animals_detailed.get(animal, {})

    def get_cultural_advice(self, festival: str, activity: str) -> List[str]:
        """Get cultural advice for specific festivals and activities."""
        if festival == "spring_festival":
            practices = self.cultural_practices["spring_festival"]
            if activity in ["preparation", "planning"]:
                return practices["preparations"]
            elif activity in ["celebration", "ceremony"]:
                return practices["activities"]
            else:
                return practices["taboos"]
        else:
            return self.cultural_practices["general_practices"]["lucky_practices"]