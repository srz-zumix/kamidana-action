# kamidana-action

[kamidana][] is yet another jinja2's cli wrapper.

## Features

* github/job/runner [context](https://docs.github.com/en/actions/learn-github-actions/contexts) is provided by default
* [kamidana][] additionals
  * [env](https://github.com/podhmo/kamidana/blob/master/kamidana/additionals/env.py)
  * [naming](https://github.com/podhmo/kamidana/blob/master/kamidana/additionals/naming.py)
  * [reader](https://github.com/podhmo/kamidana/blob/master/kamidana/additionals/reader.py)
* kamidana-action additonals
  * [io](additionals/io.py)
    * basename
    * dirname
  * [filter](additionals/filter.py)
    * ternary
    * b64encode
    * b64decode
* user defined additionals

## Usage

### GitHub Context Example

[default-example.j2](testdata/default-example.j2)

```text
{{ github.job }}
{{ github.workflow }}
{{ job.status }}
{{ github.ref_protected | ternary('protected', '') }}
{{ github.ref | regex_replace('refs/.*/(.*)', '\1') }}
{{ github.ref_name | b64encode }}
{{ github.ref | b64encode | b64decode }}
{{ runner.name }} ({{ runner.os }}/{{ runner.arch }})
{% set template_filename = github.workspace + "/testdata/default-example.j2" -%}
{{ template_filename | basename }}
{{ template_filename | read_from_file }}
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
          tee: true
      - run: |
          cat << EOS | tee output.txt
          ${{ steps.kamidana.outputs.text }}
          EOS
          diff output.txt test.txt
```

### Variable / Data file Example

[variables-and-data-file-example.j2](testdata/variables-and-data-file-example.j2)

```text
{{ github.job }}
{{ github.workflow }}
{{ name }}
{{ sample }}
{{ replace_uses_to }}
{{ links.kamidana }}
```

[variables-and-data-file-example.yml](.github/workflows/variables-and-data-file-example.yml)

```yaml
name: Variables-And-Data-File-Example
on:
  pull_request:

jobs:
  variables-and-data-file-example-1:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: kamidana
        id: kamidana
        uses: srz-zumix/kamidana-action@main
        with:
          template: testdata/variables-and-data-file-example.j2
          output_file: test.txt
          tee: true
          data_files: testdata/variables-and-data-file-example.json
          variables: |
            sample: test
            name: srz-zumix
      - run: |
          cat << EOS | tee output.txt
          ${{ steps.kamidana.outputs.text }}
          EOS
          diff output.txt test.txt

  variables-and-data-file-example-2:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: kamidana
        id: kamidana
        uses: srz-zumix/kamidana-action@main
        with:
          template: testdata/variables-and-data-file-example.j2
          output_file: test.txt
          tee: true
          data_files: |
            readme/replace-uses.json
            readme/links.json
          variables: |
            sample: test
            name: srz-zumix
      - run: |
          cat << EOS | tee output.txt
          ${{ steps.kamidana.outputs.text }}
          EOS
          diff output.txt test.txt
```

### Additionals Example

[additionals-example.j2](testdata/additionals-example.j2)

```text
{{ "srz_zumix" | slack_user_id | slack_user_presence | surprised }}

* rust-*
{%- set compilers = wandbox_list() | wandbox_fnmatch_compilers("rust-*") %}
{%- for compiler in compilers %}
  * {{ compiler.name }}
{%- endfor %}
```

[surprised.py](testdata/surprised.py)

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
          tee: true
          requirements: |
            yurumikuji
            amaterasu-j2
          additonals: |
            yurumikuji.yurumikuji
            amaterasu.amaterasu
            testdata/surprised.py
      - run: |
          cat << EOS | tee output.txt
          ${{ steps.kamidana.outputs.text }}
          EOS
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
          tee: true
          extensions: |
            i18n
            do
            loopcontrols
            with_
            autoescape
            debug
      - run: |
          cat << EOS | tee output.txt
          ${{ steps.kamidana.outputs.text }}
          EOS
          diff output.txt test.txt
```

[kamidana]:https://github.com/podhmo/kamidana
