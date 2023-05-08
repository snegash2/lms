.PHONY: install
install:
	poetry install


.PHONY: migrate
migrate:
	poetry run python -m lms.manage migrate

.PHONY: makemigrations
makemigrations:
	poetry run python -m lms.manage makemigrations


.PHONY: run-server
run-server:
	poetry run python -m lms.manage runserver

.PHONY: superuser
superuser:
	poetry run python -m lms.manage createsuperuser



.PHONY: superuser
shell:
	poetry run python -m lms.manage shell


.PHONY: update
update: install migrate ;


