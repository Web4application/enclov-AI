pip install fastapi uvicorn celery redis pydantic mlflow optuna shap
redis-server
uvicorn enclov_ai_backend:app --reload
celery -A enclov_ai_backend.celery_app worker --loglevel=info
