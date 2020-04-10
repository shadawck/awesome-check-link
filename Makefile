files=awesome_check_link test *.py
MODULE=awesome_check_link
test:
	pytest -s -v test/test_*.py --doctest-modules --cov aclinks --cov-config=.coveragerc --cov-report term-missing

lint:
	flake8 $(files)

fix:
	autopep8 --in-place -r $(files)

install:
	pip install -r requirements.txt -r test-requirements.txt

report:
	codecov

build: aclinks
	rm -rf dist
	python3 setup.py sdist bdist_wheel --bdist-dir ~/temp/bdistwheel

publish:
	make build
	twine upload --config-file ~/.pypirc -r pypi dist/*

clean:
	rm -rf __pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache
	rm -rf coverage.xml .coverage
	rm -rf .vscode

fclean: clean
	rm -rf build/
	rm -rf dist/
	rm -rf ${MODULE}.egg-info

.PHONY: clean fclean test coverage
