# kamidana-action

[kamidana][] is yet another jinja2's cli wrapper.

## Features

* github/job/runner [context](https://docs.github.com/en/actions/learn-github-actions/contexts) is provided by default
* [kamidana][] additionals
  * [env](https://github.com/podhmo/kamidana/blob/master/kamidana/additionals/env.py)
  * [naming](https://github.com/podhmo/kamidana/blob/master/kamidana/additionals/naming.py)
  * [reader](https://github.com/podhmo/kamidana/blob/master/kamidana/additionals/reader.py)
* kamidana-action additonals
  * [color](additionals/color.py)
    * is_success
    * is_failure
    * (as_global) status_success_color
    * (as_global) status_failure_color
    * (as_global) status_other_color
    * actions_status_color
    * status_color
    * discord_color
  * [filter](additionals/filter.py)
    * ternary
    * b64encode
    * b64decode
  * [github](additionals/github.py)
    * get_user
    * get_user_email
  * [io](additionals/io.py)
    * relativepath
    * abspath
    * basename
    * dirname
    * path_exists
    * listdir
    * listdir_files
    * listdir_dirs
  * [json](additionals/json.py)
    * [json_query](https://jmespath.org/)
      * [playground](https://play.jmespath.org/)
    * json_dumps
    * json_loads
  * [to_yaml](additionals/to_yaml.py)
    * to_yaml
    * to_nice_yaml
* user defined additionals

## Usage

### GitHub Context Example

[default-example.j2](testdata/default-example.j2)

```text
{{ github.job }}
{{ github.workflow }}
{{ "ng" | status_color }}
{{ job.status | outcome_color | discord_color }}
{{ (github.actor | github_user).html_url }}
{{ github.ref_protected | ternary('protected', '') }}
{{ github.ref | regex_replace('refs/.*/(.*)', '\1') }}
{{ github.ref_name | b64encode }}
{{ github.ref | b64encode | b64decode }}
{{ runner.name }} ({{ runner.os }}/{{ runner.arch }})
{% set template_filename = github.workspace + "/testdata/default-example.j2" -%}
{{ template_filename | basename }}
{{ template_filename | read_from_file }}
{%- for url in (github | json_query('[*.url,*.*.url,*.*.*.url] | [] | [] | []')) %}
* {{ url }}
{%- endfor %}
{{ '日本語test\nです' | json_dumps(ensure_ascii=True) }}
{{ '日本語test\nです' | json_dumps }}
{{ (github.event | json_dumps | json_loads).repository.name }}

{{ github | to_nice_yaml }}
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
      - uses: actions/checkout@v4
      - name: kamidana
        id: kamidana
        uses: srz-zumix/kamidana-action@main
        with:
          template: testdata/default-example.j2
          output_file: test.txt
          tee: true
      - run: |
          cat << 'EOS' | tee output.txt
          ${{ steps.kamidana.outputs.text }}
          EOS
          diff output.txt test.txt
```

[runs](https://github.com/srz-zumix/kamidana-action/actions/workflows/default-example.yml)

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

[variables-and-multi-data-file-example.yml](.github/workflows/variables-and-multi-data-file-example.yml)

```yaml
name: Variables-And-Multi-Data-File-Example
on:
  pull_request:

jobs:
  variables-and-multi-data-file-example:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
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
          cat << 'EOS' | tee output.txt
          ${{ steps.kamidana.outputs.text }}
          EOS
          diff output.txt test.txt
```

[runs](https://github.com/srz-zumix/kamidana-action/actions/workflows/variables-and-multi-data-file-example.yml)

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
  workflow_dispatch:

env:
  SLACK_TOKEN: ${{ secrets.SLACK_TOKEN }}

jobs:
  additionals-example:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
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
          cat << 'EOS' | tee output.txt
          ${{ steps.kamidana.outputs.text }}
          EOS
          diff output.txt test.txt
```

[runs](https://github.com/srz-zumix/kamidana-action/actions/workflows/additionals-example.yml)

### IO Example

[io-example.j2](testdata/io-example.j2)

```text
{{ "." | abspath }}
{{ "." | abspath | basename }}
{{ "." | listdir }}
{{ "." | listdir_files }}
{{ "." | listdir_dirs }}
{{ "LICENSE" | relativepath }}
{% if ("LICENSE" | path_exists) %}
    {{ "LICENSE" | read_from_file(relative_self=False) }}
{% endif %}
```

[io-example.yml](.github/workflows/io-example.yml)

```yaml
name: IO-Example
on:
  pull_request:

jobs:
  io-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create TestData
        run: |
          cat << 'EOS' > io-test.j2
          {%- set dir = "./.github" -%}
          {% for f in dir | listdir_dirs %}{{ dir }}/{{ f }}
          {% endfor -%}
          ---
          {% for f in dir | listdir_files %}{{ dir }}/{{ f }}
          {% endfor -%}
          EOS
      - name: kamidana
        id: kamidana
        uses: srz-zumix/kamidana-action@main
        with:
          template: io-test.j2
          output_file: test.txt
          tee: true
      - name: Test
        run: |
          {
            find ./.github -type d -mindepth 1 -maxdepth 1
            echo "---"
            find ./.github -type f -mindepth 1 -maxdepth 1
          } >> output.txt
          diff output.txt test.txt
      - run: |
          cat output.txt
          echo "====="
          cat test.txt
          echo "====="
          cat "io-test.j2"
        if: failure()

  io-example:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: kamidana
        id: kamidana
        uses: srz-zumix/kamidana-action@main
        with:
          template: testdata/io-example.j2
          output_file: test.txt
          tee: true
      - run: |
          cat << 'EOS' | tee output.txt
          ${{ steps.kamidana.outputs.text }}
          EOS
          diff output.txt test.txt

  io-example-wd:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: kamidana
        id: kamidana
        uses: srz-zumix/kamidana-action@main
        with:
          template: io-example.j2
          output_file: test.txt
          tee: true
          working-directory: testdata
      - run: |
          cat << 'EOS' | tee output.txt
          ${{ steps.kamidana.outputs.text }}
          EOS
          diff output.txt testdata/test.txt
```

[runs](https://github.com/srz-zumix/kamidana-action/actions/workflows/io-example.yml)

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
      - uses: actions/checkout@v4
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
            debug
      - run: |
          cat << 'EOS' | tee output.txt
          ${{ steps.kamidana.outputs.text }}
          EOS
          diff output.txt test.txt
```

[runs](https://github.com/srz-zumix/kamidana-action/actions/workflows/extensions-example.yml)

[kamidana]:https://github.com/podhmo/kamidana
