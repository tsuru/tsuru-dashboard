clean:
	@find . -name "*.pyc" -delete

deps:
	@pip install -r test-requirements.txt

test: clean deps
	@coverage run manage.py test
	@coverage report --omit="*/tests/*,manage.py,abyss/settings.py" --include="./*" -m
	@flake8 --max-line-length 110 .

run: clean deps
	@DEBUG=true ./manage.py runserver

node-deps:
	@npm install .

build-js: node-deps
	@./node_modules/browserify/bin/cmd.js -t reactify -o apps/static_files/js/deploy.js apps/static_files/jsx/deploy.jsx
	@./node_modules/browserify/bin/cmd.js -t reactify -o apps/static_files/js/list.js apps/static_files/jsx/list.jsx
