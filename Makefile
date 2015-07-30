clean:
	@find . -name "*.pyc" -delete

deps:
	@pip install -r test-requirements.txt

test: clean deps
	@python manage.py test
	@flake8 --max-line-length 110 .

run: clean deps
	@DEBUG=true ./manage.py runserver
