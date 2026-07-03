import streamlit as st
import plotly.graph_objects as go
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS & DATA
# ══════════════════════════════════════════════════════════════════════════════

PUPPETEERS = {
    "optimizer":  {"label": "🔴 The Optimizer",    "color": "#FF4B4B"},
    "monetizer":  {"label": "🟠 The Monetizer",    "color": "#FF8C42"},
    "engager":    {"label": "🔵 The Engager",      "color": "#4A90D9"},
    "gatekeeper": {"label": "🟡 The Gatekeeper",   "color": "#F5C518"},
    "invisible":  {"label": "⚫ The Invisible One", "color": "#888888"},
}

PUPPETEER_SUMMARY = {
    "optimizer":  "Systems engineered to make decisions faster than you can think. They removed friction from your life — and your agency with it.",
    "monetizer":  "Systems engineered to extract maximum commercial value from your attention. You're not the user. You're the product.",
    "engager":    "Systems engineered to keep you on-screen as long as possible. They didn't make your life better. They made you harder to put down.",
    "gatekeeper": "Systems that filter your access to opportunity at scale — with no nuance, no context, no appeal.",
    "invisible":  "Systems with no stated purpose. Running in the background of your life. You agreed to them when you accepted a terms & conditions you didn't read.",
}

DOMINANT_CONSEQUENCES = {
    "optimizer": (
        "Your life is heavily optimised — by someone else's definition of optimal. "
        "The Optimizer has been removing your friction before you knew it was there. "
        "The question is: whose efficiency is being served?"
    ),
    "monetizer": (
        "A significant portion of your digital life is a commercial pipeline. "
        "The Monetizer has been surfacing what pays and burying what doesn't — "
        "in your feed, your search results, and your price tags."
    ),
    "engager": (
        "Your attention is the product. The Engager has been engineering your emotional state "
        "across multiple platforms — triggering outrage, curiosity, and social comparison "
        "to keep you in the loop. The loop is designed to have no exit."
    ),
    "gatekeeper": (
        "More of your day is controlled by automated filtering than you realise. "
        "The Gatekeeper has been making access decisions at scale — "
        "with no nuance, no context, and no appeal process."
    ),
    "invisible": (
        "The most significant systems in your life are the ones you can't name. "
        "The Invisible One has been collecting, inferring, and acting — "
        "with no stated agenda, no named operator, and no obligation to tell you."
    ),
}

# ── App → Puppeteer mapping (for multiselect dropdowns) ──────────────────────
APP_MAP = {
    # OPTIMIZER
    "Google Maps":                    "optimizer",
    "Gboard / SwiftKey Keyboard":     "optimizer",
    "Sleep Tracker / Alarm App":      "optimizer",
    "Samsung Health / Fitbit":        "optimizer",
    "Google Assistant / Siri":        "optimizer",
    "Calendar / Reminders App":       "optimizer",
    "Autocorrect / Predictive Text":  "optimizer",
    # MONETIZER
    "Amazon / Flipkart":              "monetizer",
    "Swiggy / Zomato":                "monetizer",
    "Myntra / Meesho / AJIO":         "monetizer",
    "CRED":                           "monetizer",
    "Groww / Zerodha / Upstox":       "monetizer",
    "Ola / Uber / Rapido":            "monetizer",
    "Blinkit / Zepto / Dunzo":        "monetizer",
    "MakeMyTrip / Goibibo":           "monetizer",
    # ENGAGER
    "Instagram":                      "engager",
    "YouTube":                        "engager",
    "Facebook":                       "engager",
    "Twitter / X":                    "engager",
    "Snapchat":                       "engager",
    "ShareChat / Moj / Josh":         "engager",
    "Spotify / JioSaavn / Gaana":     "engager",
    "Netflix / Hotstar / Prime Video":"engager",
    "Reddit":                         "engager",
    "LinkedIn (Feed / Notifications)":"engager",
    # GATEKEEPER
    "Gmail / Email App":              "gatekeeper",
    "Banking / UPI Apps":             "gatekeeper",
    "College / Office Portal":        "gatekeeper",
    "Aadhaar / DigiLocker":           "gatekeeper",
    "LinkedIn Jobs":                  "gatekeeper",
    "Job Portals (Naukri / Indeed)":  "gatekeeper",
    # INVISIBLE
    "WhatsApp":                       "invisible",
    "Telegram":                       "invisible",
    "News Apps (Inshorts / TOI / NDTV)": "invisible",
    "Weather Apps":                   "invisible",
    "Chrome / Safari Browser":        "invisible",
    "Phone's Default / Pre-installed Apps": "invisible",
    "Any App You Didn't Consciously Choose": "invisible",
}

# ── Behavioral decisions (checkboxes, time-of-day organized from My Day) ──────
BEHAVIORAL_DECISIONS = {
    "🌅  Morning Routine": {
        "Sleep tracker decided when my alarm rang": ("optimizer", 2, "decided when your alarm rang based on your sleep phase"),
        "Phone screen auto-adjusted brightness before I touched it": ("optimizer", 1, "optimised your screen before you made a conscious choice"),
        "News feed was the first thing I checked this morning": ("engager", 3, "loaded outrage content first — anger drives 2.3x engagement"),
        "YouTube recommended a video I didn't search for": ("engager", 2, "its algorithm chose your first content of the day"),
        "Maps suggested my route before I opened the app": ("optimizer", 2, "inferred your destination from your location history"),
        "WhatsApp / keyboard smart suggestions appeared while replying": ("optimizer", 1, "predicted your reply before you thought of it"),
        "A push notification pulled me to an app I wasn't using": ("engager", 2, "was timed to your peak attention window"),
    },
    "📱  Social Media & Content": {
        "Instagram showed me a sponsored post in my first 5 scrolls": ("engager", 3, "showed you sponsored posts as the 3rd item in your feed"),
        "YouTube autoplay started the next video without asking": ("engager", 3, "autoplay kept you watching 47 unplanned minutes — documented"),
        "Facebook amplified something that made me feel angry or anxious": ("engager", 2, "amplified emotionally charged content to increase engagement"),
        "Twitter / X surfaced outrage content in my feed": ("engager", 2, "surfaced outrage-optimised content to maximise time on platform"),
        "I watched Reels / Shorts / TikTok for longer than I planned": ("engager", 3, "used short-loop dopamine mechanics to keep you scrolling"),
        "LinkedIn showed me a job I didn't search for (recruiter paid)": ("monetizer", 2, "showed you job postings you didn't search for — recruiters paid for this"),
        "My podcast or music app played something I didn't choose": ("engager", 1, "mood-inferred playlist selection based on your listening patterns"),
        "Engagement bots liked my post within minutes of publishing": ("engager", 2, "45% of Indian Instagram engagement is artificial — HypeAuditor 2023"),
    },
    "🛒  Shopping & Finance": {
        "Amazon / Flipkart showed me a personalised price": ("monetizer", 3, "showed you a personalised price — different from your friend's"),
        "Swiggy / Zomato sent a notification timed to my hunger window": ("monetizer", 2, "sent a push notification timed to your exact hunger window"),
        "A shopping app ranked sponsored products above rated ones": ("monetizer", 2, "ranked sponsored products above better-rated free listings"),
        "Google Search showed paid listings I couldn't distinguish from organic": ("monetizer", 2, "showed paid listings first — 65% of users can't tell them apart"),
        "An ad followed me across 3+ different apps today": ("monetizer", 3, "cross-app retargeting via advertising IDs — standard practice"),
        "A 'price drop' or 'only 2 left' alert pushed me to buy": ("monetizer", 2, "discount was likely manufactured — Consumer Affairs Ministry warned"),
        "UPI / PhonePe flagged a legitimate transaction as suspicious": ("invisible", 2, "flagged a legitimate transaction as suspicious without notice"),
        "I used BNPL (Simpl / LazyPay) — it assessed my credit silently": ("monetizer", 3, "AI assessed your creditworthiness without you applying"),
        "My banking app's fraud detection blocked something I intended": ("gatekeeper", 2, "blocked or flagged a payment you intended to make"),
    },
    "💼  Work & Productivity": {
        "Gmail spam filter moved a legitimate email to junk": ("gatekeeper", 2, "moved a legitimate email to junk — no human reviewed it"),
        "Google Docs / Drive scanned my documents for AI training": ("invisible", 2, "scanned your documents for AI training — ToS updated 2023"),
        "An ATS bot screened my job application before a human saw it": ("gatekeeper", 3, "was rejected in 11 seconds by ATS — 75% are, before a human reads them"),
        "Autocorrect changed a word in a message I sent": ("optimizer", 2, "changed a word in a message you sent — 1 in 14 messages affected"),
        "A chatbot handled my support query (correctly or not)": ("optimizer", 2, "resolved — or misresolved — your query with no human involved"),
        "Background noise suppression changed how I sounded on a call": ("optimizer", 1, "background noise suppression AI altered how you sounded"),
        "I used an AI writing tool (ChatGPT / Gemini / Claude)": ("optimizer", 2, "shaped the structure and language of your written output"),
        "Google autocomplete filled my search from 4 characters": ("monetizer", 2, "weighted toward high-monetisation queries"),
    },
    "🎓  Education & Information": {
        "YouTube auto-captions gave me wrong information while studying": ("optimizer", 1, "4–12% word error rate for non-native accents — wrong notes possible"),
        "I read a product or restaurant review that turned out to be AI-generated": ("monetizer", 2, "MIT 2023: AI-generated reviews indistinguishable in 52% of cases"),
        "A content filter blocked something I was legitimately trying to access": ("gatekeeper", 3, "pattern-matched and blocked — no human reviewed your specific case"),
        "A university / college portal chatbot gave me wrong information": ("optimizer", 2, "hallucinated from old data — LLM institutional chatbot problem"),
        "Google Maps gave me a wrong wait time or travel estimate": ("optimizer", 1, "aggregated location data — accuracy limitations documented"),
        "I read a news article that was AI-summarised or framed": ("engager", 2, "framing and emphasis were algorithmically chosen"),
    },
    "🌙  Evening & Night": {
        "Netflix / Hotstar autoplay chose my next episode without asking": ("engager", 3, "autoplay and recommendation removed your ability to choose what's next"),
        "Spotify / Gaana inferred my mood and chose my playlist": ("engager", 2, "Daily Mix inferred your mood — you didn't choose the playlist"),
        "A subscription cancellation required multiple steps to complete": ("monetizer", 3, "7 taps and a phone call — FTC-documented dark pattern"),
        "A fitness or health app collected data from me overnight": ("invisible", 3, "sleep data collected, anonymised, and sold — $1.5B market"),
        "A voice assistant (Siri / Alexa / Google) is always listening": ("invisible", 3, "accidental activation documented — private conversations recorded"),
        "My location services are always on for apps that don't need it": ("invisible", 3, "location sold to retail analytics — NYT investigation 2019"),
        "My phone screen switched to Night Mode automatically": ("optimizer", 1, "time-of-day inference — you didn't set it"),
        "A wellbeing or screen time app reported my behavior back to me": ("gatekeeper", 1, "monitored your behaviour and reported back to you"),
    },
}

HABIT_QUESTIONS = {
    "I check my phone within 5 minutes of waking up":                           "engager",
    "I've bought something within 24 hours of seeing an ad for it":              "monetizer",
    "I've had a legitimate post, message, or transaction auto-blocked":          "gatekeeper",
    "My location is always on — even for apps that don't need it":               "invisible",
    "I use autocomplete or AI-suggested replies in messages":                    "optimizer",
    "I've accepted terms & conditions without reading them":                     "invisible",
    "I feel anxious or restless when I haven't checked my phone for a while":    "engager",
    "I use a fitness tracker or sleep monitor":                                  "optimizer",
    "I've been shown a 'price drop' or 'only 2 left' alert that pushed me to buy": "monetizer",
    "I've been rejected by an automated system — job, loan, or content filter":  "gatekeeper",
}

PUPPETEER_DECISIONS = {
    "optimizer": [
        "Your alarm rang at the 'optimal' time — decided by a sleep algorithm, not you.",
        "Your keyboard predicted your next 3 words before you thought them.",
        "Google Maps rerouted you without asking — it just started talking.",
        "Your phone dimmed itself. You didn't ask it to.",
        "A chatbot resolved your query incorrectly — and auto-closed the ticket.",
    ],
    "monetizer": [
        "Swiggy sent you a push notification timed precisely to your hunger window.",
        "You saw a 40% discount. The original price was inflated 3 days ago.",
        "LinkedIn showed you a job posting. The recruiter paid to target you.",
        "The price you saw on Amazon was different from your friend's price.",
        "CRED rewarded you for paying bills. It made more from your data than your fees.",
    ],
    "engager": [
        "Instagram showed you outrage content as your 3rd post — anger drives 2.3x engagement.",
        "YouTube's autoplay kept you watching for 47 unplanned minutes.",
        "Your news feed opened with the most anxiety-inducing headline of the day.",
        "Spotify played a song you didn't choose, timed to your mood inferred from history.",
        "Every article you read today confirmed what you already believed.",
    ],
    "gatekeeper": [
        "A resume bot rejected your application in 11 seconds — no human saw it.",
        "Gmail moved a legitimate email to spam. You never knew it arrived.",
        "Your UPI flagged a legitimate transaction as suspicious.",
        "A content filter blocked a research paper you needed.",
        "Face ID locked you out of your own phone three times in direct sunlight.",
    ],
    "invisible": [
        "An app shared your health data with an insurer — buried in page 47 of the ToS.",
        "Your browser fingerprint was sold to a retail analytics company.",
        "A system inferred your creditworthiness before you applied for anything.",
        "Your typing speed was monitored to infer your mood.",
        "Sleep data was collected, anonymised, and sold while you slept.",
    ],
}

SCORE_BANDS = [
    (81, 100, "⚫  Deep Exposure",    "Almost every touchpoint in your day runs through a system with an agenda. You are deeply embedded in the machine."),
    (61,  80, "🔴  High Exposure",    "Your day is significantly shaped by AI systems — most of which you didn't explicitly choose."),
    (41,  60, "🟠  Moderate Exposure","AI systems are meaningfully woven into your daily routine. Several decisions are made before you open the app."),
    (21,  40, "🟡  Light Exposure",   "A moderate number of AI systems shape your day. The quiet ones are doing the most work precisely because you haven't noticed them."),
    (0,   20, "🟢  Minimal Exposure", "You interact with fewer AI-driven systems than most. Either you're deliberate about your digital life, or the significant ones are still invisible."),
]


def calculate_all_scores(all_apps, selected_behaviors, selected_habits):
    scores = {k: 0 for k in PUPPETEERS}
    for app in all_apps:
        p = APP_MAP.get(app)
        if p:
            scores[p] += 2
    for section in BEHAVIORAL_DECISIONS.values():
        for label, (p_key, weight, _) in section.items():
            if label in selected_behaviors:
                scores[p_key] += weight
    for habit, p_key in HABIT_QUESTIONS.items():
        if habit in selected_habits:
            scores[p_key] += 3
    return scores


def calculate_app_only_scores(all_apps):
    scores = {k: 0 for k in PUPPETEERS}
    for app in all_apps:
        p = APP_MAP.get(app)
        if p:
            scores[p] += 2
    return scores


def calculate_puppet_score(scores):
    MAX_POSSIBLE = 194
    raw = sum(scores.values())
    return min(int((raw / MAX_POSSIBLE) * 100), 100)


def get_exposure_band(p_score):
    for lo, hi, label, desc in SCORE_BANDS:
        if lo <= p_score <= hi:
            return label, desc
    return SCORE_BANDS[-1][2], SCORE_BANDS[-1][3]


def get_top_decisions(selected_behaviors, dominant_key, n=5):
    hits = []
    for section in BEHAVIORAL_DECISIONS.values():
        for label, (p_key, weight, consequence) in section.items():
            if p_key == dominant_key and label in selected_behaviors:
                hits.append((weight, label, consequence))
    hits.sort(reverse=True)
    return hits[:n]


def radar1_app_exposure(app_scores):
    cats  = [PUPPETEERS[k]["label"].split(" ", 1)[1] for k in PUPPETEERS]
    vals  = [app_scores[k] for k in PUPPETEERS]
    r_max = max(vals) if max(vals) > 0 else 1
    norm  = [round((v / r_max) * 100) for v in vals]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=norm + [norm[0]], theta=cats + [cats[0]],
        fill="toself", fillcolor="rgba(74,144,217,0.15)",
        line=dict(color="#4A90D9", width=2.5), name="App Exposure",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100],
                            tickfont=dict(size=9, color="#555"),
                            gridcolor="rgba(255,255,255,0.07)"),
            angularaxis=dict(tickfont=dict(size=10),
                             gridcolor="rgba(255,255,255,0.07)"),
        ),
        showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=30, l=40, r=40), height=340,
    )
    return fig


def radar2_act2_bias():
    cats = [PUPPETEERS[k]["label"].split(" ", 1)[1] for k in PUPPETEERS]
    scores = []
    has_any = False

    for key in PUPPETEERS:
        response = st.session_state.get(f"response_{key}", "")
        if response and not response.startswith("Error:") and len(response.split()) > 5:
            word_count = len(response.split())
            score = min(int((word_count / 80) * 100), 100)
            has_any = True
        else:
            score = 0
        scores.append(score)

    topic = st.session_state.get("last_topic", "")

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]], theta=cats + [cats[0]],
        fill="toself", fillcolor="rgba(255,75,75,0.15)",
        line=dict(color="#FF4B4B", width=2.5), name="Persona Bias",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100],
                            tickfont=dict(size=9, color="#555"),
                            gridcolor="rgba(255,255,255,0.07)"),
            angularaxis=dict(tickfont=dict(size=10),
                             gridcolor="rgba(255,255,255,0.07)"),
        ),
        showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=30, l=40, r=40), height=340,
    )
    return fig, topic, has_any


def pie_chart(scores):
    labels = [PUPPETEERS[k]["label"] for k in PUPPETEERS if scores[k] > 0]
    values = [scores[k]              for k in PUPPETEERS if scores[k] > 0]
    colors = [PUPPETEERS[k]["color"] for k in PUPPETEERS if scores[k] > 0]

    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values,
        marker=dict(colors=colors, line=dict(color="#0f0f1a", width=2)),
        hole=0.45, textinfo="label+percent",
        textfont=dict(size=11, color="white"),
        hovertemplate="<b>%{label}</b><br>Score: %{value}<extra></extra>",
    )])
    fig.update_layout(
        title=dict(text="Who's Pulling Your Strings?", font=dict(size=15, color="white")),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"),
        showlegend=False, margin=dict(t=50, b=10, l=10, r=10), height=320,
    )
    return fig


@st.cache_resource
def get_groq_client():
    try:
        from groq import Groq
        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key:
            try:
                api_key = st.secrets["GROQ_API_KEY"]
            except Exception:
                pass
        if not api_key:
            return None
        return Groq(api_key=api_key)
    except Exception:
        return None


def generate_ai_report(all_apps, selected_behaviors, selected_habits, scores, dominant, client):
    dom_label = PUPPETEERS[dominant]["label"]
    app_list  = ", ".join(all_apps[:12]) if all_apps else "none provided"
    beh_count = len(selected_behaviors) + len(selected_habits)

    system_prompt = """You are an AI transparency analyst writing personalized reports about how AI systems quietly shape people's daily lives.

Style: second-person ("you", "your"). Honest. Specific. Never preachy. Slightly unsettling — not alarming. Treat the reader as intelligent.

Write exactly 3 short paragraphs, no headers:
1. Their dominant puppeteer — what it is, what it specifically wants from them, and one concrete consequence in their life right now based on their apps.
2. One thing happening in their digital life they almost certainly have not noticed — make it specific to their actual app list.
3. One small action they could take this week if they wanted to — framed as an option, not a lecture.

Total: under 220 words. Be specific. Make it feel written for this person personally."""

    user_prompt = (
        f"Their daily apps: {app_list}\n"
        f"Behaviors confirmed: {beh_count} out of maximum possible\n"
        f"Puppeteer scores — Optimizer: {scores['optimizer']}, Monetizer: {scores['monetizer']}, "
        f"Engager: {scores['engager']}, Gatekeeper: {scores['gatekeeper']}, Invisible: {scores['invisible']}\n"
        f"Dominant puppeteer: {dom_label}\n\n"
        f"Write their personalized Puppet Profile report."
    )

    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            max_tokens=380, temperature=0.88,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Report unavailable: {str(e)[:100]}"


# ══════════════════════════════════════════════════════════════════════════════
# NOTION LOGGING FUNCTION
# ══════════════════════════════════════════════════════════════════════════════

def _get_notion_creds():
    """Retrieve Notion token and personal report DB ID from env or Streamlit secrets."""
    token = os.environ.get("NOTION_TOKEN") or ""
    db_id = os.environ.get("NOTION_PERSONAL_REPORT_DB_ID") or ""
    try:
        if not token:
            token = st.secrets.get("NOTION_TOKEN", "")
        if not db_id:
            db_id = st.secrets.get("NOTION_PERSONAL_REPORT_DB_ID", "")
    except Exception:
        pass
    # Notion API requires the raw 32-char ID without dashes
    db_id = db_id.replace("-", "")
    return token, db_id


def _fetch_db_properties(token, db_id):
    """Return the set of property names that exist in the Notion database."""
    try:
        resp = requests.get(
            f"https://api.notion.com/v1/databases/{db_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "Notion-Version": "2022-06-28",
            },
            timeout=10,
        )
        if resp.status_code == 200:
            return set(resp.json().get("properties", {}).keys())
    except Exception:
        pass
    return set()


def log_personal_report(scores, dominant, p_score, band_label, all_apps, ai_report, topic):
    """Log a personal report entry to the Notion database.

    Fetches the live DB schema first so the payload only includes
    properties that actually exist — no more validation_error 400s
    when the database columns differ from what the code expects.
    """
    token, db_id = _get_notion_creds()
    if not token or not db_id:
        return  # Credentials not configured — fail silently

    now       = datetime.utcnow().isoformat()
    dom_label = PUPPETEERS[dominant]["label"]
    puppeteers_text = ", ".join(
        f"{PUPPETEERS[k]['label']}: {v}" for k, v in scores.items()
    )
    report_text = (ai_report or "")[:1900]

    # Full set of properties the code knows how to send
    all_props = {
        "Session": {
            "title": [{"text": {"content": f"Report — {now[:19]}"}}]
        },
        "Apps Selected": {
            "number": len(all_apps)
        },
        "Dominant Puppeteer": {
            "rich_text": [{"text": {"content": dom_label}}]
        },
        "Exposure Band": {
            "rich_text": [{"text": {"content": band_label}}]
        },
        "Puppet Score": {
            "number": int(p_score)
        },
        "Puppeteers Analyzed": {
            "rich_text": [{"text": {"content": puppeteers_text}}]
        },
        "Report Summary": {
            "rich_text": [{"text": {"content": report_text or "—"}}]
        },
        "Timestamp": {
            "date": {"start": now}
        },
        "Topic Explored": {
            "rich_text": [{"text": {"content": str(topic) if topic else "—"}}]
        },
    }

    # Only send properties that exist in the actual database
    existing = _fetch_db_properties(token, db_id)
    if existing:
        filtered_props = {k: v for k, v in all_props.items() if k in existing}
    else:
        # If schema fetch failed, send everything and let Notion surface any error
        filtered_props = all_props

    payload = {"parent": {"database_id": db_id}, "properties": filtered_props}

    try:
        requests.post(
            "https://api.notion.com/v1/pages",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            },
            json=payload,
            timeout=15,
        )
    except Exception:
        pass  # Network errors are non-fatal — the user experience continues


def show_nav(position="top"):
    col_back, _, col_fwd = st.columns([1, 5, 1])
    with col_back:
        if st.button("← Act 2", use_container_width=True, key=f"act3_back_{position}"):
            st.session_state.current_act = "act2"
            st.rerun()
    with col_fwd:
        if st.button("Closing →", use_container_width=True, key=f"act3_fwd_{position}"):
            st.session_state.current_act = "closing"
            st.rerun()


def show_form():
    show_nav("top")
    st.divider()

    st.markdown(
        "<h1 style='margin-bottom:0;'>Act 3 — My Personal Report</h1>",
        unsafe_allow_html=True
    )
    st.caption("Rahul's day was a story. Yours is real.")

    st.markdown("""
You've seen 47 AI decisions made about Rahul. You've watched the same AI respond through five different engineered agendas.

**Now map your own life.**

Select the apps you use and confirm the decisions that happen to you. PUPPET will identify which puppeteers are most active in your life, generate your Puppet Score, and produce a personalised analysis of your digital footprint.

*Nothing you enter here is stored beyond this session.*
""")
    st.divider()

    st.subheader("Step 1 — Your Apps")
    st.caption("Select every app you use at least once a week.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Social & Entertainment**")
        social = st.multiselect("s", label_visibility="collapsed",
            options=["Instagram","YouTube","Facebook","Twitter / X","Snapchat",
                     "ShareChat / Moj / Josh","Spotify / JioSaavn / Gaana",
                     "Netflix / Hotstar / Prime Video","Reddit",
                     "LinkedIn (Feed / Notifications)"],
            key="a3_social")
        st.markdown("**Shopping & Finance**")
        shopping = st.multiselect("sh", label_visibility="collapsed",
            options=["Amazon / Flipkart","Swiggy / Zomato","Myntra / Meesho / AJIO",
                     "CRED","Groww / Zerodha / Upstox","Ola / Uber / Rapido",
                     "Blinkit / Zepto / Dunzo","MakeMyTrip / Goibibo"],
            key="a3_shopping")
    with c2:
        st.markdown("**Navigation & Productivity**")
        nav = st.multiselect("n", label_visibility="collapsed",
            options=["Google Maps","Gboard / SwiftKey Keyboard",
                     "Sleep Tracker / Alarm App","Samsung Health / Fitbit",
                     "Google Assistant / Siri","Calendar / Reminders App",
                     "Autocorrect / Predictive Text"],
            key="a3_nav")
        st.markdown("**Work, Study & Communication**")
        work = st.multiselect("w", label_visibility="collapsed",
            options=["Gmail / Email App","WhatsApp","Telegram",
                     "Banking / UPI Apps","College / Office Portal",
                     "LinkedIn Jobs","Job Portals (Naukri / Indeed)",
                     "Aadhaar / DigiLocker","News Apps (Inshorts / TOI / NDTV)",
                     "Weather Apps","Chrome / Safari Browser",
                     "Phone's Default / Pre-installed Apps",
                     "Any App You Didn't Consciously Choose"],
            key="a3_work")

    all_apps = social + shopping + nav + work
    st.divider()

    st.subheader("Step 2 — Your Day's Decisions")
    st.caption("Check every statement that happened to you — even occasionally. Occasional use still means the system ran on you.")

    selected_behaviors = []
    for section_title, items in BEHAVIORAL_DECISIONS.items():
        st.markdown(f"**{section_title}**")
        col1, col2 = st.columns(2)
        item_list = list(items.keys())
        for idx, label in enumerate(item_list):
            col = col1 if idx % 2 == 0 else col2
            safe_key = f"bd__{label[:55]}"
            with col:
                if st.checkbox(label, key=safe_key):
                    selected_behaviors.append(label)
        st.markdown("")

    st.divider()

    st.subheader("Step 3 — Your Habits")
    st.caption("Check every statement that is consistently true for you.")

    selected_habits = []
    hq1, hq2 = st.columns(2)
    habit_list = list(HABIT_QUESTIONS.keys())
    for idx, habit in enumerate(habit_list):
        col = hq1 if idx % 2 == 0 else hq2
        with col:
            if st.checkbox(habit, key=f"hq__{idx}"):
                selected_habits.append(habit)

    st.divider()

    st.markdown("**Anything else you use regularly? (optional)**")
    extra = st.text_input(
        "Other apps:",
        placeholder="e.g. CRED, Duolingo, Ola, MakeMyTrip, ChatGPT...",
        key="a3_extra_input",
        label_visibility="collapsed",
    )

    st.divider()

    n_apps = len(all_apps)
    ready  = n_apps >= 3
    if not ready:
        st.caption("*Select at least 3 apps to generate your personal report.*")

    if st.button("Generate My Personal Report →", type="primary",
                 disabled=not ready, use_container_width=False):
        scores   = calculate_all_scores(all_apps, selected_behaviors, selected_habits)
        dominant = max(scores, key=scores.get)
        p_score  = calculate_puppet_score(scores)
        band_label, band_desc = get_exposure_band(p_score)

        st.session_state.update({
            "act3_scores":         scores,
            "act3_app_scores":     calculate_app_only_scores(all_apps),
            "act3_dominant":       dominant,
            "act3_apps":           all_apps,
            "act3_behaviors":      selected_behaviors,
            "act3_habits":         selected_habits,
            "act3_extra":          extra,
            "act3_puppet_score":   p_score,
            "act3_band_label":     band_label,
            "act3_band_desc":      band_desc,
            "act3_report":         None,
            "act3_logged":         False,
            "act3_results_ready":  True,
        })
        st.rerun()

    show_nav("bottom")


def show_results():
    scores     = st.session_state["act3_scores"]
    app_scores = st.session_state["act3_app_scores"]
    dominant   = st.session_state["act3_dominant"]
    all_apps   = st.session_state["act3_apps"]
    behaviors  = st.session_state["act3_behaviors"]
    habits     = st.session_state["act3_habits"]
    p_score    = st.session_state["act3_puppet_score"]
    band_label = st.session_state["act3_band_label"]
    band_desc  = st.session_state["act3_band_desc"]
    dom_p      = PUPPETEERS[dominant]
    total      = sum(scores.values()) or 1

    if st.session_state.get("act3_report") is None:
        client = get_groq_client()
        if client:
            with st.spinner("Generating your personal analysis..."):
                report = generate_ai_report(
                    all_apps, behaviors, habits, scores, dominant, client
                )
                st.session_state["act3_report"] = report
        else:
            st.session_state["act3_report"] = ""

    ai_report = st.session_state.get("act3_report", "")
    topic_from_act2 = st.session_state.get("last_topic", "")

    if not st.session_state.get("act3_logged", False):
        log_personal_report(
            scores=scores, dominant=dominant, p_score=p_score,
            band_label=band_label, all_apps=all_apps,
            ai_report=ai_report, topic=topic_from_act2
        )
        st.session_state["act3_logged"] = True

    col_back, _, col_fwd = st.columns([1, 5, 1])
    with col_back:
        if st.button("← Redo my report", use_container_width=True, key="act3_redo"):
            for k in ["act3_scores","act3_app_scores","act3_dominant","act3_apps",
                      "act3_behaviors","act3_habits","act3_extra","act3_puppet_score",
                      "act3_band_label","act3_band_desc","act3_report",
                      "act3_logged","act3_results_ready"]:
                st.session_state.pop(k, None)
            st.rerun()
    with col_fwd:
        if st.button("Final Question →", use_container_width=True, type="primary", key="act3_to_closing"):
            st.session_state.current_act = "closing"
            st.rerun()

    st.divider()
    st.markdown("<h2 style='margin-bottom:0;'>Your Personal Report</h2>", unsafe_allow_html=True)
    st.caption(f"Analysed from {len(all_apps)} apps · {len(behaviors)} behavioral decisions · {len(habits)} confirmed habits")
    st.divider()

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
            border: 2px solid {dom_p['color']};
            border-radius: 14px;
            padding: 1.8rem 2rem;
            margin: 0.5rem 0 1.5rem 0;
            box-shadow: 0 0 40px {dom_p['color']}22;
        ">
            <div style="font-size: 0.85rem; color: #666; letter-spacing: 1px; text-transform: uppercase;">
                Your dominant puppeteer
            </div>
            <div style="font-size: 2.2rem; font-weight: 900; color: {dom_p['color']}; margin: 0.4rem 0;">
                {dom_p['label']}
            </div>
            <div style="font-size: 1rem; color: #aaa; line-height: 1.6; margin-top: 0.5rem;">
                {PUPPETEER_SUMMARY[dominant]}
            </div>
            <div style="margin-top: 1.1rem; font-size: 0.9rem; color: #777; font-style: italic; line-height: 1.6;">
                {DOMINANT_CONSEQUENCES[dominant]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    score_color = "#FF4B4B" if p_score >= 70 else "#FF8C42" if p_score >= 45 else "#4CAF50"
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:1.4rem;
            background:#0f0f1a; border-radius:12px; padding:1.1rem 1.5rem;
            margin-bottom:0.5rem; border:1px solid #1e1e1e;">
            <div style="font-size:3.2rem; font-weight:900; color:{score_color}; line-height:1;">
                {p_score}
            </div>
            <div>
                <div style="font-weight:700; font-size:1rem;">Puppet Score™</div>
                <div style="color:#888; font-size:0.88rem;">{band_label}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.info(band_desc)
    st.divider()

    st.markdown("### Your Puppeteer Profiles")
    r1, r2 = st.columns(2)

    with r1:
        st.markdown(
            "<div style='font-weight:600; font-size:0.9rem; color:#4A90D9; margin-bottom:4px;'>"
            "📊 Radar 1 — App Exposure by Puppeteer</div>"
            "<div style='font-size:0.78rem; color:#666; margin-bottom:8px;'>"
            "Which systems dominate your installed apps</div>",
            unsafe_allow_html=True
        )
        st.plotly_chart(radar1_app_exposure(app_scores), use_container_width=True)

    with r2:
        r2_fig, act2_topic, has_act2_data = radar2_act2_bias()
        if has_act2_data:
            label_text = f"📊 Radar 2 — Persona Bias in Act 2 Responses"
            sub_text   = f"Engagement intensity per puppeteer on topic: <em>\"{act2_topic}\"</em>"
        else:
            label_text = "📊 Radar 2 — Persona Bias in Act 2 Responses"
            sub_text   = "Run Act 2 with a topic to populate this radar"
        st.markdown(
            f"<div style='font-weight:600; font-size:0.9rem; color:#FF4B4B; margin-bottom:4px;'>"
            f"{label_text}</div>"
            f"<div style='font-size:0.78rem; color:#666; margin-bottom:8px;'>{sub_text}</div>",
            unsafe_allow_html=True
        )
        st.plotly_chart(r2_fig, use_container_width=True)

    st.divider()
    st.markdown("### Overall Distribution")
    pie_col, spacer = st.columns([2, 1])
    with pie_col:
        st.plotly_chart(pie_chart(scores), use_container_width=True)

    st.divider()
    st.markdown("### Exposure Breakdown — % of Your Total Score")
    for pk, pv in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        p   = PUPPETEERS[pk]
        pct = int((pv / total) * 100)
        st.markdown(
            f"""<div style="display:flex; align-items:center; margin:8px 0; gap:12px;">
                <div style="width:170px; font-size:0.82rem; color:{p['color']}; font-weight:600;">{p['label']}</div>
                <div style="flex:1; background:#1a1a1a; border-radius:4px; height:10px;">
                    <div style="width:{pct}%; background:{p['color']}; height:10px; border-radius:4px;"></div>
                </div>
                <div style="width:40px; font-size:0.8rem; color:#666; text-align:right;">{pct}%</div>
            </div>""",
            unsafe_allow_html=True
        )

    st.divider()
    st.markdown("### AI Decisions Most Likely Affecting Your Day")
    st.caption(f"Based on your dominant puppeteer — top decisions from **{dom_p['label']}** active in your life:")

    top_beh = get_top_decisions(behaviors, dominant, n=3)
    if top_beh:
        for i, (weight, label, consequence) in enumerate(top_beh, 1):
            st.markdown(
                f"<div style='background:#111; border-left:3px solid {dom_p['color']}; "
                f"padding:0.75rem 1rem; border-radius:0 8px 8px 0; margin:6px 0;'>"
                f"<div style='font-size:0.92rem; font-weight:600; color:#ddd;'>{i}. {label}</div>"
                f"<div style='font-size:0.8rem; color:#888; margin-top:3px; font-style:italic;'>→ {consequence}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
    else:
        for i, dec in enumerate(PUPPETEER_DECISIONS.get(dominant, [])[:3], 1):
            st.markdown(
                f"<div style='background:#111; border-left:3px solid {dom_p['color']}; "
                f"padding:0.75rem 1rem; border-radius:0 8px 8px 0; margin:6px 0;'>"
                f"<div style='font-size:0.92rem; color:#ccc;'>{i}. {dec}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.divider()
    st.markdown("### Your Personal Analysis")
    st.caption("Generated by the same AI technology this project is exposing.")

    if ai_report:
        paragraphs = ai_report.replace("\r\n", "\n").split("\n\n")
        report_html = "".join(
            f"<p style='margin-bottom:1rem;'>{p.replace(chr(10), '<br>')}</p>"
            for p in paragraphs if p.strip()
        )
        st.markdown(
            f"""<div style="
                background: linear-gradient(135deg, #0f0f1a, #1a1a2e);
                border: 1px solid {dom_p['color']}44;
                border-radius: 12px; padding: 1.6rem 1.8rem;
                line-height: 1.85; font-size: 1rem; color: #ddd;">
                {report_html}
            </div>""",
            unsafe_allow_html=True
        )
        st.caption(f"*This analysis was generated through the lens of AI — an AI given specific instructions. Just like every system that ran on you today.*")
    else:
        st.info(
            "⚙️ **Groq API key needed for the written analysis.**\n\n"
            "The charts and scores above are fully calculated. "
            "Add your GROQ_API_KEY to unlock the personalized written report."
        )

    st.divider()
    st.markdown("### Share Your Result")
    st.caption("Copy and post — or just keep it to yourself.")

    top2        = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:2]
    top2_labels = " + ".join(PUPPETEERS[k]["label"] for k, _ in top2)
    share_text  = (
        f"My Puppet Profile — Dominant puppeteer: {dom_p['label']}\n"
        f"Puppet Score: {p_score}/100  |  {band_label}\n"
        f"Top two systems in my life: {top2_labels}\n\n"
        f"See who's pulling your strings → https://puppet-ua.streamlit.app"
    )
    st.code(share_text, language=None)

    st.divider()
    st.markdown(
        """<div style="
            background: linear-gradient(135deg, #0f0f1a, #1a1a2e);
            border: 1px solid #A78BFA44; border-radius: 14px;
            padding: 1.6rem 2rem; text-align: center; margin: 0.5rem 0;">
            <div style="font-size: 1.2rem; font-weight: 800; margin-bottom: 0.5rem;">
                One question left.
            </div>
            <div style="color: #888; font-size: 0.95rem; line-height: 1.7;">
                You've seen Rahul's 47 decisions. You've watched AI respond through five agendas.<br>
                You've mapped your own life. Now answer the question you started with.
            </div>
        </div>""",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button(
            "Answer the final question →",
            use_container_width=True, type="primary", key="act3_to_closing_bottom"
        ):
            st.session_state.current_act = "closing"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """<div style="text-align:center; color:#555; font-style:italic; line-height:2;">
            Rahul didn't know his strings were being pulled.<br>
            Now you know yours.<br><br>
            <span style="font-size:0.85rem;">
                The question is still the same:<br>
                <strong style="color:#aaa;">Why aren't you one of the people writing the instructions?</strong>
            </span>
        </div>""",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)


def show_act3():
    if st.session_state.get("act3_results_ready", False):
        show_results()
    else:
        show_form()
