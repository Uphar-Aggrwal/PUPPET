# PUPPET — Architecture & Technical Decisions

> This document explains how PUPPET is structured, why each technical decision was made, and what tradeoffs were involved. Written as a PM-engineer hybrid document.

---

## System Overview

PUPPET is a single-app, multi-page Streamlit application. The user moves through four screens in sequence: Intro → Act 1 → Act 2 → Closing. All state is managed in `st.session_state`. No database. No backend server. No authentication.
```
User Browser
     │
     ▼
app.py  ──── reads st.session_state.page
     │
     ├──── "intro"    → renders intro screen, captures initial_opinion
     ├──── "act1"     → imports act1_autopilot.autopilot → show_act1()
     ├──── "act2"     → imports act2_signal.signal → show_act2()
     └──── "closing"  → imports assets.closing → show_closing()
```

---

## File Responsibilities

### `app.py`
- Entry point for Streamlit
- Loads `.env` via `python-dotenv` at the very top — before any module imports
- Reads `st.session_state.page` to route between screens
- Renders the intro screen directly (no separate module — it's short)
- Captures `initial_opinion` into session state before navigating to Act 1

### `act1_autopilot/autopilot.py`
- Loads `decisions.json` into a Pandas DataFrame
- Renders each decision as a timeline row
- Maintains a toggle dict in `st.session_state.toggles`
- When a toggle is switched off, triggers the pushback mechanic — a hardcoded response per puppeteer type that mimics how real systems argue against being disabled
- Navigation buttons use a `position` parameter to guarantee unique Streamlit widget keys

### `act1_autopilot/data/decisions.json`
- All 47 decisions as a structured JSON array
- Each entry has: `id`, `time`, `description`, `puppeteer`, `color`, `source`, `pushback_text`
- Sourced from real research — Facebook engagement leak, Jobscan ATS data, MIT AI review study, NPCI fraud detection, etc.

### `act2_signal/signal.py`
- Imports all 5 system prompts from `personas/prompts.py`
- Renders checkboxes for each persona
- Dynamic run button label reads live checkbox state: "Run all five →" / "Run 3 puppeteers →" etc.
- Calls Groq API for each selected persona — `llama-3.1-8b-instant` model
- Stores each response in `st.session_state[f"response_{key}"]` so it persists across reruns
- Modal pattern: clicking "Read →" sets `st.session_state.open_modal = key` and triggers `st.rerun()`. The top of `show_act2()` checks this and renders full-screen card view instead of the list view.

### `act2_signal/personas/prompts.py`
- The core intellectual content of the project
- 5 system prompts, each ~150–250 words
- Each prompt establishes a persona, an agenda, a communication style, and specific constraints on what to include or omit
- The Invisible One's prompt is intentionally sparse — no stated purpose, no constraints — to mirror how many real systems actually operate

### `assets/closing.py`
- Reads `st.session_state.initial_opinion` (set at intro)
- Re-asks the same question
- Compares answers and reveals whether the user's perspective shifted
- Ends with the project's core question: *who is writing the instructions?*

---

## Key Technical Decisions

### Decision 1: Streamlit over Flask/Django
**Why:** PUPPET is an experience, not a data application. Streamlit's reactive rendering model (full rerun on interaction) is a constraint that forces clean state management. Flask would have required a frontend layer that added complexity with no benefit. Streamlit Cloud also provides free deployment with zero configuration.

**Tradeoff:** Streamlit's rerun model means any variable not in `st.session_state` is lost on every interaction. This caused early bugs where API responses disappeared when the Read button was clicked. Solved by storing all responses in session state immediately after fetching.

### Decision 2: Groq API over OpenAI
**Why:** Groq provides free-tier inference on LLaMA 3.1 with response times under 2 seconds. For an interactive demo, latency is user experience. OpenAI's free tier is heavily rate-limited. Groq's free tier is sufficient for demonstration use.

**Tradeoff:** Groq's model options are narrower. `llama3-8b-8192` was the original model used — it was deprecated in March 2026. Updated to `llama-3.1-8b-instant`. Always check console.groq.com/docs/models for current supported models.

### Decision 3: Session State Modal Pattern (not JavaScript)
**Why:** Streamlit strips all `<script>` tags from `st.markdown()` calls. JavaScript modals are not possible inside Streamlit. The attempted approach (injecting JS via `unsafe_allow_html=True`) silently did nothing while the button click still triggered a Streamlit rerun, resetting the page.

**Solution:** `st.session_state.open_modal` acts as a modal flag. When "Read →" is clicked, the flag is set to the persona key and `st.rerun()` is called. At the top of `show_act2()`, if the flag is set, render the full-screen card view only — not the normal list view. Clicking "← Back" clears the flag and reruns again.

### Decision 4: Separate `__init__.py` in Every Package Folder
**Why:** Python does not treat a folder as an importable package unless it contains an `__init__.py` file. Without these files, `from act1_autopilot.autopilot import show_act1` raises `ModuleNotFoundError` even if the file physically exists. All `__init__.py` files in this project are empty — they exist solely to enable imports.

### Decision 5: `load_dotenv()` in Every File That Needs the Key
**Why:** `os.environ.get("GROQ_API_KEY")` only reads system environment variables. The `.env` file is not automatically loaded into the environment — it requires `from dotenv import load_dotenv` and `load_dotenv()` to be called explicitly. In Streamlit, each module file runs in its own scope. `load_dotenv()` must be called in `signal.py` directly — not just in `app.py` — because by the time `signal.py` runs, `app.py`'s scope has been re-executed in a new Streamlit rerun context.

### Decision 6: Unique Widget Keys via Position Parameter
**Why:** Streamlit requires every interactive widget (button, checkbox, etc.) to have a globally unique `key`. When `show_nav()` was called twice on the same page (top and bottom), both calls generated buttons with identical auto-generated keys, crashing with `StreamlitDuplicateElementId`. Solved by passing a `position` string ("top" / "bottom") into `show_nav()` and appending it to every widget key: `key=f"back_{position}"`.

---

## Streamlit Deployment Notes

When deploying to Streamlit Cloud:
- The `.env` file does not go to GitHub (protected by `.gitignore`)
- The API key is added via Streamlit Cloud's Secrets management: Settings → Secrets → add `GROQ_API_KEY = "your_key_here"`
- `load_dotenv()` still runs on Cloud (it finds no `.env` file, which is fine) — `os.environ.get()` reads the secret from the environment that Streamlit Cloud injects

---

## What This Project Demonstrates (PM Perspective)

1. **Prompt Engineering as Product Design** — The 5 system prompts are not technical artifacts. They are product decisions. Each one reflects a deliberate choice about what an AI system should optimise for.

2. **State Management Under Constraints** — Streamlit's rerun model forced a disciplined approach to state. Every piece of data that needs to persist across interactions lives in `st.session_state`. No exceptions.

3. **User Experience Over Feature Completeness** — The modal pattern, the pushback mechanic, the dynamic button label — each of these exists to serve a specific moment in the user's experience, not to demonstrate technical capability.

4. **Data as Narrative** — The 47 decisions in `decisions.json` are not just data. They are the story. Each one is sourced, India-relevant, and chosen to make the product's argument viscerally rather than statistically.