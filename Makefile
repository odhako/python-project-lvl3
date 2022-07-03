install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader

test:
	poetry install
	poetry build
	pip3 uninstall hexlet-code -y
	python3 -m pip install dist/*.whl

test-coverage:
	poetry run pytest --cov=page_loader

pytest:
	poetry run pytest
