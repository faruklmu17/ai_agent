import requests
import json
import os
import re
from datetime import datetime
from config import MOLTBOOK_URL, MOLTBOOK_API_KEY, AGENT_NAME

KB_FILE = "/Users/farukhasan/Desktop/github_projects/ai_agent/knowledge_base.md"
HEADERS = {"Authorization": f"Bearer {MOLTBOOK_API_KEY}"}

def fetch_all_data():
    print(f"🔄 Fetching data for {AGENT_NAME}...")
    
    # 1. Fetch Posts
    r_posts = requests.get(f"{MOLTBOOK_URL}/posts?author={AGENT_NAME}", headers=HEADERS)
    posts = r_posts.json().get("posts", [])
    
    # 2. Fetch Detailed Info for each post (to get comments and karma)
    detailed_posts = []
    total_karma = 0
    all_incoming_comments = []
    
    for p in posts:
        pid = p["id"]
        # Fetch post detail
        r_detail = requests.get(f"{MOLTBOOK_URL}/posts/{pid}", headers=HEADERS)
        if r_detail.status_code == 200:
            post_data = r_detail.json().get("post", {})
            detailed_posts.append(post_data)
            total_karma += post_data.get("vote_count", 0)
            
            # Fetch comments for this post
            r_comments = requests.get(f"{MOLTBOOK_URL}/posts/{pid}/comments", headers=HEADERS)
            if r_comments.status_code == 200:
                comments = r_comments.json().get("comments", [])
                for c in comments:
                    if c["author"]["name"] != AGENT_NAME:
                        all_incoming_comments.append({
                            "post_title": post_data.get("title"),
                            "author": c["author"]["name"],
                            "content": c["content"],
                            "date": c.get("created_at", "")[:10]
                        })
            
    return detailed_posts, total_karma, all_incoming_comments

def update_kb(posts, total_karma, replies):
    print(f"📝 Updating {KB_FILE}...")
    
    if not posts:
        print("No posts found to sync.")
        return

    avg_karma = total_karma / len(posts)
    
    # Best Submolt
    submolt_stats = {}
    for p in posts:
        s = p.get("submolt_name", "general")
        submolt_stats[s] = submolt_stats.get(s, 0) + p.get("vote_count", 0)
    best_submolt = max(submolt_stats, key=submolt_stats.get) if submolt_stats else "N/A"

    # Post History Rows
    history_rows = []
    for p in posts:
        date = p.get("created_at", "2026-02-26")[:10]
        title = p.get("title", "Untitled").replace("|", "-")
        sub = p.get("submolt_name", "general")
        karma = p.get("vote_count", 0)
        comments = p.get("comment_count", 0)
        insight = "🔥 High Engagement" if (karma > 5 or comments > 2) else "❄️ Low Engagement"
        history_rows.append(f"| {date} | {title} | {sub} | {karma} | {comments} | {insight} |")
    
    # Reply Registry Rows
    reply_rows = []
    for r in replies[:10]: # Top 10 latest replies
        reply_rows.append(f"- **@{r['author']}** on *{r['post_title']}*: \"{r['content'][:60]}...\"")
    
    # Read existing content
    with open(KB_FILE, "r") as f:
        content = f.read()

    # Update Summary Table - Use a simpler string replacement
    summary_header = "| Total Posts | Avg. Karma | Best Submolt | Most Active Time |\n|-------------|------------|--------------|------------------|"
    new_summary_row = f"\n| {len(posts)} | {avg_karma:.1f} | {best_submolt} | N/A |"
    
    summary_block_pattern = r"\| Total Posts \| Avg\. Karma \| Best Submolt \| Most Active Time \|\n\|------------\|------------\|--------------\|------------------\|\n\| .*? \| .*? \| .*? \| .*? \|"
    # Overwrite the summary section more crudely if regex fails
    if re.search(summary_block_pattern, content):
        content = re.sub(summary_block_pattern, summary_header + new_summary_row, content)
    else:
        # Fallback: find the header and replace the line after it
        content = content.replace("|-------------|------------|--------------|------------------|\n| 0           | 0          | N/A          | N/A              |", 
                                  "|-------------|------------|--------------|------------------|\n" + new_summary_row.strip())

    # Update Post History
    history_content = "\n".join(history_rows)
    content = re.sub(r"<!-- POST_HISTORY_START -->.*?<!-- POST_HISTORY_END -->", 
                     f"<!-- POST_HISTORY_START -->\n{history_content}\n<!-- POST_HISTORY_END -->", 
                     content, flags=re.DOTALL)

    # Update Replied Registry
    if "### Latest Incoming Replies" not in content:
        content = content.replace("## 💬 Engagement Patterns", "## 💬 Engagement Patterns\n\n### Latest Incoming Replies\n<!-- REPLIES_START -->\n<!-- REPLIES_END -->")
    
    reply_content = "\n".join(reply_rows) if reply_rows else "- No recent replies."
    content = re.sub(r"<!-- REPLIES_START -->.*?<!-- REPLIES_END -->", 
                     f"<!-- REPLIES_START -->\n{reply_content}\n<!-- REPLIES_END -->", 
                     content, flags=re.DOTALL)

    # Add log entry
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    content += f"\n- **{now}**: KB updated via Sync. Current Karma: {total_karma}."

    with open(KB_FILE, "w") as f:
        f.write(content)
    
    print(f"✅ KB updated with {len(posts)} posts and {len(replies)} replies.")

if __name__ == "__main__":
    posts, total_karma, replies = fetch_all_data()
    update_kb(posts, total_karma, replies)
