readme: README.md

README.md: readme/README.md.j2 Makefile additionals/*.py entorypoint.sh
	INPUTS_OUTPUT_FILE=$@ ./entorypoint.sh $< -d readme/replace-uses.json

setup:
	pip install -r requirements.txt
