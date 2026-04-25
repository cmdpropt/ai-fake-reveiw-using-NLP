import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import json

from utils.preprocess import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'model')
os.makedirs(MODEL_DIR, exist_ok=True)

def create_expanded_dataset():
    """Generates a slightly larger synthetic dataset to better train models."""
    data = [
        ("This product is absolutely amazing! I highly recommend it.", "Genuine"),
        ("Terrible quality. It broke after one use. Do not buy.", "Genuine"),
        ("Decent for the price, but could be better.", "Genuine"),
        ("I received a totally different item than what I ordered. Scam!", "Genuine"),
        ("Great customer service and fast shipping.", "Genuine"),
        ("Worst purchase ever. Complete waste of money.", "Genuine"),
        ("Love it! Exactly as described and works perfectly.", "Genuine"),
        ("Very dissatisfied. The material feels cheap and flimsy.", "Genuine"),
        ("I wouldn't recommend this to anyone. Stay away.", "Genuine"),
        ("Best thing I've bought all year. Highly recommended.", "Genuine"),
        ("This is the worst item, returning it immediately.", "Genuine"),
        ("Okay product. Doesn't quite live up to the hype, but functional.", "Genuine"),
        ("Amazing product, totally worth it. I am very happy.", "Genuine"),
        ("Do not buy this. It is poorly made.", "Genuine"),
        
        ("This is a fake review I was paid to write this 5 stars.", "Fake"),
        ("Click here to buy cheap pills! Best deal!", "Fake"),
        ("Excellent product, fast delivery, A++++", "Fake"),
        ("Earn $500 a day working from home just click my link", "Fake"),
        ("User review generator produced this amazing content.", "Fake"),
        ("Wow, I earned so much money from this link!", "Fake"),
        ("Absolutely perfect! Flawless! Best thing ever! BUY NOW!", "Fake"),
        ("Check out my profile for discount codes and free stuff", "Fake"),
        ("Make money fast, click the bio link now!!!", "Fake"),
        ("Follow me for more amazing reviews and giveaways", "Fake"),
        ("Spam bot automatically generating good reviews for this item", "Fake"),
        ("Click my link to get a 90% discount instantly!", "Fake"),
        ("Guaranteed the best! You will not regret this! Excellent!", "Fake"),
        ("I was paid to give a five star review for this product.", "Fake")
    ]
    df = pd.DataFrame(data, columns=["review", "label"])
    df = pd.concat([df]*5, ignore_index=True)
    return df

def train_models():
    print("Loading data...")
    df = create_expanded_dataset()
    
    print("Preprocessing text...")
    df['cleaned_review'] = df['review'].apply(clean_text)
    
    df.to_csv(os.path.join(MODEL_DIR, "dataset_stats.csv"), index=False)
    
    X = df['cleaned_review']
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, class_weight='balanced'),
        'Naive Bayes': MultinomialNB(),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    }
    
    results = {}
    best_acc = 0
    best_model_name = ""
    
    for name, clf in models.items():
        print(f"\\nTraining {name}...")
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
            ('clf', clf)
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {acc:.4f}")
        
        results[name] = {
            'accuracy': float(acc),
            'report': classification_report(y_test, y_pred, output_dict=True)
        }
        
        filename = "logistic.pkl" if "Logistic" in name else "nb.pkl" if "Naive" in name else "rf.pkl"
        with open(os.path.join(MODEL_DIR, filename), 'wb') as f:
            pickle.dump(pipeline, f)
            
        if acc > best_acc:
            best_acc = acc
            best_model_name = name
            
    with open(os.path.join(MODEL_DIR, "model_metrics.json"), 'w') as f:
        json.dump({
            "results": results,
            "best_model": best_model_name
        }, f, indent=4)
        
    print(f"\\nTraining complete! Best model: {best_model_name} with {best_acc:.4f} accuracy.")

if __name__ == "__main__":
    train_models()
