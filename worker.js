from celery import Celery

celery_app = Celery("enclov", broker="redis://localhost:6379/0")

@celery_app.task(name="review_pull_request")
def review_pull_request(repo_url: str, pr_number: int, job_id: str):
    # TODO: Replace this with your actual GitHub + OpenAI logic
    print(f"🔍 Reviewing PR #{pr_number} from {repo_url} [job_id={job_id}]")
    # Simulate processing...
    return {"status": "completed", "comments": ["Looks good!"]}
