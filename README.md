# PUPPET — Who's Pulling The Strings?

> *A four-act interactive AI experience. One story. 47 invisible decisions. 5 puppeteers. Your personal report. One question that doesn't answer itself.*

**A Product Case Study in Behavioural Design**  
By Uphar Aggarwal

---

## Overview

PUPPET is a multi-act interactive experience that reveals how AI instructions — system prompts, trained personas, behavioural nudges — shape every digital interaction. Most users trust AI outputs as neutral facts. They are not neutral. They are designed outputs from designed systems, engineered to optimize for someone else's definition of value.

PUPPET does not argue this. It demonstrates it — interactively, personally, with real data from real Indian platforms and real AI decisions.

**Flow**: Opening Question → Act 1 → Act 2 → Act 3 → Final Question → Closing

---

## Why Does PUPPET Exist?

The question was never *"Is AI good for humanity?"* — that assumes AI is a single thing with a single answer. It isn't.

Every AI product you've ever used had invisible instructions written by someone you never met. The news feed that made you anxious. The resume screener that rejected you in 11 seconds. The recommendation engine that nudged you toward a paid result. None of these were neutral. All of them were designed — by someone, for a reason, with an agenda.

Most people know AI exists. Almost nobody understands that AI behaves exactly the way its prompt tells it to. The same model, the same question — five completely different answers, depending on who wrote the instructions.

**PUPPET makes this visible.** Not through a lecture. Through a story — one that starts with someone else's day, moves through the mechanism that controls it, turns the lens back onto your own life, and ends by asking a question that now carries real weight.

---

## The Experience

PUPPET is built on a single design principle: **make people feel a problem before you explain it**. Explanation without empathy produces intellectual acknowledgement. Empathy followed by explanation produces durable thinking change. The four-act structure is the argument — not an interface choice, but a deliberate psychological sequence.

### **Intro — Opening Question**

*"Is AI good for humanity?"*  
User answers. Answer is stored silently. The same question returns at the end.

### **Act 1 — AUTOPILOT** *(Feel it first)*

Meet Rahul. 47 real AI decisions across one ordinary day. Toggle decisions off. Watch AI push back with real manipulative language. A live counter tracks what you've reclaimed.

**The 47 Decisions** — Organized across Morning, Midday, Afternoon, and Night. Each decision sourced from real platform disclosures, investigative journalism, regulatory filings, and independent research. Every decision referencing Indian platforms has an Indian source.

**The Toggle Mechanic** — Click any decision to take it back. AI responds with real persuasive language — "Are you sure? You might miss important updates." The system fights back. A counter shows how many decisions you've reclaimed.

### **Act 2 — SIGNAL** *(Now understand why)*

The five colour tags from Act 1 are engineered AI personas. Type any topic. All five respond simultaneously via real LLM calls (Groq API, LLaMA 3.1-8b-instant). The same question, five completely different answers. An annotation layer reveals what changed — what each persona included, buried, or emotionally amplified.

**The Five Puppeteers**:
- 🔴 **The Optimizer** — Efficiency above all. Removes friction before you know it was there.
- 🟠 **The Monetizer** — You're not the user. You're the product.
- 🔵 **The Engager** — Designed to keep you on-screen as long as possible.
- 🟡 **The Gatekeeper** — Automated filtering at scale. No nuance, no context, no appeal.
- ⚫ **The Invisible One** — Running in the background. No stated purpose. You agreed when you accepted terms & conditions.

### **Act 3 — MY PERSONAL REPORT** *(Make it yours)*

Rahul's day was a story. Yours is real. Select your own apps from Indian and global platforms (Swiggy, Zomato, Instagram, Netflix, Gmail, Aadhaar, etc.). Confirm decisions that happen to you. Answer habit questions.

**PUPPET generates**:
- Full Puppet Score (0-100 normalized exposure index)
- Two radar charts (App-only analysis + Combined behavioral analysis)
- Pie chart (Puppeteer distribution)
- Exposure breakdown with band classification
- AI-written personal analysis (3-paragraph report via Groq LLM)

### **Closing — The Final Question**

*"Is AI good for humanity?"*  
Initial answer is shown. User answers again. Perspective shift — or absence of it — is revealed.

**The Perspective Shift Revelation**:
> *AI is a mirror. It reflects exactly what the person who built it wanted it to reflect. The question was never 'Is AI good for humanity?' The real question is: Who is writing the instructions?*

---

## Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | Streamlit 1.41.1 | Interactive UI framework |
| LLM Inference | Groq API (LLaMA 3.1-8b-instant) | Real-time persona responses (Act 2) + Personal analysis (Act 3) |
| Data Visualization | Plotly ≥5.18.0 | Radar charts, pie chart (Act 3) |
| Data Storage | Notion API (2022-06-28) | Two databases: perspective shift logging + personal report logging |
| Deployment | Streamlit Cloud | Cloud hosting with secrets management |

**Python 3.9+** | **requests** | **python-dotenv**

---

## Project Structure

```
PUPPET/
├── app.py                              ← Entry point with routing
├── act1_autopilot/
│   ├── autopilot.py                    ← 47 decisions + toggle mechanic
│   └── data/decisions.json             ← Source-attributed decision data
├── act2_signal/
│   ├── signal.py                       ← 5 persona simultaneous response
│   └── personas/prompts.py             ← Engineered persona prompts
├── act3_mirror/
│   └── mirror.py                       ← Merged personal report system
│                                         (app selection + habit analysis + AI report)
├── assets/
│   └── closing.py                      ← Final question + perspective shift
├── docs/
│   └── ARCHITECTURE.md                 ← Technical design decisions
├── requirements.txt
└── README.md
```

---

## Setup & Deployment

### **Local Development**

1. **Clone repository**
   ```bash
   git clone https://github.com/Uphar-Aggrwal/PUPPET.git
   cd PUPPET
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**  
   Create `.env` file with your API keys

4. **Run locally**
   ```bash
   streamlit run app.py
   ```

### **Streamlit Cloud Deployment**

1. Push to GitHub
2. Connect repository to Streamlit Cloud
3. Configure secrets in Streamlit Cloud dashboard
4. Deploy

**Live deployment**: **[https://puppet-ua.streamlit.app](https://puppet-ua.streamlit.app/)**
---

## Design Principles

### **1. Empathy Before Explanation**

Rahul's day (Act 1) is not instructional. It's emotional. Users feel the weight of invisible systems before they understand the mechanism. The toggle mechanic creates agency — and when AI fights back, that agency feels real.

### **2. Show, Don't Tell**

Act 2 does not lecture about prompt engineering. It demonstrates prompt engineering live. Five personas, one query, five completely different answers. The annotation layer shows the delta — what changed, what was buried, what was amplified.

### **3. Make It Personal**

Act 3 shifts from observation to self-examination. Mapping your own digital life — selecting your own apps, confirming your own decisions — creates cognitive friction that passive observation cannot.

### **4. The Question That Changes**

The opening question is identical to the final question. But the context has changed. The user has changed. That delta — whether they shifted or didn't — is the entire experience.

---

## Data Sources & Attribution

All 47 decisions in Act 1 are source-attributed. Indian platforms cite Indian research. Global platforms cite regulatory filings, investigative journalism, or company disclosures.

**Sample sources**:
- Reserve Bank of India (UPI fraud detection mechanisms)
- Google Transparency Reports (Search ranking signals)
- Meta's Algorithmic Ranking disclosures
- Independent research on Swiggy/Zomato recommendation systems
- LinkedIn job filtering patent filings

**Full bibliography**: See `act1_autopilot/data/decisions.json`

---

## Key Metrics

| Metric | Type | Description |
|--------|------|-------------|
| **Completion Rate** | Primary | Users who reach the final question |
| **Perspective Shift Rate** | Primary | Users who change their answer |
| **Act 3 Completion Rate** | Tertiary | Users who generate a full Puppet Profile |
| **Average Decisions Toggled** | Secondary | Proxy for engagement depth (Act 1) |
| **Topic Search Depth** | Secondary | Number of topics queried (Act 2) |

---

## The Compulsory Act 3 Decision

Act 3 (My Personal Report) sits between Act 2 and the Closing Screen. This is intentional. The perspective shift question only lands with full weight after the user has mapped their own digital life. Making Act 3 mandatory before the final question ensures users don't just observe Rahul's manipulation — they've confronted their own.

---

## Research Statement

PUPPET is a working prototype and a research artifact. All user interactions — perspective shift data, personal report mappings, topic queries — are logged with explicit user consent for the purpose of iterating on behavioural design patterns in AI transparency tools.

---

## Future Work

- **Regional Localization**: Hindi/Hinglish language support for Indian users
- **Platform-Specific Modules**: Deep dives into specific AI systems (e.g., "Instagram's Algorithm", "LinkedIn's Job Filter")
- **Collaborative Mode**: Multi-user sessions for workshops and classroom settings
- **Export & Share**: Generate shareable Puppet Profiles as images or PDFs

---

## Credits

**Design & Development**: Uphar Aggarwal  
**LLM Infrastructure**: Groq (LLaMA 3.1-8b-instant)  
**Data Storage**: Notion API  
**Hosting**: Streamlit Cloud

---

## License

This project is licensed under the MIT License. See `LICENSE` file for details.

**Citation**:  
If you use PUPPET in academic work, please cite:
```
Aggarwal, U. (2026). PUPPET: Who's Pulling The Strings? 
A Multi-Act Interactive Experience on AI Instructions and Behavioural Design.
https://github.com/Uphar-Aggrwal/PUPPET
```

---

## Contact

**Uphar Aggarwal**  
GitHub: [@Uphar-Aggrwal](https://github.com/Uphar-Aggrwal)  
LinkedIn: [Uphar Aggarwal](https://linkedin.com/in/uphar-aggarwal)  
Project: **[https://puppet-ua.streamlit.app](https://puppet-ua.streamlit.app/)**
---

*The question was never 'Is AI good for humanity?' The real question is: Who is writing the instructions?*