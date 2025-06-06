import openai
from config import settings

openai.api_key = settings.gG1uZhj50x1lYFKrrB5kT3BlbkFJXP3R63ExWT9lkcHI0pRq

def call_openai(prompt, temperature=0.7, max_tokens=2048):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message["content"].strip()
