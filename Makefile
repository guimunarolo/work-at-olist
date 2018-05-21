run:
	docker-compose up -d
	docker-compose restart api

stop:
	docker-compose down

logs:
	docker-compose logs -f

test:
	docker-compose exec api su -c "python /api/manage.py test . --pattern='test_*.py' --settings=api.settings.test"

migrations:
	docker-compose exec api su -c "python /api/manage.py makemigrations telephony"

migrate:
	docker-compose exec api su -c "python /api/manage.py migrate telephony"

loaddata:
	docker-compose exec api su -c "python /api/manage.py loaddata callevent_initials.json"
