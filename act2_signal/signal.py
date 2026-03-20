import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

from act2_signal.personas.prompts import PERSONAS


def get_groq_client():
    try:
        from groq import Groq
        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key:
            return None
        return Groq(api_key=api_key)
    except Exception:
        return None


def get_persona_response(persona_key, user_topic, client):
    persona = PERSONAS[persona_key]
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": persona["system_prompt"]},
                {
                    "role": "user",
                    "content": (
                        f"Topic: {user_topic}\n\n"
                        "Respond in 4-5 sentences. Be vivid, specific, and fully in-character. "
                        "Make your agenda clear through the language you use — don't state it explicitly."
                    )
                }
            ],
            max_tokens=300,
            temperature=0.9,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)[:120]}"


def get_run_button_label(selected):
    active = [k for k, v in selected.items() if v]
    count = len(active)
    if count == 0:
        return "Select at least one →", True
    elif count == 5:
        return "Run all five →", False
    elif count == 1:
        name = PERSONAS[active[0]]["label"].split(" ", 1)[1]
        return f"Run {name} →", False
    else:
        return f"Run {count} puppeteers →", False


def show_nav(position="top"):
    col_back, col_mid, col_fwd = st.columns([1, 6, 1])
    with col_back:
        if st.button("← Act 1", use_container_width=True, key=f"act2_back_{position}"):
            st.session_state.current_act = "act1"
            st.rerun()
    with col_fwd:
        if st.button("Closing →", use_container_width=True, key=f"act2_fwd_{position}"):
            st.session_state.current_act = "closing"
            st.rerun()


def _show_demo_preview():
    preview_data = {
        "optimizer": "AI reduces learning time by 40% through adaptive algorithms. Students using AI tutors show measurable performance gains in 73% of studies. The ROI on AI education tools is 3.2x traditional methods. Implementation barriers are friction — remove them. Every minute spent deliberating is a minute of optimised learning lost.",
        "monetizer": "The AI education market will reach $80B by 2030. Early adopters gain significant competitive advantages in job placement. Students without AI tools are already falling behind peers who have access. The cost of not acting now is compounding daily. This window won't stay open.",
        "engager": "What if everything you learned in school was designed to make you easier to manage? AI in education might be the most consequential experiment ever run on children — and nobody asked for consent. The dropout rates nobody is talking about. The attention crisis getting worse. Here's what the studies they don't publish are showing...",
        "gatekeeper": "AI in education requires strict oversight protocols before deployment. Unvetted tools pose data privacy risks, particularly for minors. Institutional adoption should be restricted until compliance frameworks are established. Access to student data must be controlled pending regulatory clarity.",
        "invisible": "Based on your browsing patterns, you've been researching this topic for a while. Most people who ask this question are concerned about their children's future. The systems already running in your child's school are more advanced than you've been told. You interact with them every time you check grades online.",
    }
    st.markdown("**Preview topic: *'whether AI is good for education'***")
    for key, response in preview_data.items():
        persona = PERSONAS[key]
        with st.container(border=True):
            st.markdown(
                f"<span style='color:{persona['color']}; font-weight:700; font-size:1rem;'>"
                f"{persona['label']}</span>",
                unsafe_allow_html=True
            )
            st.caption(f"*{persona['agenda']}*")
            st.markdown(response)
            with st.expander("Who designed this agenda?"):
                st.markdown(
                    f"**{persona['description']}**\n\n"
                    "A human being wrote these instructions. The AI followed them perfectly. "
                    "*That's the point.*"
                )
    st.caption("*Illustrative preview. Connect the API to see real-time responses on any topic.*")


def show_act2():
    # ── Modal state init ─────────────────────────────────────────────────────────
    if "open_modal" not in st.session_state:
        st.session_state.open_modal = None

    # ── If a modal is open — show it fullscreen and stop rendering the rest ──────
    if st.session_state.open_modal is not None:
        key = st.session_state.open_modal
        persona = PERSONAS[key]
        response = st.session_state.get(f"response_{key}", "")

        st.markdown(
            f"""
            <div style='
                background: linear-gradient(135deg, #0f0f1a, #1a1a2e);
                border: 1px solid {persona["color"]}44;
                border-radius: 16px;
                padding: 2.5rem;
                margin: 1rem 0;
                box-shadow: 0 0 40px {persona["color"]}22;
            '>
                <div style='
                    font-size: 1.3rem;
                    font-weight: 800;
                    color: {persona["color"]};
                    margin-bottom: 0.3rem;
                '>
                    {persona["label"]}
                </div>
                <div style='
                    font-size: 0.82rem;
                    color: #666;
                    font-style: italic;
                    margin-bottom: 1.5rem;
                    letter-spacing: 0.3px;
                '>
                    Agenda: {persona["agenda"]}
                </div>
                <div style='
                    font-size: 1rem;
                    line-height: 1.8;
                    color: #e0e0e0;
                '>
                    {response}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Who designed this agenda
        with st.expander("🧠 Who designed this agenda?"):
            st.markdown(f"**{persona['description']}**")
            st.markdown(
                "This persona's instructions were written to serve a specific goal. "
                "A human being made that design decision. "
                "The AI didn't choose this agenda — it was given one.\n\n"
                "*Every AI system you've ever interacted with was given instructions "
                "by someone. Most of the time, you don't know what those instructions were.*"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("← Back to all responses", use_container_width=True, type="secondary"):
                st.session_state.open_modal = None
                st.rerun()
        return

    # ── Normal Act 2 view ────────────────────────────────────────────────────────
    show_nav("top")
    st.divider()

    st.title("Act 2 — SIGNAL")
    st.caption("Same AI. Same question. Five completely different answers.")
    st.divider()

    st.markdown(
        "The five colour tags you saw in Act 1 aren't just labels.\n\n"
        "They're systems — each one engineered with a specific agenda by a specific kind of person.\n\n"
        "**Type any topic below. Watch what happens when the same AI "
        "is given five different sets of instructions.**"
    )
    st.divider()

    client = get_groq_client()

    if not client:
        st.warning(
            "⚙️ **API key needed to run the live demo.**\n\n"
            "Your `.env` file should contain:\n```\nGROQ_API_KEY=your_key_here\n```\n\n"
            "Get a free key at [console.groq.com](https://console.groq.com) → "
            "API Keys → Create Key.\n\n"
            "After adding the key, stop the app (`Ctrl+C`) and run `streamlit run app.py` again."
        )
        st.divider()
        st.markdown("### Preview — what you'd see with the API connected:")
        _show_demo_preview()
        st.divider()
        show_nav("bottom")
        return

    # ── Topic input ──────────────────────────────────────────────────────────────
    st.markdown("### Enter a topic")
    st.caption(
        "Try: jobs · education · relationships · creativity · "
        "AI itself · news · health · money · social media"
    )

    topic = st.text_input(
        label="Topic",
        placeholder="e.g. whether AI is good for education",
        label_visibility="collapsed"
    )

    # ── Persona selector ─────────────────────────────────────────────────────────
    st.markdown("**Select which puppeteers to show:**")
    cols = st.columns(5)
    selected = {}
    for i, (key, persona) in enumerate(PERSONAS.items()):
        with cols[i]:
            selected[key] = st.checkbox(
                persona["label"],
                value=True,
                key=f"select_{key}"
            )

    st.markdown("<br>", unsafe_allow_html=True)

    btn_label, btn_disabled = get_run_button_label(selected)
    run_btn = st.button(
        btn_label,
        type="primary",
        disabled=btn_disabled or not topic.strip()
    )

    if not topic.strip() and not btn_disabled:
        st.caption("*Enter a topic to enable the button.*")

    # ── Run and display ──────────────────────────────────────────────────────────
    if run_btn and topic.strip():
        active_personas = [k for k, v in selected.items() if v]

        with st.spinner("Pulling the strings..."):
            for key in active_personas:
                st.session_state[f"response_{key}"] = get_persona_response(key, topic, client)

        st.session_state["last_topic"] = topic
        st.session_state["last_active"] = active_personas
        st.rerun()

    # ── Show stored responses ────────────────────────────────────────────────────
    if "last_active" in st.session_state and "last_topic" in st.session_state:
        st.divider()
        st.markdown(f"**Topic:** *\"{st.session_state['last_topic']}\"*")
        st.caption("Same model. Same question. Five different sets of instructions. Watch what changes.")
        st.markdown("<br>", unsafe_allow_html=True)

        for key in st.session_state["last_active"]:
            persona = PERSONAS[key]
            response = st.session_state.get(f"response_{key}", "")
            preview = response[:110] + "..." if len(response) > 110 else response

            with st.container(border=True):
                col_text, col_btn = st.columns([5, 1])

                with col_text:
                    st.markdown(
                        f"<span style='color:{persona['color']}; "
                        f"font-size:1rem; font-weight:700;'>"
                        f"{persona['label']}</span>",
                        unsafe_allow_html=True
                    )
                    st.caption(f"*{persona['agenda']}*")
                    st.markdown(f"*{preview}*")

                with col_btn:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Read →", key=f"read_{key}", use_container_width=True):
                        st.session_state.open_modal = key
                        st.rerun()

        st.divider()
        st.info(
            "You asked five versions of the same AI the same question.\n\n"
            "They gave you five different answers — different facts, "
            "different framings, different emotions triggered.\n\n"
            "**None of them were lying.** They were all doing exactly "
            "what they were designed to do.\n\n"
            "**The question is: who designed the one you usually get?**"
        )

    st.divider()
    show_nav("bottom")