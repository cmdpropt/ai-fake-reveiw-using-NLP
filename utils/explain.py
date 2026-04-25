import numpy as np

def explain_prediction(model_pipeline, text_features):
    """
    Provides explainability by identifying which words contributed to the decision.
    Works specifically for Logistic Regression.
    """
    clf = model_pipeline.named_steps.get('clf')
    tfidf = model_pipeline.named_steps.get('tfidf')
    
    if not hasattr(clf, 'coef_'):
        return None, "Explainability is not available for this model type (requires linear coefficients like Logistic Regression)."
        
    feature_names = tfidf.get_feature_names_out()
    coefs = clf.coef_[0]
    
    text_vector = tfidf.transform([text_features])
    indices = text_vector.nonzero()[1]
    
    if len(indices) == 0:
        return {}, "No significant vocabulary features found in this text."
        
    contributions = []
    for idx in indices:
        feat_name = feature_names[idx]
        feat_val = text_vector[0, idx]
        coef_val = coefs[idx]
        contribution = feat_val * coef_val
        contributions.append((feat_name, contribution))
        
    contributions.sort(key=lambda x: abs(x[1]), reverse=True)
    
    # Sklearn classes are sorted alphabetically: 'Fake' is 0, 'Genuine' is 1.
    # Therefore, negative coefficients push towards 'Fake', positive towards 'Genuine'.
    
    impact_dict = {
        'strong_fake': [word for word, score in contributions if score < -0.05][:5],
        'strong_genuine': [word for word, score in contributions if score > 0.05][:5]
    }
    
    explanation = ""
    if impact_dict['strong_fake']:
        explanation += f"Suspicious (Fake-leaning) keywords detected: {', '.join(impact_dict['strong_fake'])}. "
    if impact_dict['strong_genuine']:
        explanation += f"Authentic-leaning keywords detected: {', '.join(impact_dict['strong_genuine'])}. "
        
    if not explanation:
        explanation = "The prediction is based on general vocabulary patterns without strong specific keywords."
        
    return impact_dict, explanation

def highlight_text(text, suspicious_words):
    """
    Returns HTML string with suspicious words highlighted in red.
    """
    import re
    if not suspicious_words:
        return text
        
    highlighted = text
    for word in suspicious_words:
        pattern = re.compile(rf'\b({word})\b', re.IGNORECASE)
        highlighted = pattern.sub(r'<span style="background-color: #ffcccc; color: #cc0000; font-weight: bold; padding: 2px; border-radius: 3px;">\1</span>', highlighted)
        
    return highlighted
