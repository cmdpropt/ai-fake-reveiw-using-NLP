import re
from collections import Counter

PROMOTIONAL_WORDS = {"amazing", "best", "must buy", "perfect", "cheap", "click", "earn", "link", "scam"}

def calculate_fraud_score(text):
    """
    Rule-based behavioral fraud detection.
    Returns a score from 0-100 and a list of flags triggered.
    """
    if not isinstance(text, str):
        return 0, []
        
    score = 0
    flags = []
    
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    word_count = len(words)
    
    # Rule 1: Length check (Very short or very long)
    if word_count < 5:
        score += 30
        flags.append("Extremely short review length (< 5 words).")
    elif word_count > 200:
        score += 20
        flags.append("Excessively long review length (> 200 words).")
        
    # Rule 2: Excessive exclamation marks
    exclamation_count = text.count('!')
    if exclamation_count > 3:
        score += 20
        flags.append("Excessive use of exclamation marks.")
        
    # Rule 3: Repetition of words
    if word_count > 0:
        word_freq = Counter(words)
        most_common = word_freq.most_common(1)
        if most_common and most_common[0][1] > max(3, word_count * 0.3):
            score += 25
            flags.append("High repetition of single words.")
            
    # Rule 4: Promotional or suspicious keywords
    promo_count = sum(1 for p in PROMOTIONAL_WORDS if p in text_lower)
    if promo_count > 0:
        score += (promo_count * 15)
        flags.append("Contains promotional or spam-like keywords.")
        
    # Rule 5: ALL CAPS text
    caps_count = sum(1 for c in text if c.isupper())
    if len(text) > 0 and caps_count / len(text) > 0.4:
        score += 20
        flags.append("Excessive use of capital letters.")
        
    # Cap score at 100
    final_score = min(100, score)
    
    return final_score, flags
