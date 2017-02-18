

pip = /usr/local/bin/pip

default: dev

dev:
	$(pip) install --user --upgrade -e .
install:
	$(pip) install --user --upgrade .
uninstall:
	$(pip) uninstall --user --upgrade .
sys:
	sudo $(pip) install --upgrade .
clean:
	find . -name __pycache__ -exec rm -rf {} +


.PHONY: *

