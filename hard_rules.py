import re

# Optional: Load from external file
# def load_keywords(filepath: str):
#     with open(filepath, "r", encoding="utf-8") as f:
#         return [line.strip().lower() for line in f if line.strip()]

# HARD_HATE_KEYWORDS = load_keywords("hate_keywords.txt")

HARD_HATE_KEYWORDS = [
    "nigger", "nigga", "faggot", "fag", "dyke", "kike", "chink", "gook", "spic",
    "wetback", "coon", "towelhead", "raghead", "camel jockey", "sandnigger",
    "tranny", "retard", "cripple", "mongoloid", "gyppo", "beaner", "zipperhead",
    "twink", "hebe", "queer", "slant", "shemale", "redskin", "hajji", "pakki",
    "ape", "animal", "white trash", "jungle bunny", "paki", "negro", "ho", "whore",
    "cunt", "bitch", "skank", "slut", "motherfucker", "bastard", "homo", "lesbo",
    "pedo", "molester", "rapist", "terrorist", "incel", "simp", "dumbass", "fucktard",
    "dumbfuck", "asswipe", "asshole", "shithead", "pussy", "cock", "dickhead",
    "twat", "cumdumpster", "cocksucker", "clit", "nutsack", "fudgepacker", "numbnuts",
    "sex offender", "abuser", "groomer", "cracker", "honky", "hillbilly", "redneck",
    "snowflake", "femboy", "crossdresser", "beta male", "alpha male", "mutt", "subhuman"
]


def is_hard_hate(text: str) -> bool:
    """Returns True if any hardcoded slurs or patterns are found."""
    text = text.lower()
    for word in HARD_HATE_KEYWORDS:
        if word in text:
            return True
    return False
