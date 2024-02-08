ifeq ($(OS), Windows_NT)
init:
	@pip install -r requirements.txt

user:
	@uvicorn main:app --port 8000 --reload

celery:
	@celery -A task.celery worker -l info --pool=solo -E
test_all:
	@pytest
test_user:
	@pytest Test/test_user_apis.py
test_label:
	@pytest Test/test_labels_apis.py
test_notes:
	@pytest Test/test_notes_apis.py

endif