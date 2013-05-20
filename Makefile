clean:
	@find . -name "*.pyc" -delete

deps:
	@pip install -r test-requirements.txt

test: clean deps
	@coverage run manage.py test
	@coverage report
	@flake8 .

makemessages:
	@django-admin.py makemessages -a

compilemessages:
	@django-admin.py compilemessages
