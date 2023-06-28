# kamidana-action

[kamidana][] is yet another jinja2's cli wrapper.

## Usage

### Variable / Data file Example

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
name: Test
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
        uses: ./
        with:
          template: testdata/test.j2
          output_file: test.txt
          data_file: github_context.json
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
