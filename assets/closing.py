import streamlit as st
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


# ── Notion credentials ─────────────────────────────────────────────────────────
def get_creds():
    token = None
    db_id = None
    try:
        token = st.secrets["NOTION_TOKEN"]
    except Exception:
        token = os.environ.get("NOTION_TOKEN", "")
    try:
        db_id = st.secrets["NOTION_DB_ID_V2"]
    except Exception:
        db_id = os.environ.get("NOTION_DB_ID_V2", "203943c4d00e4aeba5eb1fc838c29f78")
    return token, db_id


# ── Notion logger — called exactly once per session from the button handler ────
def log_to_notion(initial, final, shifted, personas_explored, topic_searched):
    token, db_id = get_creds()
    if not token:
        return

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    now = datetime.utcnow().isoformat()

    final_map = {
        "Yes — AI is good": "Yes AI is good",
        "No — AI is harmful": "No AI is harmful",
        "Depends on who controls it": "Depends on who controls it",
    }
    final_option = final_map.get(final, "Depends on who controls it")
    shifted_option = "Yes changed" if shifted else "No stayed same"

    payload = {
        "parent": {"database_id": db_id},
        "properties": {
            "Session": {
                "title": [{"text": {"content": f"Session — {now[:19]}"}}]
            },
            "Initial Answer": {
                "rich_text": [{"text": {"content": str(initial) if initial else "Not sure"}}]
            },
            "Final Answer": {
                "select": {"name": final_option}
            },
            "Perspective Shifted": {
                "select": {"name": shifted_option}
            },
            "Timestamp": {
                "date": {"start": now}
            },
            "Personas Explored": {
                "number": int(personas_explored)
            },
            "Topic Searched": {
                "rich_text": [{"text": {"content": str(topic_searched) if topic_searched else "—"}}]
            }
        }
    }

    try:
        requests.post(url, headers=headers, json=payload, timeout=15)
    except Exception:
        pass  # Silent fail — never break the user experience


# ── Closing screen ─────────────────────────────────────────────────────────────
def show_closing():
    initial = st.session_state.get("initial_opinion", None)

    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>One last question.</h2>", unsafe_allow_html=True)

    if initial:
        st.markdown(
            f"<p style='text-align: center; color: gray;'>You came in saying: "
            f"<strong>{initial}</strong></p>",
            unsafe_allow_html=True
        )

    st.markdown("")

    final = st.radio(
        "Is AI good for humanity?",
        ["Yes — AI is good", "No — AI is harmful", "Depends on who controls it"],
        key="final_opinion"
    )

    st.markdown("")

    # ── Submit button — logs exactly once here, before rerun ──────────────────
    if st.button("See my result →", key="closing_submit"):
        final_val = final
        if not st.session_state.get("result_logged", False):
            shifted_val = (initial != final_val)
            explored    = st.session_state.get("explored_personas", [])
            topic       = st.session_state.get("last_topic", "")
            log_to_notion(
                initial=initial if initial else "Not sure",
                final=final_val,
                shifted=shifted_val,
                personas_explored=len(explored),
                topic_searched=topic
            )
            st.session_state["result_logged"] = True
        st.session_state["show_result"]  = True
        st.session_state["stored_final"] = final_val
        st.rerun()

    # ── Results ────────────────────────────────────────────────────────────────
    if st.session_state.get("show_result", False):
        final_stored = st.session_state.get("stored_final", final)
        shifted      = (initial != final_stored)

        st.markdown("---")

        if shifted:
            st.markdown(
                "<p style='text-align: center; color: #4CAF50; font-size: 20px;'>"
                "<strong>Your perspective shifted.</strong></p>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<p style='text-align: center;'>Before: {initial}<br>After: {final_stored}</p>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<p style='text-align: center; color: #FF8C42; font-size: 20px;'>"
                "<strong>Same answer. Different understanding.</strong></p>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<p style='text-align: center;'>You came in saying <strong>{initial}</strong>. "
                f"You're leaving the same way.<br>That's fine. The point was never to convert you.</p>",
                unsafe_allow_html=True
            )

        st.markdown("---")

        st.markdown("""
<div style='text-align: center; line-height: 2.2;'>
    <p style='font-size: 22px; font-weight: bold;'>The question was never <em>'Is AI good for humanity?'</em></p>
    <p style='color: gray;'>That question assumes AI is a single thing with a single answer.</p>
    <p style='color: gray;'>It isn't.</p>
    <p style='font-size: 18px;'>AI is a mirror.</p>
    <p style='color: gray;'>It reflects exactly what the person who built it wanted it to reflect.</p>
    <br>
    <p>🔴 The Optimizer reflects a world that values <strong>speed over deliberation.</strong></p>
    <p>🟠 The Monetizer reflects a world that values <strong>revenue over truth.</strong></p>
    <p>🔵 The Engager reflects a world that values <strong>attention over wellbeing.</strong></p>
    <p>🟡 The Gatekeeper reflects a world that values <strong>control over access.</strong></p>
    <p>⚫ The Invisible One reflects a world that values <strong>power over consent.</strong></p>
    <br>
    <p style='font-size: 20px; font-weight: bold;'>The real question is: <em>who is writing the instructions?</em></p>
    <p style='font-size: 18px; color: #A78BFA;'>And the more important question: <strong>why aren't you one of them?</strong></p>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("""
<div style='text-align: center; color: gray; font-style: italic; font-size: 15px;'>
    "Strings hain. Puppet bhi hai. Bas puppet dikhta hai — puppeteer nahi."
</div>
""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
<div style='text-align: center; font-size: 14px;'>
    Built by <strong>Uphar Aggarwal</strong> &nbsp;·&nbsp;
    <a href='https://github.com/Uphar-Aggrwal' target='_blank'>GitHub</a> &nbsp;·&nbsp;
    <a href='https://linkedin.com/in/uphar-aggarwal-9275103b6' target='_blank'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("↩ Start again", key="restart"):
            st.session_state["restart_triggered"] = True
            st.rerun()
