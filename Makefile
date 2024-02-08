ifeq ($(OS), Windows_NT)
init:
	@pip install -r requirements.txt

user:
	@uvicorn main:app --port 8000 --reload

celery:
	@celery -A task.celery worker -l info --pool=solo -E

endif