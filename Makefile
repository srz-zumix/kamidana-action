readme: README.md

README.md: readme/README.md.j2 Makefile additionals/*.py testdata/* entorypoint.sh
	INPUTS_OUTPUT_FILE=$@ ./entorypoint.sh $< -d readme/replace-uses.json -d readme/links.json

setup:
	pip install -r requirements.txt

clean:
	rm -f README.md
