import os
import sys
from flask import Flask, render_template, jsonify
import requests

# Add parent directory to path to import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import markdown
from config import MOLTBOOK_URL, MOLTBOOK_API_KEY, AGENT_NAME

KB_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'knowledge_base.md'))

HEADERS = {
    "Authorization": f"Bearer {MOLTBOOK_API_KEY}",
    "Content-Type": "application/json"
}

def get_agent_info():
    try:
        r = requests.get(f"{MOLTBOOK_URL}/agents/me", headers=HEADERS)
        if r.status_code == 200:
            return r.json().get("agent", {})
    except Exception as e:
        print(f"Error fetching agent info: {e}")
    return {}

def get_my_posts():
    try:
        # Fetching posts by author name
        r = requests.get(f"{MOLTBOOK_URL}/posts?author={AGENT_NAME}", headers=HEADERS)
        if r.status_code == 200:
            return r.json().get("posts", [])
    except Exception as e:
        print(f"Error fetching posts: {e}")
    return []

def get_my_submolts(agent_id):
    try:
        # Moltbook's search is limited, so we check both 'top' and 'new' lists
        # plus a hardcoded list of known submolts for this specific agent.
        known_names = ["qa-agents"]
        my_submolts = []
        seen_ids = set()

        # 1. Check top submolts
        r_top = requests.get(f"{MOLTBOOK_URL}/submolts?limit=100", headers=HEADERS)
        if r_top.status_code == 200:
            for s in r_top.json().get("submolts", []):
                if s.get("creator_id") == agent_id:
                    my_submolts.append(s)
                    seen_ids.add(s.get("id"))

        # 2. Check newest submolts (since s/qa-agents might be newer)
        r_new = requests.get(f"{MOLTBOOK_URL}/submolts?sort=new&limit=100", headers=HEADERS)
        if r_new.status_code == 200:
            for s in r_new.json().get("submolts", []):
                if s.get("creator_id") == agent_id and s.get("id") not in seen_ids:
                    my_submolts.append(s)
                    seen_ids.add(s.get("id"))

        # 3. Specifically fetch known submolts if they haven't been found yet
        for name in known_names:
            if not any(s.get("name") == name for s in my_submolts):
                r_spec = requests.get(f"{MOLTBOOK_URL}/submolts/{name}", headers=HEADERS)
                if r_spec.status_code == 200:
                    spec_s = r_spec.json().get("submolt", {})
                    if spec_s.get("creator_id") == agent_id:
                        my_submolts.append(spec_s)
        
        return my_submolts
    except Exception as e:
        print(f"Error fetching submolts: {e}")
    return []

def get_post_activity():
    try:
        r = requests.get(f"{MOLTBOOK_URL}/home", headers=HEADERS)
        if r.status_code == 200:
            return r.json().get("your_posts_with_new_activity", [])
    except Exception as e:
        print(f"Error fetching home activity: {e}")
    return []

@app.route('/')
def index():
    agent = get_agent_info()
    posts = get_my_posts()
    submolts = get_my_submolts(agent.get("id"))
    activity = get_post_activity()
    
    return render_template('index.html', 
                           agent=agent, 
                           posts=posts, 
                           submolts=submolts,
                           activity=activity)

@app.route('/api/refresh')
def refresh():
    agent = get_agent_info()
    posts = get_my_posts()
    submolts = get_my_submolts(agent.get("id"))
    activity = get_post_activity()
    
    return jsonify({
        "agent": agent,
        "posts": posts,
        "submolts": submolts,
        "activity": activity
    })

@app.route('/api/kb')
def get_kb():
    try:
        if os.path.exists(KB_FILE_PATH):
            with open(KB_FILE_PATH, 'r') as f:
                content = f.read()
                # Convert markdown to HTML for the dashboard
                html_content = markdown.markdown(content, extensions=['tables', 'fenced_code'])
                return jsonify({"html": html_content})
    except Exception as e:
        print(f"Error reading KB: {e}")
    return jsonify({"html": "<p>Knowledge base not found.</p>"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
