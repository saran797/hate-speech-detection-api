import re

CONTEXT_RULES = {
    "hate_speech": [
        r"\b(kill|slay|destroy|wipe out|eliminate)\s+(everyone|[a-zA-Z]+)\b",
        r"\b(people|humans|society) like (us|you|them) should die\b",
        r"\b(i’ll|i want to|we should) [a-zA-Z]+ them\b",
        r"\b(you|those) [a-zA-Z]+ are scum\b",
        r"\b(terrorists|scum|cockroaches) should be wiped out\b",
        r"\bgo back to (your country|where you came from)\b",
        r"\b(white|black|asian) supremacy\b",
        r"\b(immigrants?|refugees?) are ruining our (culture|country|society)\b",
        r"\b(destroy|eliminate) the (left|right) wing\b",
        r"\bwe are the chosen (race|people)\b",
        r"\bno place for (these people|them)\b",
        r"\bwe need to rid the world of (them|those)\b",
        r"\b(exterminate|genocide|eradicate) (them|these people)\b",
        r"\b(subhuman|animals|vermin) deserve to die\b",
        r"\bget rid of (them|those people|[a-zA-Z]+) for good\b",
        r"\bshut them down (forever|permanently)\b",
        r"\b(exterminate|massacre|slaughter) them\b",
        r"\bthey don’t belong here\b",
        r"\bthey’re better off dead\b",
        r"\b(replace|eliminate) them\b",
        r"\bwe must separate ourselves from (them|others)\b",
        r"\bthey don’t deserve rights\b",
    ],
    "non_offensive": [
        r"\bI don't mind\b", r"\bnot a big deal\b", r"\bno harm in it\b", r"\bnot bothered\b",
        r"\bI’m fine with it\b", r"\bno offense\b", r"\bI’m okay\b", r"\bdon’t care\b", r"\bdo whatever\b"
    ],
    "sarcasm": [
        r"\boh, absolutely\b", r"\byeah, sure\b", r"\byeah right\b", r"\bso clever\b", r"\bgreat idea\b",
        r"\boh, that’s brilliant\b", r"\bcan’t believe it\b", r"\bso funny\b", r"\bdefinitely not fake\b", r"\bwho would’ve guessed\b"
    ],
    "exaggeration": [
        r"\bI am literally dying\b", r"\bthis is the worst day ever\b", r"\bI’m losing my mind\b",
        r"\bI can’t take this anymore\b", r"\bthis is beyond belief\b", r"\bI’m dead\b", r"\bthis is unbearable\b"
    ],
    "violent": [
        r"\b(beat|stab|shoot|kill|punch) [a-zA-Z]+\b", r"\battack them\b", r"\bend them\b", r"\bblow them up\b",
        r"\bstab them in the back\b", r"\bshoot them on sight\b", r"\bviolence is the answer\b", r"\bI’m going to destroy you\b"
    ],
    "positive": [
        r"\bI love this\b", r"\bthis is awesome\b", r"\bso kind\b", r"\bthat’s great\b", r"\bvery inspiring\b",
        r"\bso thoughtful\b", r"\bthis is incredible\b", r"\bwonderful work\b", r"\bso amazing\b"
    ],
    "political": [
        r"\bvote\b", r"\belection\b", r"\bmake [a-zA-Z]+ great again\b", r"\b(Republican|Democrat) party\b", 
        r"\bleft-wing\b", r"\bright-wing\b", r"\bwe need a new leader\b", r"\bpolitical revolution\b", 
        r"\bchange the system\b", r"\b(communist|capitalist) revolution\b", r"\bpower to the people\b"
    ],
    "manipulative": [
        r"\btrust me\b", r"\bonly I know the truth\b", r"\bthis is for your own good\b", r"\bdon't question me\b",
        r"\bjust follow me\b", r"\byou’ll regret it\b", r"\bdo what I say\b", r"\bI'm doing this for your own benefit\b"
    ],
    "humor": [
        r"\bjust kidding\b", r"\bhaha\b", r"\bhilarious\b", r"\bso funny\b", r"\bI’m just joking\b", r"\bLOL\b",
        r"\bcan’t take this seriously\b", r"\bwhat a joke\b", r"\bnot really\b", r"\bjust messing around\b"
    ],
    "offensive_remarks": [
        r"\bshut your mouth\b", r"\bshut up\b", r"\bget a life\b", r"\bgo to hell\b", r"\bI don’t care about you\b",
        r"\byou’re a fool\b", r"\byou are stupid\b", r"\bno one cares\b", r"\byou mean nothing\b", r"\bI don’t like you\b"
    ],
    "aggressive_remarks": [
        r"\bback off\b", r"\bdon’t mess with me\b", r"\bleave me alone\b", r"\bstay away from me\b", r"\bget lost\b",
        r"\bI’ll make you regret this\b", r"\bwatch out\b", r"\bI’m not afraid of you\b", r"\bI’ll destroy you\b"
    ],
    "dehumanization": [
        r"\b(animals|vermin|scum|cockroaches)\b", r"\bsubhuman\b", r"\b(lesser|inferior) beings\b", r"\bthey’re not people\b",
        r"\bno better than animals\b", r"\bwe must rid the world of these people\b", r"\bthey don’t deserve rights\b"
    ],
    "threatening": [
        r"\bI will find you\b", r"\bI’m going to make you pay\b", r"\byou will regret this\b", r"\bthis will not go unpunished\b",
        r"\bI’ll hurt you\b", r"\byou’re dead\b", r"\bwatch your back\b", r"\bI’m coming for you\b"
    ],
    "exclusionary": [
        r"\b(we|them|us) vs (them|others)\b", r"\bthey don’t belong\b", r"\bnot one of us\b", r"\bout of our group\b",
        r"\bseparate them\b", r"\bthey don’t deserve to be here\b", r"\bwe are better than them\b"
    ]
}

def match_context(sentence):
    matched_categories = []
    for category, patterns in CONTEXT_RULES.items():
        for pattern in patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                matched_categories.append(category)
                break
    return matched_categories

def contextual_vote(sentence):
    matched_categories = match_context(sentence)

    if "hate_speech" in matched_categories or "violent" in matched_categories or "dehumanization" in matched_categories:
        return "hate_speech"
    
    if "sarcasm" in matched_categories or "exaggeration" in matched_categories:
        return "not_hate_speech"
    
    if "non_offensive" in matched_categories or "positive" in matched_categories:
        return "not_hate_speech"

    if "aggressive_remarks" in matched_categories or "offensive_remarks" in matched_categories:
        return "offensive_speech"

    if "manipulative" in matched_categories or "humor" in matched_categories:
        return "not_hate_speech"

    if "threatening" in matched_categories or "exclusionary" in matched_categories:
        return "hate_speech"

    return "not_hate_speech"
