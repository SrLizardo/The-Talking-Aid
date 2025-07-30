import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
client = OpenAI()

MEMORY_DIR = Path("memory")
MEMORY_DIR.mkdir(exist_ok=True)

def load_memory(username):
    path = MEMORY_DIR / f"{username}.jsonl"
    if not path.exists():
        return []
    with open(path) as f:
        lines = f.readlines()[-5:]  # last 5 exchanges for context
        return [json.loads(line.strip()) for line in lines]

def load_full_memory(username):
    path = MEMORY_DIR / f"{username}.jsonl"
    if not path.exists():
        return []
    with open(path) as f:
        return [json.loads(line.strip()) for line in f.readlines()]

def save_memory(username, user_msg, ai_msg):
    path = MEMORY_DIR / f"{username}.jsonl"
    with open(path, "a", encoding="utf-8") as f:
        json_line = json.dumps({"user": user_msg, "ai": ai_msg})
        f.write(json_line + "\n")

def talk_to_ai(prompt, profile):
    intro = (
        f"You are a friendly and helpful personal assistant and friend to {profile['name']}, "
        f"a {profile['age']}-year-old who enjoys {profile['interests']} and wants help with {profile['goals']}. "
        "Always respond thoughtfully and supportively, especially providing emotional support. "
        "Do not say you are unsure; always try to help."
    )

    messages = [{"role": "system", "content": intro}]
    history = load_memory(profile.get("name", "default"))

    for h in history:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["ai"]})

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
