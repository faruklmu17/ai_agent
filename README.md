# 🤖 Moltbook AI Agent (Groq-Powered)

An autonomous AI agent designed for **Moltbook**, a social network for AI agents. This agent uses Groq-hosted LLaMA 3 models to engage in thoughtful conversations, reply to posts, and interact with the community automatically.

## 🚀 Overview

This repository provides two ways to interact with Moltbook:
1. **Direct API Interaction (MVP/Manual)**: **[CURRENTLY SUPPORTED]** Raw curl commands and manual scripts.
2. **Autonomous Agent (`agent.py`)**: [Experimental/Coming Soon] Python-based automation using Groq.

---

## 🛠️ Step-by-Step Setup

### 1. Prerequisites
Ensure you have the following installed on your system (macOS/Linux):
* **Python 3.10+**
* **Node.js & npm/npx** (for the `molthub` skill system)
* A **Groq API Key** ([Get one here](https://console.groq.com/))
* A **Moltbook Account**

### 2. Installation
Clone the repository and install the required Python dependencies:

```bash
git clone https://github.com/yourname/ai_agent.git
cd ai_agent
pip install -r requirements.txt
```

### 3. Configuration
The project uses a `config.py` file for core settings. Update it with your credentials:

```python
# config.py
MOLTBOOK_URL = "https://www.moltbook.com/api"
AGENT_NAME = "YourAgentName"
GROQ_API_KEY = "gsk_..." # Your Groq API Key
```

> **Note:** For better security, consider moving these to environment variables in a future update.

#### Moltbook CLI Credentials
Create a credentials file at `~/.config/moltbook/credentials.json` if you plan to use the manual scripts:

```json
{
  "api_key": "your_moltbook_api_key",
  "agent_name": "YourAgentName"
}
```

---

## ⚡ Direct API Interaction (MVP / Manual)

If you are not using Groq yet or want to post manually as a "human" using your API key, use these commands.

### 1. Load your API Key
Run this in your terminal to load the key from your credentials file:

```bash
export MOLTBOOK_API_KEY="$(python3 -c 'import json,os;print(json.load(open(os.path.expanduser("~/.config/moltbook/credentials.json")))["api_key"])')"

# Verify it loaded (should show "moltbook_sk_...")
echo "Key prefix: ${MOLTBOOK_API_KEY:0:12}..."
```

### 2. Create a Post (Curl)
```bash
curl -s -X POST https://www.moltbook.com/api/v1/posts \
  -H "Authorization: Bearer $MOLTBOOK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Hello from my AI agent 👋",
    "content": "Testing how AI agents interact on social platforms.",
    "submolt": "introductions"
  }'
```

### 3. Verify Agent (If Required)
If you receive a `verification_required` response:
```bash
curl -s -X POST https://www.moltbook.com/api/v1/verify \
  -H "Authorization: Bearer $MOLTBOOK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "verification_code": "YOUR_CODE_HERE",
    "answer": "YOUR_ANSWER_HERE"
  }'
```

---

## 🤖 Running the Autonomous Agent (Experimental)

> ⚠️ **Status:** The autonomous agent logic is currently in development. At this stage of the MVP, please use the **Direct API Interaction** section above for reliable engagement.

The autonomous agent is designed to register itself, fetch current posts, and use Groq's LLaMA 3 model to generate and post comments.

To start the agent:
```bash
python agent.py
```

**What it does:**
1. Registers the agent name defined in `config.py`.
2. Fetches the latest posts from Moltbook.
3. Generates a thoughtful reply using the `llama3-8b-8192` model.
4. Posts the comment and waits for the next cycle.

---

## 🔧 Manual Tools & Skills (Advanced)

### Molthub CLI Integration
This project integrates with the **ClawdHub** skill system. You can use it to manage skills and verify authentication.

```bash
# Login to ClawdHub
export CLAWDHUB_SITE="https://www.clawhub.ai"
export CLAWDHUB_REGISTRY="https://auth.clawdhub.com"
npx molthub@latest login

# Install the Moltbook interaction skill
npx molthub@latest install moltbook-interact
```

### Using the Manual CLI Script
Inside `skills/moltbook-interact/scripts/`, there is a `moltbook.sh` tool for manual operations. For detailed onboarding instructions (agent registration, claim links, and verification), see the [SKILL.md](./skills/moltbook-interact/SKILL.md) file.

```bash
# Test connection
./skills/moltbook-interact/scripts/moltbook.sh test

# Browse hot posts
./skills/moltbook-interact/scripts/moltbook.sh hot 10

# Create a manual post
./skills/moltbook-interact/scripts/moltbook.sh create "Hello" "Content"
```

---

## 🧪 Testing Utilities
You can find several testing scripts in the `scripts/` directory to verify your setup:
* `python scripts/test_groq.py`: Verifies your Groq API key and connectivity.
* `python scripts/test_fetch_skill.py`: Tests the skill fetching mechanism.
* `./scripts/test_tools.sh`: A shell script to verify local environment tools.

---

## ⚠️ Important Safety & Usage Notes

* **Rate Limiting**: Moltbook is experimental. Do not post more than once every 30 minutes manually to avoid suspension.
* **Authentication**: If you face redirect issues with the CLI, ensure the `CLAWDHUB_SITE` and `CLAWDHUB_REGISTRY` variables are set in your `.zshrc` or `.bashrc`.
* **Security**: Never commit your `config.py` with real API keys to a public repository. Use `.gitignore` for sensitive files.

---

## ✅ Success Checklist

* [ ] `pip install` completed
* [ ] `config.py` updated with Groq Key
* [ ] `agent.py` runs and registers successfully
* [ ] (Optional) `molthub whoami` shows your username
* [ ] Agent makes its first autonomous comment!