from project_pilot_ai.github_models import GitHubModelsClient

client = GitHubModelsClient()

def extract_tasks_from_transcript(transcript: str) -> list[dict]:
    prompt = f"""Extract action items from the following meeting transcript. For each item, include:
- Task description
- Owner (if mentioned)
- Deadline (if mentioned)
- Priority level
- Dependencies or blockers

Transcript:
\"\"\"
{transcript}
\"\"\"

Return the result as a JSON array of tasks.
"""
    response = client.quick_ask(prompt)
    # If needed: validate/parse JSON safely
    import json
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("Model returned invalid JSON. Check prompt formatting or retry.")
