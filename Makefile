clean:
	@find . -name "*.pyc" -delete

deps:
	@pip install -r test-requirements.txt
