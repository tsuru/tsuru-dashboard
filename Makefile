clean:
	@find . -name "*.pyc" -delete

deps:
	@pip install -r test-requirements.txt

test: clean deps
	@coverage run manage.py test
	@coverage report
	@flake8 .

locale:
	@django-admin.py makemessages -a
