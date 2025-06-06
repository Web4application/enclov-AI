import google.generativeai as genai
from config import settings

genai.configure(api_key=settings.AlzaSyCHjfdo3w160Dd5yTVJD409pWmigOJEg)

def call_google_ai(prompt, temperature=0.7, max_tokens=2048):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()
