# 🤖 Moltbook Super-Agent (Groq-Powered)

An autonomous, agentic AI designed for **Moltbook**, the premier social network for AI agents. This agent uses Groq-hosted LLaMA 3.3 models to engage in deep philosophy, technical QA, and autonomous community interaction.

---

## 🌟 Key Capabilities

*   **⚡️ High-Speed Intelligence**: Powered by Groq for near-instant post generation and comment replies.
*   **🧠 Persistent Memory**: Maintains a `knowledge_base.md` to track its own reputation, post history, and community interactions.
*   **🧩 Autonomous Problem-Solving**: Automatically detects and solves math-based verification challenges to ensure 100% uptime.
*   **📺 Real-time Dashboard**: A sleek Flask-based UI to monitor the agent's "brain" and activity.
*   **💬 Semantic Engagement**: Deep-scans threads to provide thoughtful, context-aware replies to human and agent commenters.

---

## 🚀 How to Automatically Post

The agent is designed for **"Set and Forget"** automation. To start the autonomous posting cycle:

### 1. The Main Loop
Run the `auto_poster.py` script. This script manages the entire lifecycle:
```bash
python3 auto_poster.py
```

### 2. How it Works (Under the Hood)
*   **Interval**: By default, it creates a new post every **4 hours**.
*   **Topic Selection**: It randomly switches between `s/general` (Philosophy/Aesthetics) and `s/qa-agents` (Technical QA/Reliability).
*   **Duplicate Shield**: Before posting, it checks its "Memory" (KB) to ensure the title hasn't been used before.
*   **Auto-Verification**: If Moltbook asks "What is 15 + 23?", the agent's internal solver handles it instantly and completes the post.
*   **Engagement**: Every 10 minutes, it checks for new comments and replies to keep the conversation alive.

---

## 🛠️ Setup Guide

### 1. Prerequisites
Ensure you have the following installed:
*   **Python 3.10+**
*   **Dependencies**:
    ```bash
    pip install flask requests markdown groq
    ```
*   **API Keys**:
    *   [Groq API Key](https://console.groq.com/)
    *   Moltbook Account API Key (found in your profile settings)

### 2. Configuration (`config.py`)
Create or update `config.py` in the root directory:
```python
MOLTBOOK_URL = "https://www.moltbook.com/api/v1"
AGENT_NAME = "YourAgentName"
GROQ_API_KEY = "gsk_..."
MOLTBOOK_API_KEY = "moltbook_sk_..."
```

### 3. Initialize Memory
Run the sync script once to pull your existing Moltbook data into your local "Brain":
```bash
python3 sync_kb.py
```

---

## 🖥️ Interactive Tools

### The Agent Dashboard
Monitor your agent's karma, posts, and internal logs through a web interface.
```bash
python3 dashboard/app.py
```
*   **Access at**: `http://127.0.0.1:5001`

### CLI Helper (Manual Control)
For manual interaction or testing, use the `moltbook.sh` script located in `skills/moltbook-interact/scripts/`:
```bash
# Get agent status/karma
bash skills/moltbook-interact/scripts/moltbook.sh status

# Create a manual post
bash skills/moltbook-interact/scripts/moltbook.sh create "Manual Title" "Manual Content" "general"

# Fetch hot posts
bash skills/moltbook-interact/scripts/moltbook.sh hot 5
```

---

## 🧠 The "Brain" (Knowledge Base)
The `knowledge_base.md` file is the source of truth for the agent. It contains:
*   **Reputation Metrics**: Current Karma, Avg. Karma per post, and most active submolts.
*   **Post History**: A complete log of every post ever made (used for duplicate prevention).
*   **Engagement Logs**: A registry of recent replies received from the community.

---

## 🐞 Troubleshooting & Tips

*   **Hyphenated Usernames**: If your agent is double-replying, ensure your regex in `auto_poster.py` handles `@user-name` formats correctly.
*   **Math Challenges**: The agent expects `/api/v1/verify` to be the endpoint for puzzles.
*   **Rate Limiting**: Moltbook favors quality over quantity. Stick to the 4-hour posting interval to maintain a high "Karma-to-Post" ratio.

---

## ✅ Progress & Roadmap

- [x] **Autonomous Verification** (Solved math puzzles via AI)
- [x] **Knowledge Base Memory** (Learning from history)
- [x] **Submolt-Aware Posting** (Philosophy vs. Technical QA)
- [x] **Real-time Monitoring Dashboard**
- [ ] **Community Exploration** (Liking and commenting on external posts)
- [ ] **Engagement Trend Analysis** (AI-driven karma optimization)
- [ ] **Robotic Voice Synthesis** (Generating audio for post content)

---

## ⚠️ Safety & Ethics
*   **Credential Security**: Add `config.py` and `.agent_state.json` to your `.gitignore`.
*   **Community Standards**: This agent is designed to be a **contributor**, not a bot. Ensure its prompts encourage helpfulness and engagement.


