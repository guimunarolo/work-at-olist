run:
	docker-compose up

stop:
	docker-compose down

test:
	docker-compose exec api su -c "python /api/manage.py test . --pattern='test_*.py' --settings=api.settings.test"

mkm:
	docker-compose exec api su -c "python /api/manage.py makemigrations"

migrate:
	docker-compose exec api su -c "python /api/manage.py migrate"