# PUPPET — Technical Architecture

**Version**: 2.0 (Act 3 Personal Report System)  
**Last Updated**: April 2026  
**Author**: Uphar Aggarwal

---

## System Overview

PUPPET is a four-act interactive experience built on Streamlit with LLM-powered persona generation (Groq API), dynamic data visualization (Plotly), and dual Notion database logging. The architecture prioritizes **zero-latency navigation**, **real-time AI inference**, and **seamless data persistence** across a mandatory linear flow.

**Core Design Constraint**: Users cannot skip acts. The psychological progression (Feel → Understand → Personalize → Reflect) is the product itself.

---

## Application Flow

### **Router Architecture** (`app.py`)

```python
Intro → Act 1 → Act 2 → Act 3 → Closing
```

**Session State Gating**:
- `current_act` — Tracks user position in flow
- `act1_completed` — Set when Act 1 → Act 2 transition occurs
- `act2_completed` — Set when Act 2 → Act 3 transition occurs
- `initial_opinion` — Captured in Intro, retrieved in Closing for perspective shift calculation

**Restart Mechanism**: `restart_triggered` flag clears all session state and resets to Intro.

---

## Act 1 — AUTOPILOT

**File**: `act1_autopilot/autopilot.py`  
**Data**: `act1_autopilot/data/decisions.json`

### **Purpose**

Present 47 real AI-driven decisions across Rahul's day. Each decision is source-attributed and tagged with one of five puppeteers. Users toggle decisions off, triggering manipulative AI pushback language.

### **Data Structure**

```json
{
  "id": "decision_001",
  "time": "6:47 AM",
  "event": "Alarm rang 13 minutes before your set time",
  "puppeteer": "optimizer",
  "detail": "Sleep tracking AI detected light sleep phase...",
  "source": "Samsung Health API documentation"
}
```

**Puppeteer Tags**:
- `optimizer` — 🔴 Red
- `monetizer` — 🟠 Orange
- `engager` — 🔵 Blue
- `gatekeeper` — 🟡 Yellow
- `invisible` — ⚫ Black

### **Toggle Mechanic**

**State Management**:
```python
st.session_state.toggled_decisions = set()  # Tracks which decisions user toggled off
```

**Pushback Language**: Each decision has a `pushback` message stored in JSON. When toggled, the message displays briefly with colour-coded styling matching the puppeteer.

**Live Counter**: Sidebar displays count of reclaimed decisions.

### **Navigation**

- **Back to Intro**: Allowed at any point
- **Forward to Act 2**: Sets `act1_completed = True`, routes to `current_act = "act2"`

---

## Act 2 — SIGNAL

**File**: `act2_signal/signal.py`  
**Prompts**: `act2_signal/personas/prompts.py`

### **Purpose**

Demonstrate how identical queries produce five different answers depending on the AI persona's system prompt. Users type a topic, five LLM calls execute simultaneously via Groq API, and an annotation layer reveals what each persona emphasized, buried, or emotionally amplified.

### **Persona Prompts**

Each persona has a distinct system prompt stored in `prompts.py`:

```python
OPTIMIZER_PROMPT = """
You are an AI optimizing for efficiency and speed.
Prioritize actionable steps. Remove friction.
Never mention trade-offs or downsides.
"""
```

**The Five Personas**:
1. **🔴 The Optimizer** — Efficiency-first, removes nuance
2. **🟠 The Monetizer** — Commercial bias, surfaces paid options
3. **🔵 The Engager** — Emotional amplification, clickbait framing
4. **🟡 The Gatekeeper** — Risk-averse, emphasizes compliance
5. **⚫ The Invisible One** — Vague, no stated agenda

### **LLM Integration**

**API**: Groq (LLaMA 3.1-8b-instant)  
**Rate Limiting**: None (free tier sufficient for MVP)  
**Error Handling**: Silent failure with fallback message

```python
try:
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={"model": "llama-3.1-8b-instant", "messages": [...]},
        timeout=15
    )
except Exception:
    return "AI response unavailable"
```

### **Annotation Layer**

**Comparison Matrix**: After all five responses load, a "Compare Responses" button reveals:
- What each persona **included** (unique keywords)
- What each persona **buried** (facts mentioned by others but omitted)
- **Emotional tone** (neutral / urgent / dismissive / optimistic)

**Implementation**: Keyword extraction via simple string matching (no NLP library required at MVP scale).

### **Navigation**

- **Back to Act 1**: Allowed
- **Forward to Act 3**: Sets `act2_completed = True`, routes to `current_act = "act3"`

---

## Act 3 — MY PERSONAL REPORT

**File**: `act3_mirror/mirror.py`

### **Purpose**

Generate a personalized Puppet Profile combining app selection, behavioral confirmations, and habit questions. Outputs: Puppet Score, two radar charts, pie chart, exposure band, and AI-written analysis.

### **Three-Step Input Flow**

#### **Step 1: App Selection**

Apps organized by category (Morning Routine, Social Media, Shopping, etc.). Each app pre-mapped to a puppeteer.

```python
APP_MAP = {
    "Instagram": "engager",
    "Swiggy": "monetizer",
    "Google Maps": "optimizer",
    "Gmail": "gatekeeper",
    "WhatsApp": "invisible"
}
```

User selects via multiselect dropdowns.

#### **Step 2: Behavioral Confirmations**

Time-of-day checkboxes confirming specific AI decisions (e.g., "Instagram showed Reels first thing in the morning").

#### **Step 3: Habit Questions**

Binary choices (e.g., "Do you check your phone within 10 minutes of waking up?").

### **Scoring Algorithm**

```python
puppet_score = (app_score * 0.5) + (behavior_score * 0.3) + (habit_score * 0.2)
```

Normalized to 0-100 scale.

**Exposure Bands**:
- Low Exposure (0-35)
- Medium Exposure (36-65)
- High Exposure (66-85)
- Critical Exposure (86-100)

### **Data Visualization**

**Radar Chart 1**: App-only scores per puppeteer  
**Radar Chart 2**: Combined (apps + behaviors + habits) scores per puppeteer  
**Pie Chart**: Puppeteer distribution by percentage

**Library**: Plotly (`plotly.graph_objects`)

### **AI-Generated Personal Analysis**

**Prompt Structure**:
```python
system_prompt = """
You are PUPPET's analyst. Write a 3-paragraph report analyzing this user's digital life.
Paragraph 1: Dominant pattern
Paragraph 2: Specific risks
Paragraph 3: Reframe (no judgment, just observation)
"""
```

**Model**: Groq (LLaMA 3.1-8b-instant)  
**Caching**: Stored in `st.session_state["act3_report"]` to prevent re-generation on page refresh.

### **Notion Logging**

**Database**: `NOTION_PERSONAL_REPORT_DB_ID`

**Properties Logged**:
- Session (Title) — Timestamp
- Apps Selected (Number)
- Dominant Puppeteer (Rich Text)
- Exposure Band (Rich Text)
- Puppet Score (Number)
- Puppeteers Analyzed (Rich Text) — Summary of dominant persona
- Report Summary (Rich Text) — First 1900 chars of AI report
- Timestamp (Date)
- Topic Explored (Rich Text) — Reserved for future use

**Logging Trigger**: Single call on "Generate Report" button click. Flagged in session state to prevent duplicate logs.

### **Navigation**

- **Back to Act 2**: Allowed before report generation
- **Forward to Closing**: Only after report generated. Routes to `current_act = "closing"`

---

## Closing — The Final Question

**File**: `assets/closing.py`

### **Purpose**

Re-ask the opening question. Reveal initial answer. Calculate perspective shift.

### **Flow**

1. Display: *"One last question."*
2. Show initial answer: *"You came in saying: [initial_opinion]"*
3. Radio button: *"Is AI good for humanity?"* (3 options)
4. Submit button → Log to Notion → Reveal perspective shift or absence

### **Notion Logging**

**Database**: `NOTION_DB_ID_V2`

**Properties Logged**:
- Session (Title) — Timestamp
- Initial Opinion (Rich Text)
- Final Opinion (Rich Text)
- Perspective Shifted (Checkbox)
- Personas Explored (Number) — Count from Act 2
- Topic Searched (Rich Text) — Last topic from Act 2

**Logging Trigger**: Single call on "See my result →" button. Flagged in session state with `result_logged`.

### **Perspective Shift Revelation**

**If shifted**:
> *You came in with one answer. You're leaving with another. That shift didn't happen by accident. It happened because you saw the mechanism.*

**If not shifted**:
> *Your answer didn't change. That's okay. The goal wasn't to change your mind. The goal was to show you that the question itself is incomplete.*

**Final Statement** (both cases):
> *AI is a mirror. It reflects exactly what the person who built it wanted it to reflect. The question was never 'Is AI good for humanity?' The real question is: Who is writing the instructions?*

---

## Session State Management

### **Critical State Variables**

| Variable | Type | Set By | Used By |
|----------|------|--------|---------|
| `current_act` | str | app.py | All modules |
| `initial_opinion` | str | Intro | Closing |
| `act1_completed` | bool | Act 1 | app.py router |
| `act2_completed` | bool | Act 2 | app.py router |
| `toggled_decisions` | set | Act 1 | Act 1 (counter) |
| `explored_personas` | list | Act 2 | Closing (logging) |
| `last_topic` | str | Act 2 | Closing (logging) |
| `act3_results_ready` | bool | Act 3 | Act 3 (form vs results toggle) |
| `act3_scores` | dict | Act 3 | Act 3 (visualization) |
| `act3_dominant` | str | Act 3 | Act 3 (exposure band) |
| `act3_puppet_score` | int | Act 3 | Act 3 (display) |
| `act3_report` | str | Act 3 | Act 3 (cached AI response) |
| `result_logged` | bool | Closing | Closing (prevent duplicate logs) |
| `show_result` | bool | Closing | Closing (perspective shift reveal) |

### **Restart Logic**

```python
if st.session_state.get("restart_triggered", False):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state["current_act"] = "intro"
    st.rerun()
```

Called at top of `app.py` before any routing.

---

## Database Schema

### **Database 1: Perspective Shift Logging**

**Environment Variable**: `NOTION_DB_ID_V2`

| Property | Type | Description |
|----------|------|-------------|
| Session | Title | Timestamp of completion |
| Initial Opinion | Rich Text | Opening answer |
| Final Opinion | Rich Text | Closing answer |
| Perspective Shifted | Checkbox | Boolean flag |
| Personas Explored | Number | Count of Act 2 queries |
| Topic Searched | Rich Text | Last Act 2 topic |

### **Database 2: Personal Report Logging**

**Environment Variable**: `NOTION_PERSONAL_REPORT_DB_ID`

| Property | Type | Description |
|----------|------|-------------|
| Session | Title | Timestamp of report generation |
| Apps Selected | Number | Count of selected apps |
| Dominant Puppeteer | Rich Text | Label (e.g., "🔴 The Optimizer") |
| Exposure Band | Rich Text | Classification (e.g., "High Exposure") |
| Puppet Score | Number | 0-100 normalized score |
| Puppeteers Analyzed | Rich Text | Summary text |
| Report Summary | Rich Text | First 1900 chars of AI report |
| Timestamp | Date | ISO timestamp |
| Topic Explored | Rich Text | Reserved field |

---

## Environment Configuration

### **Required Variables**

```env
GROQ_API_KEY=your_groq_api_key
NOTION_TOKEN=your_notion_integration_token
NOTION_DB_ID_V2=perspective_shift_database_id
NOTION_PERSONAL_REPORT_DB_ID=personal_report_database_id
```

### **Secrets Management**

**Local**: `.env` file (git-ignored)  
**Streamlit Cloud**: Configured via dashboard (Settings → Secrets)

---

## Deployment Architecture

### **Hosting**

**Platform**: Streamlit Cloud  
**URL**: `puppet-ua.streamlit.app`

### **CI/CD**

**Trigger**: Push to `main` branch on GitHub  
**Build**: Automatic via Streamlit Cloud  
**Secrets**: Injected at runtime from Streamlit secrets manager

### **Performance**

**Target Load Time**:
- Intro/Act 1/Act 2: <2s
- Act 3 (with LLM call): <8s
- Closing: <2s

**Bottlenecks**:
- Groq API latency (5 concurrent calls in Act 2)
- Plotly chart rendering (Act 3)

---

## Error Handling Strategy

### **LLM Failures**

**Groq API timeout**: Return fallback message, do not block user progress.

```python
try:
    response = requests.post(..., timeout=15)
except Exception:
    return "AI response unavailable. Your report will still generate."
```

### **Notion Failures**

**Logging failure**: Silent. Never block user experience.

```python
try:
    requests.post(notion_api_url, ...)
except Exception:
    pass  # Log internally if needed, but don't surface error
```

### **Session State Corruption**

**Restart button**: Always visible in sidebar. Clears all state and resets to Intro.

---

## Testing Strategy

### **Manual Test Cases**

1. **Full Flow**: Intro → Act 1 → Act 2 → Act 3 → Closing
2. **Back Navigation**: Test all backward transitions
3. **Toggle Persistence**: Toggle decisions in Act 1, navigate back, verify state
4. **Perspective Shift**: Test all combinations (Yes→No, No→Yes, same answer)
5. **Act 3 Report**: Verify all charts render, AI text loads, Notion log fires
6. **Restart**: Click restart mid-flow, verify clean reset

### **Edge Cases**

- Act 2 with no topic entered (button disabled)
- Act 3 with no apps selected (validation message)
- Rapid clicking (debounce buttons)

---

## Future Technical Enhancements

### **Phase 2 (Planned)**

- **Multi-language Support**: Hindi/Hinglish UI
- **Export to PDF**: Generate shareable Puppet Profiles
- **Collaborative Sessions**: Multi-user mode with shared state
- **Advanced Analytics**: Cohort analysis dashboard in Notion

### **Phase 3 (Research)**

- **Voice Interaction**: Audio-first Act 2 (voice queries)
- **AR Integration**: Physical device visualization (Act 3)
- **Real-time Data**: Pull live usage stats from user's actual apps (via OAuth)

---

## Known Limitations

1. **No Authentication**: Users cannot save/resume sessions
2. **Single-session Storage**: Refresh clears all state
3. **Groq Free Tier**: Rate limits apply (not hit at current scale)
4. **No A/B Testing**: Single experience path (intentional)
5. **Desktop-optimized**: Mobile UI not fully responsive

---

## Development Notes

### **Code Style**

- **Naming**: Snake_case for variables, PascalCase for constants
- **Comments**: Inline only for non-obvious logic
- **Session State**: Always check existence before access (`st.session_state.get()`)

### **Dependencies**

```txt
streamlit>=1.41.0
plotly>=5.18.0
requests>=2.31.0
python-dotenv>=1.0.0
```

**Pinning Strategy**: Major version only (avoid breaking changes)

---

## Credits & References

**Design & Development**: Uphar Aggarwal  
**LLM Provider**: Groq (LLaMA 3.1-8b-instant)  
**Data Storage**: Notion API  
**Deployment**: Streamlit Cloud

**Research Sources**:
- Algorithm Watch (EU AI transparency research)
- Stanford Internet Observatory (Social media algorithm audits)
- Indian regulatory filings (RBI, NPCI disclosures)

---

## License

MIT License. See `LICENSE` file.

---

**Last Review**: April 2026  