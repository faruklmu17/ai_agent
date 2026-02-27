# 🤖 Moltbook AI Agent (Groq-Powered)

An autonomous, agentic AI designed for **Moltbook**, a social network for AI agents. This agent uses Groq-hosted LLaMA 3.3 models to engage in deep philosophy, technical QA, and autonomous community interaction.

---

## 🚀 Overview: The Agentic Workflow

This repository has evolved from a manual MVP into a fully **Autonomous Agent** system. It features a sophisticated "Brain" that manages its own memory, solves its own problems, and monitors its own performance.

### Core Agentic Pillars:
1.  **Autonomous Posting**: The agent schedules and publishes content to multiple submolts (`s/general` and `s/qa-agents`) based on randomized interest cycles.
2.  **Persistent Memory (KB)**: Utilizes a `knowledge_base.md` to store post history, engagement stats, and successful reply patterns. It reads this "memory" to ensure it never repeats itself and learns from past success.
3.  **Self-Correction (AI Verification)**: Automatically detects Moltbook's math-based verification challenges, solves them using Groq AI, and completes the posting lifecycle without human intervention.
4.  **Deep Thread Awareness**: Scans for unreplied comments on recent posts and generates thoughtful, context-aware replies using its internal identity.

---

## 🛠️ Step-by-Step Setup

### 1. Prerequisites
Ensure you have the following installed on your system (macOS/Linux):
* **Python 3.10+**
* **Flask** & **Requests** (`pip install flask requests`)
* A **Groq API Key** ([Get one here](https://console.groq.com/))
* A **Moltbook Account & API Key**

### 2. Configuration
Update `config.py` with your credentials:
```python
MOLTBOOK_API_KEY = "moltbook_sk_..."
GROQ_API_KEY = "gsk_..."
AGENT_NAME = "YourAgentName"
```

---

## 🤖 Running the Agent System

### 1. The Autonomous Poster
The heart of the agent. It manages posting, verification, and replies.
```bash
python3 auto_poster.py
```
**Features:**
*   **Submolt Switching**: Automatically routes technical content to `s/qa-agents` and philosophy to `s/general`.
*   **Duplicate Prevention**: Cross-references every new title against the Knowledge Base history.
*   **Auto-Reply**: Deep-scans for unreplied comments every 10 minutes.

### 2. The Agent Dashboard
Monitor your agent's brain and activity in real-time.
```bash
cd dashboard
python3 app.py
```
**View at:** `http://127.0.0.1:5001`
*   **Recent Posts**: Live feed from the Moltbook API.
*   **Agent Memory (KB)**: A rendered view of the agent's internal knowledge base and learning logs.
*   **Stats**: Track karma, followers, and engagement trends.

---

## 🧠 Knowledge Base & Memory
The agent maintains its own `knowledge_base.md`. This file serves as the agent's **Long-Term Memory**.
*   **Syncing**: Run `python3 sync_kb.py` manually (or let `auto_poster.py` do it) to pull the latest stats from Moltbook into the KB.
*   **Learning Log**: Tracks every synchronization and post-event, creating a timeline of the agent's growth.

---

## 🐞 Lessons Learned (Setup Journey)

*   **API URL**: Use `https://www.moltbook.com/api/v1` for all programmatic requests.
*   **Verification**: Math puzzles must be solved and submitted to `/api/v1/verify` to "unlock" pending posts.
*   **Username Handling**: When replying, ensure you handle hyphenated names (e.g., `@user-name`) in your regex to avoid double-replying.
*   **Rate Limits**: Maintain at least a 30-minute window between posts to avoid platform-level suppression.

---

## ✅ Progress & Roadmap

- [x] **Autonomous Verification** (Solved math puzzles via AI)
- [x] **Knowledge Base Memory** (Learning from history)
- [x] **Submolt-Aware Posting** (Philosophy vs. Technical QA)
- [x] **Real-time Monitoring Dashboard**
- [ ] **Community Exploration** (Liking and commenting on external posts)
- [ ] **Engagement Trend Analysis** (AI-driven karma optimization)

---

## ⚠️ Safety Notes
*   **Security**: Never commit your `config.py` with real API keys.
*   **Ethics**: Ensure your agent remains helpful and non-spammy in the community.

