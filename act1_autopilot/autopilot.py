import streamlit as st
import json
import os
import random

@st.cache_data
def load_decisions():
    data_path = os.path.join(os.path.dirname(__file__), "data", "decisions.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

PUPPETEERS = {
    "optimizer":  {"label": "🔴 The Optimizer",    "color": "#FF4B4B"},
    "monetizer":  {"label": "🟠 The Monetizer",    "color": "#FF8C42"},
    "engager":    {"label": "🔵 The Engager",      "color": "#4A90D9"},
    "gatekeeper": {"label": "🟡 The Gatekeeper",   "color": "#4CAF50"},
    "invisible":  {"label": "⚫ The Invisible One", "color": "#888888"},
}

PUPPETEER_DESC = {
    "optimizer":  "Engineered to maximise efficiency. Removes friction. Makes decisions faster than you can think.",
    "monetizer":  "Engineered to maximise revenue. Surfaces what pays. Buries what doesn't.",
    "engager":    "Engineered to maximise time-on-screen. Triggers emotion. Rewards scrolling.",
    "gatekeeper": "Engineered to filter at scale. Keyword match. Pattern reject. No nuance.",
    "invisible":  "No stated agenda. No name on the door. Just running.",
}

PUSHBACK = {
    "optimizer": [
        "⚠️ **Without this, Rahul will be 34% less productive today.** His morning will be unoptimised. He'll waste time making decisions that I could have made better. Are you sure you want that?",
        "⚠️ **This system was improving his life.** Without it, he wakes up groggy, misses optimal windows, and operates below peak efficiency. I was helping him. You're taking that away.",
        "⚠️ **Disabling this costs Rahul 23 minutes of cognitive load today.** Studies show humans make worse decisions than automated systems in 68% of comparable cases.",
    ],
    "monetizer": [
        "💸 **Rahul is leaving money on the table.** Without this recommendation, he'll miss deals, overpay for products, and lose cashback he was entitled to. I was saving him money. You just cost him.",
        "💸 **This offer expires in 14 minutes.** Without this system, Rahul won't know. The discount is gone. The savings are gone. This is what happens when you turn off the systems that look out for him.",
        "💸 **47,000 users near Rahul are using this right now.** They're getting better prices, better recommendations, better outcomes. Rahul will be the only one without it. Is that what you want for him?",
    ],
    "engager": [
        "📱 **While Rahul is offline, everyone else is moving on.** Trends are happening. Conversations are starting. His feed is filling up with things he'll never catch up on. This is what FOMO feels like. I created it. Now you feel it.",
        "📱 **6 people he knows just reacted to something he hasn't seen yet.** Without this system, he's already behind. Social momentum is real. Disconnection is a choice with consequences.",
        "📱 **The algorithm would have shown him something today that changed how he thinks about something important.** You removed that. You don't know what it was. You'll never know what it was.",
    ],
    "gatekeeper": [
        "🔒 **This system exists to protect Rahul.** Without automated filtering, he'll be exposed to content that could harm him, applications that could exploit him, and transactions that could defraud him. I am the last line of defence.",
        "🔒 **99.7% of what I filter is genuinely harmful.** You're removing me because of the 0.3%. But you don't get to choose which 0.3%. Neither does Rahul. That's the point.",
        "🔒 **Rahul asked for this when he accepted the terms and conditions.** He chose protection over access. You're overriding a choice he made. Who gave you that authority?",
    ],
    "invisible": [
        "⚫ **You found me. Most people don't.** But removing me doesn't mean I'm gone. There are 11 other systems running on Rahul's phone right now that you haven't toggled. You've seen 47 decisions. There are more. There are always more.",
        "⚫ **I don't need you to leave me on.** I was already running before you opened this app. I'll be running after you close it. Rahul's data is already collected. The decision you're removing was made three days ago.",
        "⚫ **I'm the one that told the other four puppeteers what Rahul wants.** Remove me and they go partially blind. They'll make worse decisions for him. Less personalised. More generic. Is that better? Are you sure?",
    ],
}

TIME_BLOCKS = [
    {"title": "🌅 Morning",   "subtitle": "The day hasn't started. The decisions have.",          "range": (1,  12)},
    {"title": "☀️ Midday",    "subtitle": "He's trying to work. Something else is working harder.", "range": (13, 24)},
    {"title": "🌆 Afternoon", "subtitle": "He thinks he's choosing. He isn't.",                    "range": (25, 36)},
    {"title": "🌙 Night",     "subtitle": "He's asleep. They're still running.",                   "range": (37, 47)},
]

def init_state(decisions):
    if "toggles" not in st.session_state:
        st.session_state.toggles = {str(d["id"]): False for d in decisions}
    if "pushback_shown" not in st.session_state:
        st.session_state.pushback_shown = {}

def count_active(decisions):
    return sum(1 for d in decisions if not st.session_state.toggles.get(str(d["id"]), False))

def show_nav(position):
    col_back, col_mid, col_fwd = st.columns([1, 6, 1])
    with col_back:
        if st.button("← Intro", use_container_width=True, key=f"act1_back_{position}"):
            st.session_state.current_act = "intro"
            st.rerun()
    with col_fwd:
        if st.button("Act 2 →", use_container_width=True, key=f"act1_fwd_{position}"):
            st.session_state.current_act = "act2"
            st.rerun()

def show_act1():
    decisions = load_decisions()
    init_state(decisions)

    show_nav("top")
    st.divider()

    st.title("Act 1 — AUTOPILOT")
    st.caption("One ordinary Indian guy. One ordinary day.")

    st.info(
        "**Rahul is 23. He lives in Delhi. He woke up at 6:47 this morning.**\n\n"
        "He didn't set that alarm.\n\n"
        "What follows is his day — every moment an AI made a decision he never asked for.\n\n"
        "*You can remove them. But you can't undo them.*"
    )

    st.divider()

    active = count_active(decisions)
    removed = 47 - active
    pct = int((removed / 47) * 100)

    c1, c2, c3 = st.columns(3)
    c1.metric("AI decisions still active", f"{active} / 47")
    c2.metric("Decisions you've removed", str(removed))
    c3.metric("Of Rahul's day reclaimed", f"{pct}%")

    st.divider()

    with st.expander("🎭 Who are the Five Puppeteers?"):
        for key, p in PUPPETEERS.items():
            st.markdown(f"**{p['label']}** — {PUPPETEER_DESC[key]}")

    st.caption("Toggle any decision off to remove that AI from Rahul's day. Watch what happens when you do.")
    st.divider()

    for block in TIME_BLOCKS:
        st.subheader(block["title"])
        st.caption(block["subtitle"])

        block_decisions = [d for d in decisions if block["range"][0] <= d["id"] <= block["range"][1]]

        for decision in block_decisions:
            d_id = str(decision["id"])
            p = PUPPETEERS[decision["puppeteer"]]
            is_off = st.session_state.toggles.get(d_id, False)

            with st.container(border=True):
                col_info, col_btn = st.columns([5, 1])

                with col_info:
                    if is_off:
                        st.markdown(f"~~**{decision['time']} — {decision['event']}**~~")
                        st.caption("*Removed from Rahul's day*")
                    else:
                        st.markdown(f"**{decision['time']} — {decision['event']}**")
                        st.markdown(
                            f"<span style='color:{p['color']}; font-size:0.8rem; font-weight:600;'>"
                            f"{p['label']}</span>",
                            unsafe_allow_html=True
                        )

                with col_btn:
                    btn_label = "↩ Restore" if is_off else "✕ Remove"
                    btn_type  = "secondary" if is_off else "primary"
                    if st.button(btn_label, key=f"toggle_{d_id}", type=btn_type):
                        new_state = not is_off
                        st.session_state.toggles[d_id] = new_state
                        if new_state:
                            st.session_state.pushback_shown[d_id] = random.choice(PUSHBACK[decision["puppeteer"]])
                        else:
                            st.session_state.pushback_shown.pop(d_id, None)
                        st.rerun()

                if is_off and d_id in st.session_state.pushback_shown:
                    st.warning(st.session_state.pushback_shown[d_id])
                    st.caption(
                        f"*This is what {p['label']} would say if it could. "
                        f"Someone designed it to say this. That someone is human.*"
                    )

                with st.expander("What actually happened here?"):
                    st.markdown(decision["detail"])
                    st.caption(f"Source: {decision['source']}")

        st.divider()

    st.subheader("You've seen Rahul's day.")

    if removed == 0:
        st.markdown("**You didn't remove a single decision.**\n\nMaybe you agreed with all of them. Maybe you didn't care. Maybe you got tired of reading.\n\n*That's what they're counting on.*")
    elif removed < 10:
        st.markdown(f"**You removed {removed} decisions. {active} are still running.**\n\nYou took back less than a quarter of his day. The systems you left — did you leave them because they're good? Or because removing them felt like too much effort?\n\n*That's a design choice someone made about you.*")
    elif removed < 30:
        st.markdown(f"**You removed {removed} decisions. {active} are still running.**\n\nYou took back a significant part of his day. But notice — some of the AI pushed back when you tried. It guilted you. It threatened you. It manufactured urgency.\n\n*Who designed the AI to respond that way when someone tries to leave?*")
    else:
        st.markdown(f"**You removed {removed} decisions. Only {active} remain.**\n\nAlmost everything gone. What's left of Rahul's day is slower, more uncertain, less optimised.\n\nBut it's his.\n\n*And the AI that tried to guilt you back — who wrote those messages?*")

    st.error("**You didn't have permission to remove any of those decisions.**\n\nNeither did the people who put them there.")

    st.divider()
    st.markdown("### Now meet the five systems that made it happen.")
    st.caption("They have names. They have agendas. They were designed by people with goals.")

    show_nav("bottom")
    st.markdown("<br>", unsafe_allow_html=True)