# utils/llm_client.py

from openai import OpenAI

openai_client = OpenAI(api_key="sk-...")

def analyze_code_with_llm(diff: str) -> list:
    system_prompt = (
        "You are a senior code reviewer. Analyze this GitHub PR diff and return improvement suggestions, "
        "style issues, refactor ideas, and security concerns."
    )
    response = openai_client.chat.completions.create(
        model="gpt-4",  # or gpt-3.5-turbo, llama3, etc.
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": diff}
        ],
        temperature=0.3
    )
    suggestions = response.choices[0].message.content.strip()
    return suggestions.split("\n")
