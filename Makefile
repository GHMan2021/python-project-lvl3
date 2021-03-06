install:
	poetry install
build:
	poetry build
package-install:
	python3 -m pip install --user dist/*.whl
package-reinstall:
	python3 -m pip install --force-reinstall --user dist/*whl
lint:
	poetry run flake8 page_loader
test:
	poetry run pytest tests/ -vv --log-cli-level='INFO'
test-coverage:
	poetry run pytest --cov=page_loader --cov-report=xml tests/
