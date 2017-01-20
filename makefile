
pip:
	pip install --user -e .

clean:
	find . -name __pycache__ -exec rm -rf {} +


.PHONY: *

