.PHONY venv mongo mongo-down clear

venv:
	python -m venv .venv
	. source .venv/bin/activate

mongo:
	cd 01-introduction
	docker-compose up

mongo-down:
	cd 01-introduction
	docker-compose down

clear:
	deactivate
	rm -rf .venv
