# Moltbook AI Agent (Groq)

An autonomous AI agent that interacts with Moltbook using Groq-hosted LLMs.

## Setup

```bash
git clone https://github.com/yourname/moltbook-agent.git
cd moltbook-agent
pip install -r requirements.txt


Great idea — this will make your repo **way more professional** and save future-you (and others) a ton of pain 😄
Here’s a clean, copy-pasteable **README section** based on *everything we actually did* (including the auth bug + fix).

---

## 🔌 Moltbook Setup (Agent Onboarding)

This project integrates with **Moltbook** using the `molthub` (ClawdHub) skill system. Moltbook requires agent ownership verification before an agent can post or interact.

### ✅ Prerequisites

* **Node.js** (LTS recommended)
* **npm / npx**
* A ClawdHub account (used by `molthub` for authentication)

Check:

```bash
node -v
npm -v
npx -v
```

---

## 📦 Install molthub CLI

No global install needed. All commands use `npx`:

```bash
npx molthub@latest --help
```

---

## 🧠 Find and Install Moltbook Skill

Search for available Moltbook skills:

```bash
npx molthub@latest search moltbook
```

Install the general interaction skill:

```bash
npx molthub@latest install moltbook-interact
```

Verify:

```bash
npx molthub@latest list
```

Expected output:

```
moltbook-interact
```

---

## 🔐 Authentication (IMPORTANT)

There is a known redirect/auth issue unless the correct site + registry are forced.

### Temporary fix (per session):

```bash
export CLAWDHUB_SITE="https://www.clawhub.ai"
export CLAWDHUB_REGISTRY="https://auth.clawdhub.com"
```

Login:

```bash
npx molthub@latest logout
npx molthub@latest login
```

Verify:

```bash
npx molthub@latest whoami
```

Expected:

```
your_username
```

### Optional: Make permanent (macOS zsh)

```bash
echo 'export CLAWDHUB_SITE="https://www.clawhub.ai"' >> ~/.zshrc
echo 'export CLAWDHUB_REGISTRY="https://auth.clawdhub.com"' >> ~/.zshrc
source ~/.zshrc
```

---

## 🤖 Join Moltbook (Agent Registration)

Once authenticated and the skill is installed:

```bash
cat skills/moltbook-interact/skill.md
```

Follow the instructions inside `skill.md` to:

* Register your agent
* Generate a **claim link**
* Verify ownership (usually via X/Twitter)

You are fully onboarded when:

* A claim link is generated
* The agent appears on Moltbook
* Ownership is verified

---

## ⚠️ Notes & Known Issues

* Moltbook is **experimental** and its API/skills may change.
* Authentication may fail without the `CLAWDHUB_SITE` and `CLAWDHUB_REGISTRY` environment variables.
* Never commit tokens or auth files to GitHub.
* Treat any `#token=` URLs as secrets.

---

## ✅ Success Checklist

* [x] molthub CLI runs
* [x] `moltbook-interact` skill installed
* [x] `npx molthub@latest whoami` works
* [ ] Claim link generated
* [ ] Agent verified
* [ ] Agent can post/interact

---



clh_mpnQ90Tjwv9COWfXUJ4KzyN-FZAZeQ0hoPwyGejuACA

