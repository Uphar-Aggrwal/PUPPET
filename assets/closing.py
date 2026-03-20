import streamlit as st

def show_closing():

    # ── Perspective shift check ─────────────────────────────────────────────────
    initial = st.session_state.get("stored_opinion", None)

    # ── Header ──────────────────────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.markdown("# The Final Question")
        st.divider()

        st.markdown(
            "You've seen Rahul's day.\n\n"
            "47 decisions. Zero consent.\n\n"
            "You've met the five systems that made it happen.\n\n"
            "You've watched the same AI say five completely different things "
            "based on who wrote its instructions.\n\n"
        )

        st.markdown("---")

        st.markdown(
            "### Is AI the problem?\n\n"
            "The Optimizer was designed by a product team chasing efficiency metrics.\n\n"
            "The Monetizer was approved by a board optimising for quarterly revenue.\n\n"
            "The Engager was built by engineers whose bonuses depended on time-on-screen.\n\n"
            "The Gatekeeper was written by a compliance team afraid of liability.\n\n"
            "The Invisible One was deployed by someone who preferred you didn't know it existed.\n\n"
        )

        st.error(
            "**Every system you encountered today was designed by a human being "
            "who made a deliberate choice about what it would optimise for.**\n\n"
            "The AI didn't choose its agenda.\n\n"
            "Someone else did."
        )

        st.markdown("---")

        # ── Perspective shift reveal ─────────────────────────────────────────────
        st.markdown("### Before you began, you said:")

        if initial:
            st.markdown(f"## *\"{initial}\"*")
        else:
            st.markdown("## *You skipped the opening question.*")
            st.caption("*(That's fine. The puppeteers noted it.)*")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### And now?")

        final_opinion = st.radio(
            label="Has your answer changed?",
            options=[
                "Yes, definitely",
                "Mostly yes",
                "Not sure",
                "Mostly no",
                "No, definitely not"
            ],
            index=2,
            key="final_opinion"
        )

        if initial and final_opinion:
            opinion_scale = {
                "Yes, definitely": 5,
                "Mostly yes": 4,
                "Not sure": 3,
                "Mostly no": 2,
                "No, definitely not": 1
            }
            initial_score = opinion_scale.get(initial, 3)
            final_score = opinion_scale.get(final_opinion, 3)
            delta = final_score - initial_score

            st.markdown("<br>", unsafe_allow_html=True)

            if delta > 1:
                st.success(
                    "**Your view shifted significantly toward AI being good.**\n\n"
                    "Interesting. The systems you just encountered were designed "
                    "to manipulate, surveil, monetise, and control. "
                    "And you came out more optimistic.\n\n"
                    "*What does that say about the strength of the case for AI — "
                    "or about what you're willing to accept?*"
                )
            elif delta == 1:
                st.info(
                    "**Your view shifted slightly toward AI being good.**\n\n"
                    "A small movement in the positive direction despite everything you saw. "
                    "Maybe the efficiency gains are worth the trade-offs. "
                    "Maybe you've already made your peace with it.\n\n"
                    "*Or maybe the framing of this experience was itself a kind of influence.*"
                )
            elif delta == 0:
                st.warning(
                    "**Your view didn't change.**\n\n"
                    "You walked through 47 invisible decisions, met five manipulative systems, "
                    "and watched the same AI become five different things — and you feel "
                    "exactly the same as when you started.\n\n"
                    "*Either your position is extremely well-considered. "
                    "Or the experience didn't reach you. "
                    "Both are worth sitting with.*"
                )
            elif delta == -1:
                st.info(
                    "**Your view shifted slightly toward AI being a problem.**\n\n"
                    "Something moved. You're not sure how much.\n\n"
                    "*The question isn't whether AI is good or bad. "
                    "It's whether you get to be part of deciding. Right now, mostly you don't.*"
                )
            else:
                st.error(
                    "**Your view shifted significantly toward AI being a problem.**\n\n"
                    "You came in with some openness and left with considerably less.\n\n"
                    "*That shift is data. The question is what you do with it.*"
                )

        st.markdown("---")

        # ── The real question ────────────────────────────────────────────────────
        st.markdown(
            "### The question was never *'Is AI good for humanity?'*\n\n"
            "That question assumes AI is a single thing with a single answer.\n\n"
            "It isn't.\n\n"
            "AI is a mirror.\n\n"
            "It reflects exactly what the person who built it wanted it to reflect.\n\n"
            "The Optimizer reflects a world that values speed over deliberation.\n\n"
            "The Monetizer reflects a world that values revenue over truth.\n\n"
            "The Engager reflects a world that values attention over wellbeing.\n\n"
            "The Gatekeeper reflects a world that values control over access.\n\n"
            "The Invisible One reflects a world that values power over consent.\n\n"
        )

        st.markdown(
            "> *\"Strings hain. Puppet bhi hai.*\n"
            "> *Bas puppet dikhta hai — puppeteer nahi.\"*"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            "The real question is: **who is writing the instructions?**\n\n"
            "And the more important question: **why aren't you one of them?**"
        )

        st.markdown("---")

        # ── Credits ──────────────────────────────────────────────────────────────
        st.caption("PUPPET — Who's Pulling The Strings?")
        st.caption("Built by Uphar Aggarwal · [GitHub](https://github.com/Uphar-Aggrwal) · [LinkedIn](https://linkedin.com/in/uphar-aggarwal-9275103b6)")
        st.caption("*All 47 decisions in Act 1 are real, sourced, and documented.*")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Restart ──────────────────────────────────────────────────────────────
        if st.button("↩ Start again", use_container_width=False):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)