from project_pilot_ai.github_models import GitHubModelsClient

client = GitHubModelsClient()

def analyze_project_structure(file_tree: str, goals: str) -> dict:
    prompt = f"""
You are an expert project architect. Given the following file and folder tree of a project, analyze what essential components may be missing or disorganized. Then provide clear improvement suggestions to ensure project success.

Include:
- Missing files or folders (tests, configs, docs, CI/CD)
- Suggested structure (reordered or renamed if necessary)
- Key enhancements based on project goals

Project Goals:
{goals}

Project File Tree:
\"\"\"
{file_tree}
\"\"\"

Respond in JSON with fields:
- missing_elements: list
- structural_suggestions: list
- recommended_improvements: list
"""
    response = client.quick_ask(prompt)
    import json
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("Model returned invalid JSON. Check structure or retry.")
