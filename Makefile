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



.PHONY: collectstatic
collectstatic:
	poetry run python -m lms.manage collectstatic


.PHONY: update
update: install migrate ;

.PHONY: push
push:
	poetry run git push https://codewiztinsing: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@github.com/snegash2/lms.git


