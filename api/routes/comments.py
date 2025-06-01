from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/api/comments")
def get_ai_comments(job_id: str = Query(...)):
    # Example: Fetch comments from DB/cache/queue for the given job_id
    # In production, replace with actual job status + comments store (e.g. Redis, PostgreSQL)
    example_comments = [
        "✅ Refactored inefficient loop at <code>utils/helpers.py:45</code>.",
        "🛡️ Suggested stronger typing in <code>main.py</code>.",
        "🧹 Unused imports cleaned in <code>api/views.py</code>.",
        "🔒 Security note: avoid exposing tokens in logs."
    ]
    html = "<ul style='padding-left:1.2rem;'>"
    for comment in example_comments:
        html += f"<li>{comment}</li>"
    html += "</ul>"
    return JSONResponse(content={"comments_html": html})
