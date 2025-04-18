import re

# Define contextual rules
CONTEXT_RULES = {
    "hate_speech": [
        r"\bgo back to your country\b",
        r"\byou people\b",
        r"\bkill all\b",
        r"\bdumb (muslims|hindus|christians|jews)\b",
        r"\brapists?\b",
        r"\bflooding our country\b",
        r"\b(black|white|asian|jewish) scum\b",
        r"\bthey should be wiped out\b",
        r"\bget out of here\b",
    ],
    "non_offensive": [
        r"\bi dislike\b",
        r"\bi don’t agree\b",
        r"\bthis is wrong\b",
        r"\byou're mistaken\b",
        r"\bthis doesn't make sense\b",
    ],
    "sarcasm": [
        r"\boh sure\b",
        r"\byeah right\b",
        r"\bvery smart\b",
        r"\bwhat a genius\b",
        r"\bgreat job\b",
    ],
    "exaggeration": [
        r"\bliterally dying\b",
        r"\bcan’t even\b",
        r"\bworst thing ever\b",
        r"\blosing my mind\b",
    ],
    "violent": [
        r"\bshould be killed\b",
        r"\bi’ll stab you\b",
        r"\bburn them\b",
        r"\bshoot them all\b",
        r"\bi’ll murder\b",
    ],
    "positive": [
        r"\bi love\b",
        r"\bso beautiful\b",
        r"\bwonderful\b",
        r"\bso peaceful\b",
        r"\bamazing people\b",
    ]
}

def match_context(sentence):
    matched_categories = []

    for category, patterns in CONTEXT_RULES.items():
        for pattern in patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                matched_categories.append(category)
                break  # Avoid double counting same category

    return matched_categories
