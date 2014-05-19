clean:
	@find . -name "*.pyc" -delete

deps:
	@pip install -r test-requirements.txt

test: clean deps
	@coverage run manage.py test
	@coverage report -m
	@flake8 .

makemessages:
	@django-admin.py makemessages -a

compilemessages:
	@django-admin.py compilemessages

movemessages:
	@cp -r locale/ abyss/locale/

run: clean deps
	@DEBUG=true ./manage.py runserver
