readme: README.md

README.md: readme/README.md.j2 Makefile additionals/*.py entorypoint.sh
	./entorypoint.sh $< -d readme/replace-uses.json > $@

setup:
	pip install -r requirements.txt
