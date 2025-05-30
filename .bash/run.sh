docker build --build-arg CONFIGCAT_AUTH_KEY=yourkeyhere --build-arg JOB_ID=1234 -t myreactapp .
docker run -p 3000:3000 -e JOB_ID=1234 myreactapp
redis-server
uvicorn enclov_ai_backend:app --reload
celery -A enclov_ai_backend.celery_app worker --loglevel=info
