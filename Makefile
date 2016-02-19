clean:
	@find . -name "*.pyc" -delete
	@rm -rf node_modules tsuru_dashboard.egg-info build dist

deps:
	@pip install -r test-requirements.txt

python-test: clean deps
	@coverage run manage.py test
	@coverage report --omit="*/tests/*,manage.py,abyss/settings.py" --include="./*" -m
	@flake8 --max-line-length 110 .

run: clean deps
	@DEBUG=true ./manage.py runserver

node-test: node-deps
	@npm test

test: python-test node-test

node-deps:
	@npm install .

build-js: node-deps
	@bash -c 'for i in `git status --porcelain | awk "/.*jsx.pages.*.jsx/{print \\$$2}"`; do A=`echo $$i | sed s/jsx/js/g | sed s/pages.//g`; ./node_modules/browserify/bin/cmd.js -t reactify -o $$A $$i; done'

rebuild-all-js: node-deps
	@bash -c 'for i in `find . -regex ".*jsx/pages/.*.jsx"`; do A=`echo $$i | sed s/jsx/js/g | sed s/pages.//g`; ./node_modules/browserify/bin/cmd.js -t reactify -o $$A $$i; done'
