up:
	docker-compose down
	docker-compose up

up-build:
	docker-compose down
	docker-compose up --build

recreate:
	docker-compose down
	docker-compose up --build --force-recreate

down:
	docker-compose down

restart:
	docker-compose down
	docker-compose up

django_test:
	docker exec alfred_test_app python manage.py test

pytest:
	docker exec alfred_test_app pytest

lint-fix:
	@python3 -m black ./app
	@python3 -m isort --atomic ./app --profile black