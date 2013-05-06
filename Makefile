clean:
	@find . -name "*.pyc" -delete

deps:
	@pip install -r test-requirements.txt

# test: clean deps
test: clean
	@coverage run manage.py test
	@coverage report
	@flake8 .
