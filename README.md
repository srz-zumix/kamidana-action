# kamidana-action

[kamidana][] is yet another jinja2's cli wrapper.

## Usage

### Variable / Data file Example

[variables-and-data-file-example.j2](testdata/variables-and-data-file-example.j2)

```text
{{ job }}
{{ workflow }}
{{ name }}
{{ sample }}
```

[variables-and-data-file-example.yml](.github/workflows/variables-and-data-file-example.yml)

```yaml
name: Variables-And-Data-File-Example
on:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: dump github context
        env:
          GITHUB_CONTEXT: ${{ toJson(github) }}
        run: |
          echo "${GITHUB_CONTEXT}" | tee github_context.json
      - name: kamidana
        id: kamidana
        uses: srz-zumix/kamidana-action@main
        with:
          template: testdata/variables-and-data-file-example.j2
          output_file: test.txt
          data_file: github_context.json
          variables: |
            { "sample": "test", "name": "srz-zumix" }
          input-format: json
      - run: |
          echo "${{ steps.kamidana.outputs.text }}" | tee output.txt
          diff output.txt test.txt
```

### Additionals Example

[additionals-example.j2](testdata/additionals-example.j2)

```text
{{ "srz_zumix" | slack_user_id | slack_user_presence }}

* rust-*
{%- set compilers = wandbox_list() | wandbox_fnmatch_compilers("rust-*") %}
{%- for compiler in compilers %}
  * {{ compiler.name }}
{%- endfor %}
```

[additionals-example.yml](.github/workflows/additionals-example.yml)

```yaml
name: Additionals-Example
on:
  pull_request:

env:
  SLACK_TOKEN: ${{ secrets.SLACK_TOKEN }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: kamidana
        id: kamidana
        uses: srz-zumix/kamidana-action@main
        with:
          template: testdata/additionals-example.j2
          output_file: test.txt
          requirements: |
            yurumikuji
            amaterasu-j2
          additonals: |
            yurumikuji.yurumikuji
            amaterasu.amaterasu
      - run: |
          echo "${{ steps.kamidana.outputs.text }}" | tee output.txt
          diff output.txt test.txt
```

[kamidana]:https://github.com/podhmo/kamidana
