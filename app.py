import streamlit as st
import time
import random
import re
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt

# ── Scraper ───────────────────────────────────────────────────────────────────
try:
    from utils.scraper import extract_reviews, detect_platform
except ImportError:
    def extract_reviews(url): return []
    def detect_platform(url): return None

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fake Review Detector",
    page_icon="🔍",
    layout="wide", # Wider layout for stats
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Reset & base ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* ── Header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    animation: fadeInDown 0.7s ease;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #38bdf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.4rem;
}
.hero p {
    color: #94a3b8;
    font-size: 1rem;
    margin: 0;
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    animation: fadeInUp 0.5s ease;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
}

/* Verdict cards */
.card-fake {
    background: linear-gradient(135deg, rgba(239,68,68,0.18), rgba(185,28,28,0.12));
    border: 1px solid rgba(239,68,68,0.4);
}
.card-genuine {
    background: linear-gradient(135deg, rgba(52,211,153,0.18), rgba(6,95,70,0.12));
    border: 1px solid rgba(52,211,153,0.4);
}

/* ── Metric label ── */
.metric-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748b;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #f1f5f9;
}
.metric-sub {
    font-size: 0.82rem;
    color: #94a3b8;
    margin-top: 0.2rem;
}

/* ── Verdict badge ── */
.badge {
    display: inline-block;
    padding: 0.35rem 1rem;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.badge-fake   { background: rgba(239,68,68,0.25); color: #fca5a5; border: 1px solid rgba(239,68,68,0.5); }
.badge-genuine{ background: rgba(52,211,153,0.25); color: #6ee7b7; border: 1px solid rgba(52,211,153,0.5); }

/* ── Progress bar ── */
.progress-wrap {
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
    margin-top: 0.5rem;
}
.progress-fill-fake    { height:100%; border-radius:999px; background: linear-gradient(90deg,#ef4444,#b91c1c); transition: width 1s ease; }
.progress-fill-genuine { height:100%; border-radius:999px; background: linear-gradient(90deg,#34d399,#059669); transition: width 1s ease; }
.progress-fill-neutral { height:100%; border-radius:999px; background: linear-gradient(90deg,#a78bfa,#6366f1); transition: width 1s ease; }

/* ── Highlight suspicious words ── */
.highlight {
    background: rgba(239,68,68,0.28);
    color: #fca5a5;
    border-radius: 4px;
    padding: 0 3px;
    font-weight: 600;
    border-bottom: 2px solid #ef4444;
}

/* ── Example buttons ── */
.example-label {
    font-size: 0.75rem;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 1.2rem 0;
}

/* ── Stagger animation ── */
.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }
.delay-3 { animation-delay: 0.3s; }
.delay-4 { animation-delay: 0.4s; }
.delay-5 { animation-delay: 0.5s; }

/* ── Keyframes ── */
@keyframes fadeInDown {
    from { opacity:0; transform: translateY(-20px); }
    to   { opacity:1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity:0; transform: translateY(20px); }
    to   { opacity:1; transform: translateY(0); }
}

/* Streamlit widget overrides */
div[data-testid="stTextArea"] textarea, div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: #f1f5f9 !important;
    font-size: 0.95rem !important;
    padding: 0.8rem !important;
    transition: border 0.2s;
}
div[data-testid="stTextArea"] textarea:focus, div[data-testid="stTextInput"] input:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.2) !important;
}
div[data-testid="stButton"] > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Suspicious words list ─────────────────────────────────────────────────────
SUSPICIOUS_WORDS = [
    "amazing", "incredible", "unbelievable", "best ever", "perfect", "love it",
    "awesome", "fantastic", "excellent", "wonderful", "superb", "outstanding",
    "must buy", "highly recommend", "five stars", "game changer", "life changing",
    "exceeded expectations", "blown away", "absolutely love", "obsessed",
    "buy now", "hurry", "limited", "deal", "discount", "free", "bonus",
    "not disappointed", "zero complaints", "flawless", "literally perfect",
]

# ── Example reviews ───────────────────────────────────────────────────────────
EXAMPLES = {
    "🚩 Obvious Fake": (
        "This product is absolutely AMAZING!! Best purchase I have ever made in my entire life. "
        "Incredible quality, exceeded all my expectations. Highly recommend to everyone!! "
        "Five stars isn't enough. Life changing product. BUY NOW before it sells out!!"
    ),
    "✅ Likely Genuine": (
        "Bought this for my home office setup. Build quality is decent for the price. "
        "The instructions were a bit unclear but I managed. Delivery took 5 days. "
        "One small scratch on the corner but nothing major. Overall satisfied."
    ),
    "⚠️ Mixed Signals": (
        "Wonderful product, absolutely love it! However the shipping was slow and packaging "
        "was damaged. Customer service was helpful. Would recommend with caution. "
        "Price seems a bit high but quality is good."
    ),
}


# ── Core ML logic ─────────────────────────────────────────────────────────────
def highlight_suspicious(text: str) -> str:
    highlighted = text
    for word in sorted(SUSPICIOUS_WORDS, key=len, reverse=True):
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        highlighted = pattern.sub(
            lambda m: f'<span class="highlight">{m.group()}</span>',
            highlighted
        )
    return highlighted

def get_sentiment(text: str) -> tuple[float, str]:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.3:
        label = "Positive 😊"
    elif polarity < -0.1:
        label = "Negative 😞"
    else:
        label = "Neutral 😐"
    return round(polarity, 3), label

def compute_fraud_score(text: str) -> float:
    score = 0
    text_lower = text.lower()
    hits = sum(1 for w in SUSPICIOUS_WORDS if w in text_lower)
    score += min(hits * 6, 35)
    excl = text.count("!")
    score += min(excl * 4, 20)
    caps = len(re.findall(r'\\b[A-Z]{3,}\\b', text))
    score += min(caps * 5, 15)
    words = len(text.split())
    if words < 15: score += 10
    if words > 200: score += 5
    superlatives = len(re.findall(r'\\b(best|worst|greatest|perfect|flawless|amazing|incredible)\\b', text_lower))
    score += min(superlatives * 4, 20)
    polarity, _ = get_sentiment(text)
    if polarity > 0.7: score += 10
    return min(round(score, 1), 100)

def predict(text: str) -> dict:
    fraud_score = compute_fraud_score(text)
    polarity, sentiment_label = get_sentiment(text)
    if fraud_score >= 55:
        label = "FAKE"
        confidence = min(50 + fraud_score * 0.5, 97)
    else:
        label = "GENUINE"
        confidence = min(50 + (100 - fraud_score) * 0.47, 96)

    reasons = []
    text_lower = text.lower()
    hits = [w for w in SUSPICIOUS_WORDS if w in text_lower]
    if hits: reasons.append(f"Contains {len(hits)} suspicious/promotional keyword(s): _{', '.join(hits[:5])}_")
    if text.count("!") > 2: reasons.append(f"Overuse of exclamation marks ({text.count('!')} found)")
    caps = re.findall(r'\\b[A-Z]{3,}\\b', text)
    if caps: reasons.append(f"ALL-CAPS words detected: {', '.join(caps[:4])}")
    if polarity > 0.6: reasons.append("Unrealistically positive sentiment")
    if len(text.split()) < 15: reasons.append("Review is unusually short")
    if not reasons: reasons.append("No major red flags detected — language appears natural")

    return {
        "label": label,
        "confidence": round(confidence, 1),
        "fraud_score": fraud_score,
        "polarity": polarity,
        "sentiment": sentiment_label,
        "reasons": reasons,
        "highlighted_text": highlight_suspicious(text),
    }

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔍 Fake Review Detector</h1>
    <p>Powered by NLP heuristics · Sentiment analysis · Fraud scoring</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 Single Review", "🔗 URL Analysis (Beta)"])

with tab1:
    # ── Example buttons ───────────────────────────────────────────────────────────
    st.markdown('<div class="example-label">⚡ Quick examples</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    selected_example = None
    for i, (label, review) in enumerate(EXAMPLES.items()):
        if cols[i].button(label, use_container_width=True):
            selected_example = review

    # ── Text area ─────────────────────────────────────────────────────────────────
    default_text = selected_example if selected_example else ""
    review_text = st.text_area(
        "Paste or type a product review below:",
        value=default_text,
        height=150,
        placeholder="e.g. This product is absolutely amazing!! Best purchase ever. Highly recommend!!",
        label_visibility="visible",
    )

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    analyze_btn = st.button("🔍 Analyze Review", type="primary", use_container_width=True)

    # ── Results ───────────────────────────────────────────────────────────────────
    if analyze_btn:
        if not review_text.strip():
            st.warning("⚠️ Please enter a review to analyze.")
        else:
            with st.spinner("Analyzing review..."):
                time.sleep(0.5)
                result = predict(review_text)

            is_fake = result["label"] == "FAKE"
            card_class  = "card-fake"    if is_fake else "card-genuine"
            badge_class = "badge-fake"   if is_fake else "badge-genuine"
            bar_class   = "progress-fill-fake" if is_fake else "progress-fill-genuine"
            icon        = "🚨"           if is_fake else "✅"
            color       = "#fca5a5"      if is_fake else "#6ee7b7"

            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            # ── 1. Verdict ──
            st.markdown(f"""
            <div class="card {card_class}">
                <div class="metric-label">Verdict</div>
                <div style="display:flex; align-items:center; gap:1rem; margin-top:0.4rem;">
                    <span style="font-size:2.4rem;">{icon}</span>
                    <div>
                        <span class="badge {badge_class}">{result['label']}</span>
                        <div class="metric-sub" style="margin-top:0.4rem;">
                            This review is most likely <strong style="color:{color};">{result['label'].lower()}</strong>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── 2. Confidence + Fraud Score ──
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="card delay-1">
                    <div class="metric-label">Confidence</div>
                    <div class="metric-value">{result['confidence']}%</div>
                    <div class="progress-wrap">
                        <div class="{bar_class}" style="width:{result['confidence']}%"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                fraud_bar = "progress-fill-fake" if result['fraud_score'] > 50 else "progress-fill-neutral"
                st.markdown(f"""
                <div class="card delay-2">
                    <div class="metric-label">Fraud Score</div>
                    <div class="metric-value">{result['fraud_score']}<span style="font-size:1rem;color:#64748b;">/100</span></div>
                    <div class="progress-wrap">
                        <div class="{fraud_bar}" style="width:{result['fraud_score']}%"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ── 3. Sentiment ──
            polarity_pct = round((result['polarity'] + 1) / 2 * 100, 1)
            polarity_bar = (
                "progress-fill-genuine" if result['polarity'] > 0.1
                else "progress-fill-fake" if result['polarity'] < -0.05
                else "progress-fill-neutral"
            )
            st.markdown(f"""
            <div class="card delay-3">
                <div class="metric-label">Sentiment Polarity</div>
                <div style="display:flex; justify-content:space-between; align-items:baseline;">
                    <div class="metric-value">{result['polarity']}</div>
                    <div class="metric-sub">{result['sentiment']}</div>
                </div>
                <div class="progress-wrap">
                    <div class="{polarity_bar}" style="width:{polarity_pct}%"></div>
                </div>
                <div class="metric-sub" style="margin-top:0.5rem;">Scale: −1 (very negative) → +1 (very positive)</div>
            </div>
            """, unsafe_allow_html=True)

            # ── 4. Highlighted review ──
            st.markdown(f"""
            <div class="card delay-4">
                <div class="metric-label">🔦 Suspicious Words Highlighted</div>
                <div style="margin-top:0.7rem; color:#cbd5e1; line-height:1.7; font-size:0.95rem;">
                    {result['highlighted_text']}
                </div>
                <div class="metric-sub" style="margin-top:0.8rem;">
                    <span class="highlight" style="font-size:0.75rem; padding:1px 6px;">red highlights</span>
                    &nbsp;= promotional / suspicious language
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── 5. Explanation ──
            reasons_html = "".join(f"<li style='margin-bottom:0.4rem;'>{r}</li>" for r in result['reasons'])
            st.markdown(f"""
            <div class="card delay-5">
                <div class="metric-label">🧠 Analysis Explanation</div>
                <ul style="margin-top:0.7rem; color:#cbd5e1; font-size:0.92rem; padding-left:1.2rem; line-height:1.8;">
                    {reasons_html}
                </ul>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 🌐 Analyze Reviews from URL")
    st.markdown("<p style='color:#94a3b8;'>Paste an Amazon or Flipkart product URL to fetch and analyze reviews automatically.</p>", unsafe_allow_html=True)
    
    url_input = st.text_input("Product URL:", placeholder="https://www.amazon.in/dp/B08N5WRWNW", label_visibility="collapsed")
    
    if st.button("🚀 Scrape & Analyze Reviews", type="primary", use_container_width=True, key="url_btn"):
        if not url_input.strip():
            st.warning("⚠️ Please enter a URL.")
        else:
            platform = detect_platform(url_input)
            if not platform:
                st.error("❌ Unsupported URL. Please provide an Amazon or Flipkart product link.")
            else:
                with st.spinner(f"Scraping reviews from {platform.title()}... (This may take a moment)"):
                    reviews = extract_reviews(url_input)
                    
                if not reviews:
                    st.error("⚠️ Unable to fetch reviews (site protection or no reviews found). Try another link.")
                else:
                    st.success(f"✅ Successfully extracted {len(reviews)} reviews! Analyzing...")
                    
                    # Analyze all reviews
                    results = []
                    progress_text = "Analyzing reviews..."
                    my_bar = st.progress(0, text=progress_text)
                    
                    for i, rev in enumerate(reviews):
                        res = predict(rev)
                        res['original_text'] = rev
                        results.append(res)
                        my_bar.progress((i + 1) / len(reviews), text=f"Analyzing {i+1}/{len(reviews)}")
                        
                    my_bar.empty()
                    
                    # Aggregate stats
                    df = pd.DataFrame(results)
                    total_reviews = len(df)
                    fake_count = len(df[df['label'] == 'FAKE'])
                    genuine_count = len(df[df['label'] == 'GENUINE'])
                    fake_pct = (fake_count / total_reviews) * 100
                    genuine_pct = (genuine_count / total_reviews) * 100
                    
                    st.markdown('<hr class="divider">', unsafe_allow_html=True)
                    st.markdown("### 📊 Aggregated Statistics")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f'''
                        <div class="card" style="text-align:center;">
                            <div class="metric-label">Total Reviews</div>
                            <div class="metric-value">{total_reviews}</div>
                        </div>''', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'''
                        <div class="card card-fake" style="text-align:center;">
                            <div class="metric-label">Fake Reviews</div>
                            <div class="metric-value" style="color:#fca5a5;">{fake_count}</div>
                            <div class="metric-sub">{fake_pct:.1f}%</div>
                        </div>''', unsafe_allow_html=True)
                    with col3:
                        st.markdown(f'''
                        <div class="card card-genuine" style="text-align:center;">
                            <div class="metric-label">Genuine Reviews</div>
                            <div class="metric-value" style="color:#6ee7b7;">{genuine_count}</div>
                            <div class="metric-sub">{genuine_pct:.1f}%</div>
                        </div>''', unsafe_allow_html=True)
                    
                    # Charts using matplotlib (dark theme styling)
                    plt.style.use('dark_background')
                    fig_col1, fig_col2 = st.columns(2)
                    
                    with fig_col1:
                        st.markdown("**Fake vs Genuine Distribution**")
                        fig, ax = plt.subplots(figsize=(5, 4))
                        fig.patch.set_facecolor('none')
                        ax.set_facecolor('none')
                        ax.pie([fake_count, genuine_count], labels=['Fake', 'Genuine'], autopct='%1.1f%%', 
                               colors=['#ef4444', '#34d399'], textprops={'color':"w"})
                        st.pyplot(fig)
                        
                    with fig_col2:
                        st.markdown("**Sentiment Distribution**")
                        sentiment_counts = df['sentiment'].value_counts()
                        fig2, ax2 = plt.subplots(figsize=(5, 4))
                        fig2.patch.set_facecolor('none')
                        ax2.set_facecolor('none')
                        sentiment_counts.plot(kind='bar', color='#a78bfa', ax=ax2)
                        plt.xticks(rotation=45)
                        ax2.tick_params(colors='white')
                        st.pyplot(fig2)
                        
                    st.markdown("### 📝 Extracted Reviews Breakdown")
                    for i, row in df.iterrows():
                        is_fake = row['label'] == 'FAKE'
                        icon = "🚨 FAKE" if is_fake else "✅ GENUINE"
                        
                        with st.expander(f"{icon} (Fraud Score: {row['fraud_score']}) - {row['original_text'][:60]}..."):
                            st.markdown(f"**Confidence:** {row['confidence']}%")
                            st.markdown(f"**Sentiment:** {row['sentiment']} ({row['polarity']})")
                            st.markdown("**Highlighted Text:**")
                            st.markdown(row['highlighted_text'], unsafe_allow_html=True)
                            st.markdown("**Reasons:**")
                            for r in row['reasons']:
                                st.markdown(f"- {r}")

# ── Footer note ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#334155; font-size:0.75rem; margin-top:2.5rem; padding-bottom:2rem;">
    Results based on heuristic NLP analysis · Not 100% accurate · For educational use
</div>
""", unsafe_allow_html=True)
