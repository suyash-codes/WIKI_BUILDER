import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_content(text):
    prompt = f"Summarize the following into a clear Wikipedia-style introduction:\n\n{text}"

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Or another Groq model
        messages=[
            {"role": "system", "content": "You are a summarizer for Wikipedia pages. Produce detailed, sectioned summaries with as much detail as possible."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=5000
    )

    return completion.choices[0].message.content

