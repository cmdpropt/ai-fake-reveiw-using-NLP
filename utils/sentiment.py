from textblob import TextBlob

def get_sentiment(text):
    """
    Returns sentiment polarity and subjectivity using TextBlob.
    Polarity: -1.0 (Negative) to 1.0 (Positive)
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    # Determine label
    if polarity > 0.1:
        sentiment_label = "Positive"
    elif polarity < -0.1:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"
        
    return polarity, sentiment_label
