run:
	@uvicorn workoutapi.main:app --reload

create-migrations:
# Windows
	@set PYTHONPATH=%PYTHONPATH%;%cd% && alembic revision --autogenerate -m "$(d)"
# Linux
#	@PYTHONPATH=PYTHONPATH:$(pwd) alembic revision --autogenerate -m $(d)

run-migrations:
# Windows
	@set PYTHONPATH=%PYTHONPATH%;%cd% && alembic upgrade head
# Linux
#	@PYTHONPATH=PYTHONPATH:$(pwd) alembic upgrade head

reqs:
	@pip freeze > requeriments.txt