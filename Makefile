.PHONY: venv activate clean

VENV_NAME=venv
PYTHON=python3

venv:
	$(PYTHON) -m venv $(VENV_NAME)
	@echo "Virtual environment created. Run 'make activate' to activate it"

activate:
	@echo "To activate the virtual environment, run:"
	@echo "source $(VENV_NAME)/bin/activate"

clean:
	rm -rf $(VENV_NAME)
