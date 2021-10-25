PY = python3
VENV = .venv
BIN=$(VENV)/bin

.PHONY: test help run clean

all: clean test

$(VENV):
	$(PY) -m venv $(VENV)
	touch $(VENV)

test:	$(VENV)
	$(BIN)/$(PY) -m unittest discover

help:	$(VENV)
	$(BIN)/$(PY) cron_expression_parser_cli.py -h
	@echo
	@echo 'make run crontab="*/15 0 1,15 * 1-5 /usr/bin/find"'

run:	$(VENV)
	 @[ "${crontab}" ]  || ( echo 'crontab is not set usage: make run crontab="*/15 0 1,15 * 1-5 /usr/bin/find"'; exit 1 )
	$(BIN)/$(PY) cron_expression_parser_cli.py "$(crontab)"

clean:
	rm -rf $(VENV)
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
