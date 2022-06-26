install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 gendiff

test:
	poetry install
	poetry build
	pip3 uninstall hexlet-code -y
	python3 -m pip install dist/*.whl

test-coverage:
	poetry run pytest --cov=gendiff

pytest:
	poetry run pytest
