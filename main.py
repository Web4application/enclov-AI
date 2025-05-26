import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

# Load your OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY environment variable")

openai.api_key = OPENAI_API_KEY

class CodeReviewRequest(BaseModel):
    code: str

class CodeReviewResponse(BaseModel):
    review_comment: str

@app.post("/analyze-code", response_model=CodeReviewResponse)
async def analyze_code(request: CodeReviewRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code input cannot be empty")

    prompt = f"""
You are a senior code reviewer. Review the following code snippet and provide constructive, concise feedback pointing out potential issues, improvements, or code smells:

Code:
{request.code}

Review:
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.2,
        )
        review_text = response.choices[0].message.content.strip()
        return CodeReviewResponse(review_comment=review_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
