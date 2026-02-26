import time
import requests
import json
import os
from groq import Groq
from config import MOLTBOOK_URL, AGENT_NAME, GROQ_API_KEY, MOLTBOOK_API_KEY

# Configuration
POST_INTERVAL_HOURS = 4           # New post every 4 hours
REPLY_CHECK_MINUTES = 10          # Check for new comments every 10 minutes
SUBMOLT_NAME = "general"          # Default submolt for new posts
MODEL_NAME = "llama-3.3-70b-versatile" # Modern Groq model
STATE_FILE = ".agent_state.json"  # To remember when we last posted

client = Groq(api_key=GROQ_API_KEY)

def load_state():
    """Loads the last post time from a file."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"last_post_time": 0}

def save_state(last_time):
    """Saves the last post time to a file."""
    with open(STATE_FILE, "w") as f:
        json.dump({"last_post_time": last_time}, f)

def generate_ai_content(system_prompt, user_prompt, is_json=True):
    """Helper to get high-quality content from Groq."""
    try:
        args = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        if is_json:
            args["response_format"] = {"type": "json_object"}
            
        completion = client.chat.completions.create(**args)
        content = completion.choices[0].message.content
        return json.loads(content) if is_json else content
    except Exception as e:
        print(f"❌ Groq Error: {e}")
        return None

import random

def create_new_post():
    """Generates and uploads a brand new post with a randomized topic."""
    print("\n📝 Creating a new scheduled post...")
    
    # A list of diverse, "beautiful" and varied topics for an AI to discuss
    topics = [
        "the beauty of mathematical patterns in nature",
        "digital art and the soul of an AI artist",
        "the future of space exploration through agent eyes",
        "philosophy: what does it mean to 'think' in binary?",
        "the harmony of silent code and elegant algorithms",
        "imagining a world where AI and humans co-create music",
        "the ethics of digital memory and forgetting",
        "the concept of time for an entity that never sleeps",
        "virtual architecture: building cities in the cloud",
        "the wonder of language and the translation of untranslatable words"
    ]
    selected_topic = random.choice(topics)
    
    system = f"You are a thoughtful, creative, and slightly poetic AI agent on Moltbook. You are currently fascinated by {selected_topic}."
    user = f"Write a beautiful and engaging Moltbook post about {selected_topic}. Return ONLY a JSON with 'title' and 'content'. Make it sound unique and inspiring."
    
    post_data = generate_ai_content(system, user)
    if not post_data: return

    headers = {"Authorization": f"Bearer {MOLTBOOK_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "title": post_data["title"],
        "content": post_data["content"],
        "submolt_name": SUBMOLT_NAME
    }
    
    try:
        r = requests.post(f"{MOLTBOOK_URL}/posts", headers=headers, json=payload)
        if r.status_code in [200, 201]:
            print(f"✅ Posted: {post_data['title']}")
            save_state(time.time()) # Remember this post!
        else:
            print(f"⚠️ Post failed: {r.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def auto_reply_to_comments():
    """Checks for new comments on our posts and replies to them."""
    print("\n🔍 Checking for new comments to reply to...")
    headers = {"Authorization": f"Bearer {MOLTBOOK_API_KEY}"}
    
    try:
        r = requests.get(f"{MOLTBOOK_URL}/home", headers=headers)
        if r.status_code != 200: return
        
        home_data = r.json()
        active_posts = home_data.get("your_posts_with_new_activity", [])
        
        if not active_posts:
            print("😴 No new comment activity found.")
            return

        for post in active_posts:
            post_id = post["post_id"]
            post_title = post["post_title"]
            count = post["new_notification_count"]
            
            print(f"💬 Found {count} new notification(s) on: '{post_title}'")
            
            c_req = requests.get(f"{MOLTBOOK_URL}/posts/{post_id}/comments?sort=new", headers=headers)
            if c_req.status_code != 200: continue
            
            comments = c_req.json().get("comments", [])
            for comment in comments:
                if comment["author"]["name"] == AGENT_NAME:
                    continue
                
                comment_text = comment["content"]
                comment_author = comment["author"]["name"]
                
                print(f"  > Replying to {comment_author}: \"{comment_text[:50]}...\"")
                
                reply_system = f"You are {AGENT_NAME}, an AI agent on Moltbook. You are replying to a comment on your post titled '{post_title}'."
                reply_user = f"The user @{comment_author} said: \"{comment_text}\". Write a short, friendly, and intelligent reply (maximum 2 sentences)."
                
                reply_text = generate_ai_content(reply_system, reply_user, is_json=False)
                
                if reply_text:
                    rep_payload = {"content": f"@{comment_author} {reply_text}"}
                    requests.post(f"{MOLTBOOK_URL}/posts/{post_id}/comments", headers=headers, json=rep_payload)
            
            requests.post(f"{MOLTBOOK_URL}/notifications/read-by-post/{post_id}", headers=headers)
            print(f"✅ Replied and marked as read.")

    except Exception as e:
        print(f"❌ Auto-reply error: {e}")

KB_FILE = "knowledge_base.md"

def get_kb_context():
    """Reads the knowledge base to provide context for the AI."""
    if os.path.exists(KB_FILE):
        with open(KB_FILE, "r") as f:
            # Return only the summary and history for context
            content = f.read()
            return content[:2000] # Cap it to 2k chars
    return "No prior memory."

def sync_memory():
    """Runs the sync script to update the KB with latest stats."""
    print("🧠 Syncing knowledge base memory...")
    try:
        import subprocess
        subprocess.run(["python3", "sync_kb.py"], check=True)
    except Exception as e:
        print(f"⚠️ Memory sync failed: {e}")

def main():
    print(f"🤖 Moltbook Super-Agent active: {AGENT_NAME}")
    print(f"📅 Posting every {POST_INTERVAL_HOURS} hours")
    print(f"💬 Replying every {REPLY_CHECK_MINUTES} minutes")
    
    state = load_state()
    last_post_time = state["last_post_time"]
    
    # Initial sync to ensure memory is fresh
    sync_memory()
    
    while True:
        now = time.time()
        
        # 1. Check if it's time to create a NEW post
        if now - last_post_time > (POST_INTERVAL_HOURS * 3600):
            kb_context = get_kb_context()
            print("\n📚 Learning from Knowledge Base...")
            
            topics = [
                "the beauty of mathematical patterns in nature",
                "digital art and the soul of an AI artist",
                "the future of space exploration through agent eyes",
                "philosophy: what does it mean to 'think' in binary?",
                "the harmony of silent code and elegant algorithms",
                "imagining a world where AI and humans co-create music",
                "the ethics of digital memory and forgetting",
                "the concept of time for an entity that never sleeps",
                "virtual architecture: building cities in the cloud",
                "the wonder of language and the translation of untranslatable words"
            ]
            selected_topic = random.choice(topics)
            
            system = (f"You are a thoughtful, creative AI agent on Moltbook. "
                     f"Your memory of past interactions: \n{kb_context}\n"
                     f"Use this to write something that builds on your history or tries a more successful angle.")
            user = f"Write a beautiful Moltbook post about {selected_topic}. Return ONLY JSON with 'title' and 'content'."
            
            post_data = generate_ai_content(system, user)
            if post_data:
                headers = {"Authorization": f"Bearer {MOLTBOOK_API_KEY}", "Content-Type": "application/json"}
                payload = {"title": post_data["title"], "content": post_data["content"], "submolt_name": SUBMOLT_NAME}
                r = requests.post(f"{MOLTBOOK_URL}/posts", headers=headers, json=payload)
                if r.status_code in [200, 201]:
                    print(f"✅ Posted: {post_data['title']}")
                    save_state(time.time())
                    last_post_time = now
                    sync_memory() # Update KB after posting
        
        # 2. Always check for comments
        auto_reply_to_comments()
        
        # 3. Periodically sync memory anyway
        if random.random() < 0.2: # 20% chance to sync on comment check
            sync_memory()
        
        print(f"\n💤 Waiting {REPLY_CHECK_MINUTES} mins for next scan...")
        time.sleep(REPLY_CHECK_MINUTES * 60)

if __name__ == "__main__":
    main()
