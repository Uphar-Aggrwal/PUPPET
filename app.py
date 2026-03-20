import streamlit as st
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PUPPET — Who's Pulling The Strings?",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Session state init ──────────────────────────────────────────────────────────
if "current_act" not in st.session_state:
    st.session_state.current_act = "intro"

# ── Navigation ──────────────────────────────────────────────────────────────────
def go_to(act):
    st.session_state.current_act = act
    st.rerun()

# ── INTRO SCREEN ────────────────────────────────────────────────────────────────
def show_intro():
    # Centre everything using columns
    left, center, right = st.columns([1, 2, 1])
    with center:
        st.markdown(
            "<h1 style='text-align:center; font-size:3.5rem; font-weight:900;'>🎭 PUPPET</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align:center; color:#888; font-size:1.2rem; margin-top:-0.8rem;'>"
            "Who's Pulling The Strings?</p>",
            unsafe_allow_html=True
        )
        st.divider()
        st.markdown(
            "<p style='text-align:center; font-size:1.05rem;'>Before we begin — one question.</p>",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Is AI good for humanity?")
        opinion = st.radio(
            label="Your answer right now:",
            options=["Yes, definitely", "Mostly yes", "Not sure", "Mostly no", "No, definitely not"],
            index=2,
            key="opinion_widget"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Begin the experience →", use_container_width=True, type="primary"):
            st.session_state.stored_opinion = opinion
            go_to("act1")

# ── RENDER ───────────────────────────────────────────────────────────────────────
if st.session_state.current_act == "intro":
    show_intro()

elif st.session_state.current_act == "act1":
    from act1_autopilot.autopilot import show_act1
    show_act1()

elif st.session_state.current_act == "act2":
    from act2_signal.signal import show_act2
    show_act2()

elif st.session_state.current_act == "closing":
    from assets.closing import show_closing
    show_closing()