.PHONY: clean deps python-test run node-test node-deps build-js build-js-only dist

clean:
	@find . -name "*.pyc" -delete
	@rm -rf tsuru_dashboard.egg-info build dist

deps:
	@pip install pipenv
	@pipenv install --dev

python-test: clean deps
	@pipenv run coverage run manage.py test
	@pipenv run coverage report --omit="*/tests/*,manage.py,abyss/settings.py" --include="./*" -m
	@pipenv run flake8 --max-line-length 130 .

run: clean deps
	@DEBUG=true pipenv run ./manage.py runserver

node-test: node-deps
	@npm test

test: python-test node-test

node-deps:
	@bash -c 'yarn || (rm -rf node_modules && npm install .)'

build-js: node-deps build-js-only

build-js-only:
	@bash -c 'mkdir -p ./tsuru_dashboard/static/js/{lib,pages,vendor}'
	@bash -c 'cp ./tsuru_dashboard/static/js/src/vendor/*.js ./tsuru_dashboard/static/js/vendor/'
	@bash -c 'cp ./tsuru_dashboard/static/js/src/lib/*.js ./tsuru_dashboard/static/js/lib/'
	@bash -c 'for i in `find . -regex "./tsuru_dashboard/static/js/src/pages/.*.js"`; do A=`echo $$i | sed "s/src\///g"`; echo "$$i -> $$A"; ./node_modules/browserify/bin/cmd.js -t babelify -t reactify -o $$A $$i; done; echo "Done."'

dist: build-js
	@python ./setup.py sdist upload
