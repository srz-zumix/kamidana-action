VERSION=main
USES=srz-zumix/kamidana-action@${VERSION}

readme: README.md

README.md: README.md.j2 Makefile additionals/io.py
	echo '{ "replace_uses": "uses: ./", "replace_uses_to": "uses: ${USES}" }' | kamidana -i json $< -a additionals/io.py > $@

setup:
	pip install -r requirements.txt
