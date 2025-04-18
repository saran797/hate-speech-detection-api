import re

# List of banned hate keywords
HARD_HATE_KEYWORDS = [
    "nigger", "nigga", "faggot", "kike", "chink", "spic", "tranny", "retard",
    "wetback", "gook", "coon", "sandnigger", "towelhead", "beaner", "gyppo"
]

# Regex patterns to catch obfuscated slurs
HARD_HATE_PATTERNS = [
    r"\bn[i1!|][gq9]{2}[a@]\b",
    r"\bn[i1!|][gq9]{2}er\b",
    r"\bf[a@][gq9]{2}[o0t]?\b",
    r"\bch[i1]nk\b",
    r"\bk[i1]ke\b",
    r"\bsp[i1]c\b",
    r"\br[e3]t[a@]rd\b"
]

def is_hard_hate(text: str) -> bool:
    text = text.lower()
    for word in HARD_HATE_KEYWORDS:
        if word in text:
            return True
    for pattern in HARD_HATE_PATTERNS:
        if re.search(pattern, text):
            return True
    return False
