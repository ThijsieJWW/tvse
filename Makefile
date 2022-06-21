default: debug

debug:
	@pip install -e .

dist: build upload clean

build:
	@python -m build

upload:
	@python -m twine upload --skip-existing --repository pypi dist/*

clean:
	@wsl rm -r dist