install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl --force-reinstall

lint:
	poetry run flake8 page_loader

test:
	poetry install
	poetry build
	python3 -m pip install dist/*.whl --force-reinstall

test-coverage:
	poetry run pytest --cov=page_loader

pytest:
	poetry run pytest
