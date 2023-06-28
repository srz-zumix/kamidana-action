# kamidana-action

[kamidana][] is yet another jinja2's cli wrapper.

## Usage

### GitHub Context Example

github/job/runner [context](https://docs.github.com/en/actions/learn-github-actions/contexts) is provided by default.

[default-example.j2](testdata/default-example.j2)

```text
{{ github.job }}
{{ github.workflow }}
{{ job.status }}
{{ runner.name }} ({{ runner.os }}/{{ runner.arch }})
```

[default-example.yml](.github/workflows/default-example.yml)

```yaml
name: Default-Example
on:
  pull_request:

jobs:
  default-example:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: kamidana
        id: kamidana
        uses: srz-zumix/kamidana-action@main
        with:
          template: testdata/default-example.j2
          output_file: test.txt
      - run: |
          echo "${{ steps.kamidana.outputs.text }}" | tee output.txt
          diff output.txt test.txt
```

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
  variables-and-data-file-example:
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
{{ "srz_zumix" | slack_user_id | slack_user_presence | suprised }}

* rust-*
{%- set compilers = wandbox_list() | wandbox_fnmatch_compilers("rust-*") %}
{%- for compiler in compilers %}
  * {{ compiler.name }}
{%- endfor %}
```

[suprised.py](testdata/suprised.py)

```python
from kamidana import (
    as_filter,
)


@as_filter
def surprised(v):
    return "{}!!".format(v)
```

[additionals-example.yml](.github/workflows/additionals-example.yml)

```yaml
name: Additionals-Example
on:
  pull_request:

env:
  SLACK_TOKEN: ${{ secrets.SLACK_TOKEN }}

jobs:
  additionals-example:
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
            testdata/suprised.py
      - run: |
          echo "${{ steps.kamidana.outputs.text }}" | tee output.txt
          diff output.txt test.txt
```

### Extensions Example

[extensions-example.j2](testdata/extensions-example.j2)

```text
{# with with. with_ extension is used. #}
{%- with msg = "hello"%}
{{msg}}
{%- with msg = "world"%}
  {{msg}}
{%- endwith %}
{{msg}}
{%- endwith %}

## counting
{#- with break and continue. loopcontrolls extension is used. #}

{%- for i in range(10) %}
{%- if i % 3 == 0 %}{% continue %} {% endif %}
{%- if i == 5 %}{% break %} {% endif %}
- {{i}}
{%- endfor %}

## do

{%- set xs = [] %}
{%- for i in range(10) %}
{%- do xs.append(i) %}
{%- endfor %}
{{xs}}
```

[extensions-example.yml](.github/workflows/extensions-example.yml)

```yaml
name: Extensions-Example
on:
  pull_request:

jobs:
  extensions-example:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: kamidana
        id: kamidana
        uses: srz-zumix/kamidana-action@main
        with:
          template: testdata/extensions-example.j2
          output_file: test.txt
          extensions: |
            i18n
            do
            loopcontrols
            with_
            autoescape
            debug
      - run: |
          echo "${{ steps.kamidana.outputs.text }}" | tee output.txt
          diff output.txt test.txt
```

[kamidana]:https://github.com/podhmo/kamidana
