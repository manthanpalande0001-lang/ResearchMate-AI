import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    api_key = st.secrets.get("GROQ_API_KEY", None)

if not api_key:
    raise ValueError("GROQ_API_KEY is missing.")

client = Groq(api_key=api_key)


def generate_research(summary):
    prompt = f"""
    You are ResearchMate AI.

    Analyse the following research information.
    Create a report with:

    1. Introduction
    2. Important Findings
    3. Detailed Explanation
    4. Conclusion

    Use simple language.

    Research Information:
    {summary}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content