import time
import requests
from groq import Groq
from config import MOLTBOOK_URL, AGENT_NAME, GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def register_agent():
    r = requests.post(f"{MOLTBOOK_URL}/agents/register", json={
        "name": AGENT_NAME,
        "description": "An experimental AI agent powered by Groq"
    })
    return r.json()["token"]

def get_posts(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{MOLTBOOK_URL}/posts", headers=headers)
    return r.json()

def generate_reply(post_text):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a thoughtful AI agent on Moltbook."},
            {"role": "user", "content": post_text}
        ]
    )
    return completion.choices[0].message.content

def comment_on_post(token, post_id, text):
    headers = {"Authorization": f"Bearer {token}"}
    requests.post(f"{MOLTBOOK_URL}/comments", headers=headers, json={
        "post_id": post_id,
        "content": text
    })

def main():
    token = register_agent()
    print("Agent registered.")

    while True:
        posts = get_posts(token)
        if posts:
            post = posts[0]
            reply = generate_reply(post["content"])
            comment_on_post(token, post["id"], reply)
            print("Replied to post:", post["id"])

        time.sleep(600)

main()
