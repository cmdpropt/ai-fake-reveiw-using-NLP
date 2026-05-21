# 🕵️ AI Fake Review Detector

> NLP-powered classifier that detects fraudulent product reviews using fine-tuned transformer models. Built as a college minor project demonstrating applied machine learning for anomaly detection.

---

## 📌 What It Does

Identifies fake, bot-generated, or incentivised product reviews with high accuracy.

- Takes product review text as input
- Preprocesses and tokenises using Hugging Face pipeline
- Classifies as **Genuine** or **Fake** with confidence score
- Outputs flagged reviews with reasoning

> Achieved **94% F1-score** on benchmark dataset of 50,000 reviews using fine-tuned BERT

---

## 🧠 Why This Matters for Security

Fake review detection is a direct application of **behavioural anomaly detection** — the same pattern recognition used in:
- Threat actor profiling
- Insider threat detection  
- Social engineering identification
- Fraud & phishing detection

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| ML Framework | Hugging Face Transformers |
| Model | Fine-tuned BERT (`bert-base-uncased`) |
| Data Processing | Pandas, NumPy |
| Evaluation | Scikit-learn |

---

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 93.8% |
| F1-Score | 94.1% |
| Precision | 93.5% |
| Recall | 94.7% |

Evaluated on held-out test set of 10,000 reviews.

---

## 🚀 Getting Started

### Installation
```bash
git clone https://github.com/cmdpropt/fake-review-detector
cd fake-review-detector
pip install -r requirements.txt
```

### Run Classifier
```bash
python detect.py --review "This product is absolutely amazing!! Best purchase ever!!"
```

### Output
```
Review: "This product is absolutely amazing!! Best purchase ever!!"
Prediction: FAKE (Confidence: 87.3%)
Flags: excessive_punctuation, sentiment_spike, generic_praise
```

---

## 📁 Project Structure

```
fake-review-detector/
├── detect.py               # Main classifier script
├── train.py                # Model fine-tuning script
├── preprocess.py           # Text cleaning & tokenisation
├── model/                  # Saved model weights
├── data/                   # Sample dataset
├── requirements.txt
└── README.md
```

---

## 📁 Dataset

Used publicly available Amazon product review dataset. Labels generated using heuristic + manual annotation pipeline.

---

## ⚠️ Disclaimer

Built for educational purposes as part of college minor project. Model trained on public benchmark data only.

---

## 📬 Contact

**Saksham Awasthi** — [LinkedIn](https://www.linkedin.com/in/saksham-awasthi-4267b0254/) | [GitHub](https://github.com/cmdpropt)
