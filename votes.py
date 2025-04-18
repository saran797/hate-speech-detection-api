from textblob import TextBlob
from context import match_context
from profanity_list import BAD_WORDS

def context_vote(sentence):
    matches = match_context(sentence)

    if any(category in matches for category in ["hate_speech", "violent"]):
        return "hate_speech"
    elif any(category in matches for category in ["exaggeration", "sarcasm", "non_offensive", "positive"]):
        return "not_hate_speech"
    
    # Default to neutral
    return "not_hate_speech"

def textblob_vote(sentence):
    blob = TextBlob(sentence)
    polarity = blob.sentiment.polarity
    return "hate_speech" if polarity < -0.3 else "not_hate_speech"

def subjectivity_vote(sentence):
    blob = TextBlob(sentence)
    subjectivity = blob.sentiment.subjectivity
    polarity = blob.sentiment.polarity
    return "hate_speech" if subjectivity > 0.6 and polarity < -0.2 else "not_hate_speech"

def profanity_vote(sentence):
    words = sentence.lower().split()
    return "hate_speech" if any(word in BAD_WORDS for word in words) else "not_hate_speech"

def intensity_vote(sentence):
    all_caps = sentence.isupper()
    too_many_exclaims = sentence.count("!") > 2
    too_much_censoring = sentence.count("*") > 3
    return "hate_speech" if all_caps or too_many_exclaims or too_much_censoring else "not_hate_speech"
