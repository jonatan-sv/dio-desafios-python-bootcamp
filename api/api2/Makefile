# Rodar o servidor
run:
	@uvicorn store.main:app --reload
# Rodar T0DOS os testes
test:
	@poetry run pytest
# Rodar UM teste
test-this:
	@poetry run pytest -s -rx -k $(K) --pdb store ./tests/

clear-cache:
	@poetry run pytest --cache-clear