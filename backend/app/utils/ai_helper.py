import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SUMMARIZE_PROMPT = """You are a helpful assistant. Summarize the following note in 2-3 concise sentences. 
Return only the summary, no extra text."""

AUTOTAG_PROMPT = """You are a helpful assistant. Suggest 3-5 relevant tags for the following note.
Return only a comma-separated list of lowercase tags, nothing else. Example: python,flask,api"""


def summarize_note(title: str, content: str) -> str:
    """Call Groq to summarize a note."""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SUMMARIZE_PROMPT},
            {"role": "user", "content": f"Title: {title}\n\nContent: {content}"},
        ],
        max_tokens=200,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


def suggest_tags(title: str, content: str) -> list:
    """Call Groq to suggest tags for a note."""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": AUTOTAG_PROMPT},
            {"role": "user", "content": f"Title: {title}\n\nContent: {content}"},
        ],
        max_tokens=50,
        temperature=0.3,
    )
    raw = response.choices[0].message.content.strip()
    # Parse comma-separated tags into clean list
    return [t.strip().lower() for t in raw.split(",") if t.strip()][:5]
