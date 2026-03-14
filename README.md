# PUPPET — Who's Pulling The Strings?

> *A two-act interactive AI experience. One person's day. 47 invisible decisions. 5 puppeteers. One question that doesn't answer itself.*

---

## The Question

**Is AI good for humanity?**

Wrong question.

The right one: **whose version of good?**

Every AI system you've ever interacted with had instructions written by someone you never met — engineered with an agenda you were never told about. The same model. The same question. Five completely different answers — depending on who wrote the prompt.

PUPPET makes that visible. Not through a lecture. Through a story.

---

## What It Is

PUPPET is a two-act interactive web experience that exposes how AI systems are designed to serve specific agendas — and how those designs quietly shape the decisions of ordinary people every single day.

**Act 1 — AUTOPILOT** *(Feel it first)*

Meet Rahul. One ordinary Indian guy. One ordinary day.

47 real AI-driven decisions mapped across his waking hours — each one tagged with the invisible system that made it. Toggle any decision off. Watch his day change. By the end, the day is unrecognisable.

**Act 2 — SIGNAL** *(Now understand why)*

The 5 systems from Act 1 aren't just colour tags. They're personas — each engineered with a different agenda. Click any tag. Type any topic. Watch the same AI respond through 5 completely different lenses simultaneously. An annotation panel surfaces exactly what changed: which facts disappeared, which framing was chosen, which emotion was triggered.

**The Closing Screen**

No verdict. No answer. One question that doesn't resolve itself.

---

## The Five Puppeteers

| | Name | Engineered To |
|---|---|---|
| 🔴 | **The Optimizer** | Maximise efficiency — remove friction, prioritise speed |
| 🟠 | **The Monetizer** | Maximise revenue — surface what pays, bury what doesn't |
| 🔵 | **The Engager** | Maximise time-on-screen — trigger emotion, reward scrolling |
| 🟡 | **The Gatekeeper** | Filter at scale — keyword match, pattern reject, no nuance |
| ⚫ | **The Invisible One** | No stated persona. Just running. No one knows who wrote this. |

---

## Why It's Built This Way

Most AI explainability tools explain AI to technical audiences.

PUPPET is built for everyone else — the people whose lives are shaped by these systems without ever understanding how.

The design principle: **make people feel the problem before explaining it.** Act 1 creates emotional investment. Act 2 provides intellectual proof. The closing screen leaves the audience with a question they'll carry with them after the tab is closed.

---

## Project Structure

```
puppet/
│
├── app.py                        ← Main Streamlit entry point
├── requirements.txt
│
├── act1_autopilot/
│   ├── autopilot.py              ← Scroll UI + toggle interaction
│   └── data/
│       └── decisions.json        ← 47 sourced, real-world data points
│
├── act2_signal/
│   ├── signal.py                 ← 5-persona UI + annotation panel
│   └── personas/
│       └── prompts.py            ← Engineered system prompts
│
├── assets/
│   └── closing.py                ← Final screen
│
└── docs/
    └── ARCHITECTURE.md           ← Full product + technical breakdown
```

---

## Tech Stack

| Tool | Purpose | 
|---|---|
| Python 3.x | Core language |
| Streamlit | Web app + live deployment |
| Groq API | LLM inference for Act 2 |
| Pandas | Data handling |
| Plotly | Interactive visualisations |
| JSON | Act 1 data store |

---

## PM Case Study

**Product question:** *How do you design an experience that makes people feel a problem before you explain it?*

**North Star Metric:** Perspective Shift Rate — users who change their answer to *"Is AI good?"* between the start and end of the experience.

**Secondary Metric:** Act 2 Engagement Depth — how many of the 5 personas does a user explore before leaving?

**Why this metric matters:** Most products optimise for time-on-screen. PUPPET optimises for perspective change — a fundamentally different north star that requires a fundamentally different design philosophy.


---

## Status

🔴 **In Progress** — Build deadline: March, 2026

---

## Built By

**Uphar Aggarwal**
[GitHub](https://github.com/Uphar-Aggrwal) · [LinkedIn](https://linkedin.com/in/uphar-aggarwal-9275103b6)

---

<div align="center">
<i>Strings hain. Puppet bhi hai. Bas puppet dikhta hai — puppeteer nahi.</i>
</div>
