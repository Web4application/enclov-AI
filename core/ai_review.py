async def generate_ai_review(diff_text: str) -> str:
    # TODO: Connect this to LLM or local model
    return (
        "✅ Refactored inefficient loop at utils/helpers.py:45.\n"
        "🛡️ Suggested stronger typing in main.py.\n"
        "🧹 Unused imports cleaned in api/views.py.\n"
        "🔒 Security note: avoid exposing tokens in logs."
    )
