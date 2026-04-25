
# 🛡️ Fake Review Intelligence System

An advanced examiner-level machine learning web application that detects whether a given product review is Fake or Genuine using NLP, Explainable AI, and Behavioral Fraud Detection.

## Features Added in Advanced Version
- **Explainable AI (XAI)**: Highlights the exact words that contributed to the model's prediction. Explains *why* a review was flagged.
- **Multi-Model Support**: Trains and automatically selects the best among **Logistic Regression, Naive Bayes, and Random Forest**. The active model can be toggled via the UI sidebar.
- **Behavioral Fraud Detection**: Cybersecurity-style rule-based analysis (checks for review length, overused exclamation marks, word repetition, promotional keywords, all-caps). Outputs a **Fraud Score (0-100)**.
- **Data Insights Layer**: Visualizes class distributions and global word clouds from the training dataset.
- **Upgraded Streamlit UI**: 
  - Dynamic Probability / Confidence Bars (Low, Medium, High).
  - Color-coded metrics.
  - Interactive test examples.

## Project Structure
```
Fake_Review_Detector/
│── app.py                 # Advanced Streamlit web application
│── train.py               # Multi-model training script
│── requirements.txt       # Python dependencies (now includes wordcloud, matplotlib)
│── README.md              # Project documentation
│── model/
│    ├── logistic.pkl      # Serialized Logistic Regression
│    ├── nb.pkl            # Serialized Naive Bayes
│    ├── rf.pkl            # Serialized Random Forest
│    ├── model_metrics.json# Training results & accuracy comparison
│    └── dataset_stats.csv # Processed dataset for Data Insights tab
│── utils/
│    ├── preprocess.py     # Text cleaning & tokenization logic
│    ├── sentiment.py      # Sentiment analysis logic
│    ├── explain.py        # Explainable AI logic & text highlighting
│    └── fraud_detection.py# Rule-based behavioral anomaly scoring
```

## Installation

1. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

1. **Train the Models**:
Before running the app, you need to train the models and generate the files in the `model/` folder.
```bash
python train.py
```

2. **Start the Web App**:
```bash
streamlit run app.py
```

3. Open your browser to the URL provided (usually `http://localhost:8501`).

## Using the System
- **Detection Engine Tab**: Paste a review or click the Example Buttons. View AI confidence, sentiment, fraud score, and reasoning.
- **Data Insights Tab**: View charts detailing model training data distribution and common terminology.
- **Sidebar**: Switch models and compare testing accuracies.
