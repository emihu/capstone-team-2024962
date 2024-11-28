lint:
	# temporary skipping mypy until disabling missing import type hints
	# echo "Running mypy..."
	# mypy -v src/ test/
	echo "Running black..."
	black -v --check src/ test/

init:
	pip install -r requirements.txt

.PHONY: lint init
