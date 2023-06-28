readme: README.md

README.md: readme/README.md.j2 Makefile additionals/io.py
	kamidana -d readme/replace-uses.json $< -a additionals/io.py > $@

setup:
	pip install -r requirements.txt
