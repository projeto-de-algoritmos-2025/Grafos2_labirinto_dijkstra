VENV_DIR=.venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

.PHONY: all run install clean

all: run

$(VENV_DIR)/bin/activate:
	python3 -m venv $(VENV_DIR)

install: $(VENV_DIR)/bin/activate
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) main.py

clean:
	rm -rf $(VENV_DIR)
