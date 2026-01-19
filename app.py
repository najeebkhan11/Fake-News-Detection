import streamlit as st
import pickle
import re
import time

# ================= LOAD MODEL =================
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ================= SESSION STATE =================
if "scam_keywords" not in st.session_state:
    st.session_state.scam_keywords = [
        "urgent", "immediate action", "act now", "last chance",
        "account will be blocked", "congratulations", "credit",
        "you have won", "lottery", "prize", "cash reward",
        "free gift", "bank", "sbi", "rbi", "kyc",
        "verify", "click here", "otp", "pin", "cvv",
        "send", "account", "work from home", "earn", "per day"
    ]

# ================= FUNCTIONS =================
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z ]", "", text)
    return text

def alert_card(icon, text, type="info"):
    st.markdown(
        f"""
        <div class="alert alert-{type}">
            <div class="alert-icon">{icon}</div>
            <div class="alert-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Fake News & Scam Detection",
    page_icon="🛡️",
    layout="centered"
)

# ================= THEME TOGGLE =================
dark_mode = st.toggle("🌗 Dark Mode")

bg = "#0e1117" if dark_mode else "#f5f7fb"
card = "#161b22" if dark_mode else "#ffffff"
text_color = "white" if dark_mode else "#1f2937"

st.markdown(f"""
<style>

/* ================= ROOT ================= */
.stApp {{
    background-color: {"#0e1117" if dark_mode else "#f8fafc"};
    color: {"#ffffff" if dark_mode else "#0f172a"};
    font-family: 'Segoe UI', system-ui, sans-serif;
}}

/* ================= CARD ================= */
.card {{
    background: {"rgba(22,27,34,0.95)" if dark_mode else "#ffffff"};
    padding: 28px;
    border-radius: 20px;
    box-shadow: 0 18px 40px rgba(0,0,0,0.15);
    margin-bottom: 34px;
    animation: fadeIn 0.5s ease;
}}

/* ================= ALERT BASE ================= */
.alert {{
    display: flex;
    gap: 16px;
    padding: 18px 22px;
    border-radius: 16px;
    margin-bottom: 20px;
    animation: slideUp 0.4s ease;
}}

.alert-icon {{
    font-size: 22px;
}}

.alert-text {{
    font-size: 15px;
    line-height: 1.6;
    color: {"#ffffff" if dark_mode else "#0f172a"};
}}

/* ================= DARK MODE ALERTS ================= */
{""
if not dark_mode else
"""
.alert-info {{
    background: linear-gradient(135deg, #1f3b5b, #162b40);
    border-left: 6px solid #4b6cb7;
}}

.alert-warning {{
    background: linear-gradient(135deg, #5b3a1f, #402616);
    border-left: 6px solid #f59e0b;
}}

.alert-danger {{
    background: linear-gradient(135deg, #5b1f1f, #401616);
    border-left: 6px solid #ef4444;
}}

.alert-success {{
    background: linear-gradient(135deg, #1f5b3a, #16402b);
    border-left: 6px solid #22c55e;
}}
"""
}

/* ================= LIGHT MODE ALERTS ================= */
{""
if dark_mode else
"""
.alert-info {{
    background: linear-gradient(135deg, #e0ecff, #dbeafe);
    border-left: 6px solid #2563eb;
}}

.alert-warning {{
    background: linear-gradient(135deg, #fff7ed, #ffedd5);
    border-left: 6px solid #f59e0b;
}}

.alert-danger {{
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    border-left: 6px solid #dc2626;
}}

.alert-success {{
    background: linear-gradient(135deg, #dcfce7, #bbf7d0);
    border-left: 6px solid #16a34a;
}}
"""
}

/* ================= INPUTS ================= */
textarea, input {{
    background-color: {"#161b22" if dark_mode else "#ffffff"} !important;
    color: {"#ffffff" if dark_mode else "#0f172a"} !important;
    border-radius: 12px !important;
}}

/* ================= BUTTONS ================= */
button {{
    background: linear-gradient(135deg, #4b6cb7, #182848) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 8px 18px !important;
}}

/* ================= PROGRESS ================= */
.stProgress > div > div {{
    background: linear-gradient(90deg, #4b6cb7, #22c55e);
}}

/* ================= ANIMATIONS ================= */
@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}

@keyframes slideUp {{
    from {{ transform: translateY(12px); opacity: 0; }}
    to {{ transform: translateY(0); opacity: 1; }}
}}

</style>
""", unsafe_allow_html=True)


# ================= HEADER =================
st.markdown("""
<h1 style="text-align:center;">🛡️ Fake News & Scam Detection</h1>
<p style="text-align:center; opacity:0.85;">
Hybrid AI System using NLP, Machine Learning & Rule-Based Intelligence
</p>
""", unsafe_allow_html=True)

# ================= TABS =================
tab1, tab2 = st.tabs(["📰 Fake News Detection", "🚨 Scam Message Detection"])

# =====================================================
# TAB 1 : FAKE NEWS
# =====================================================
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    alert_card(
        "📰",
        "<b>Use this tab ONLY for news articles.</b><br>"
        "For SMS / WhatsApp / bank / lottery messages → use <b>🚨 Scam Message Detection</b>.",
        "info"
    )

    with st.form("fake_news_form"):
        news = st.text_area(
            "Paste News Article",
            height=180,
            placeholder="Example: Scientists claim a new planet has been discovered..."
        )
        submit_news = st.form_submit_button("🔍 Analyze News")

    if submit_news:
        if not news.strip():
            st.toast("Please enter a news article", icon="⚠️")
            alert_card("⚠️", "Please enter a news article.", "warning")
        else:
            with st.spinner("Analyzing news with AI..."):
                time.sleep(0.6)
                cleaned = clean_text(news)

                scam_guard = [
    # Sensational / Clickbait
    "breaking news", "shocking truth", "secret plan exposed",
    "this will change everything", "media wont show", "hidden agenda",
    "big conspiracy", "leaked", "shocking video",

    # Government / Authority misuse
    "government hiding", "vote cancelled", "pm announced",
    "new rule from tonight", "government scheme", "debt waived",
    "bank collapse", "license cancelled", "police alert",
    "curfew announced", "section 144", "new fine",

    # Health misinformation
    "doctors dont want you to know", "miracle cure",
    "instant recovery", "natural treatment", "cure in 3 days",
    "scientifically proven",

    # Financial misinformation
    "free money", "instant loan", "100 guaranteed",
    "15 lakh credited",

    # Panic / Emergency
    "alert", "warning", "emergency", "evacuate immediately",
    "cyclone confirmed", "earthquake expected", "earthquake"

    # Social / Religious manipulation
    "temple destroyed", "mosque destroyed", "religion in danger",
    "ban", "attack",

    # Viral fake updates
    "whatsapp charging money", "forward to save account",
    "blue tick danger", "phone will explode", "new update",

    # Education panic
    "exam cancelled", "result leaked", "holiday declared",
    "degree invalid", "university closed",

    # Death / Crime exaggeration
    "died", "arrested", "hospitalized", "banned",

    # Pseudoscience
    "nasa confirms", "ancient secret",
    "energy waves", "vibrations"
]

                if any(word in cleaned for word in scam_guard):
                    st.toast("Looks like a scam message", icon="🚨")
                    alert_card(
                        "⚠️",
                        "<b>This looks like a scam message.</b><br>"
                        "Please use the <b>🚨 Scam Message Detection</b> tab.",
                        "warning"
                    )
                else:
                    vect = vectorizer.transform([cleaned])
                    pred = model.predict(vect)[0]
                    proba = model.predict_proba(vect)[0]
                    confidence = max(proba) * 100

                    st.write("📊 Prediction Confidence")
                    st.progress(int(confidence))
                    st.write(f"**{confidence:.2f}%**")

                    if pred == "FAKE":
                        st.toast("Fake news detected", icon="🚨")
                        alert_card("🚨", "<b>FAKE NEWS DETECTED</b>", "danger")
                    else:
                        st.toast("News looks real", icon="✅")
                        alert_card("✅", "<b>This news appears REAL</b>", "success")

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# TAB 2 : SCAM DETECTION
# =====================================================
with tab2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    alert_card(
        "🚨",
        "<b>Use this tab for scam / fraud messages.</b><br>"
        "SMS, WhatsApp, bank alerts, lottery offers, job scams.",
        "info"
    )

    with st.form("scam_form"):
        msg = st.text_area(
            "Paste Message / SMS / WhatsApp Text",
            height=180,
            placeholder="Example: Congratulations! You have won a lottery..."
        )
        submit_scam = st.form_submit_button("🔍 Detect Scam")

    if submit_scam:
        if not msg.strip():
            st.toast("Please enter a message", icon="⚠️")
            alert_card("⚠️", "Please enter a message.", "warning")
        else:
            with st.spinner("Scanning message for scam patterns..."):
                time.sleep(0.5)
                cleaned = clean_text(msg)
                matched = [kw for kw in st.session_state.scam_keywords if kw in cleaned]

                risk_score = (len(matched) / len(st.session_state.scam_keywords)) * 100
                st.write("⚠️ Scam Risk Level")
                st.progress(int(risk_score))
                st.write(f"**{risk_score:.2f}%**")

                if matched:
                    st.toast("Scam detected!", icon="🚨")
                    alert_card(
                        "🚨",
                        "<b>SCAM DETECTED</b><br>"
                        "High-risk scam indicators found.",
                        "danger"
                    )

                    highlighted = msg
                    for word in matched:
                        highlighted = re.sub(
                            word,
                            f"<span style='background:#ff4b4b;color:white;padding:2px 6px;border-radius:4px;'>{word}</span>",
                            highlighted,
                            flags=re.IGNORECASE
                        )

                    st.markdown(highlighted, unsafe_allow_html=True)
                else:
                    st.toast("Message looks safe", icon="✅")
                    alert_card(
                        "✅",
                        "<b>No scam patterns detected.</b><br>"
                        "Message appears safe.",
                        "success"
                    )

    st.markdown("</div>", unsafe_allow_html=True)

# ================= KEYWORD MANAGER =================
with st.expander("⚙️ Scam Keyword Manager"):
    st.write(", ".join(sorted(set(st.session_state.scam_keywords))))
    new_kw = st.text_input("Add new keyword")
    if st.button("Add Keyword"):
        if new_kw.strip():
            st.session_state.scam_keywords.append(new_kw.lower())
            st.toast("Keyword added", icon="✅")

# ================= FOOTER =================
st.markdown("""
<hr>
<div style="text-align:center; font-size:14px; opacity:0.7;">
🛡️ Fake News & Scam Detection System<br>
Built with Python • NLP • Machine Learning • Streamlit<br>
</div>
""", unsafe_allow_html=True)
