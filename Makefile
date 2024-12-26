.PHONY: venv activate clean install

VENV_NAME=venv
PYTHON=python3
MAKEFILE_DIR=$(dir $(realpath $(firstword $(MAKEFILE_LIST))))
SRC_DIR=$(MAKEFILE_DIR)src

venv: install

install:
	$(PYTHON) -m venv $(VENV_NAME)
	./$(VENV_NAME)/bin/pip install -r requirements.txt
	@echo "Virtual environment created and requirements installed. Run 'make activate' to activate it"

activate:
	@echo "To activate the virtual environment, run:"
	@echo "source $(VENV_NAME)/bin/activate"

clean:
	rm -rf $(VENV_NAME)

run:
	./$(VENV_NAME)/bin/python $(SRC_DIR)/run_flow.py
