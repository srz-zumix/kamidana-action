#!/usr/bin/env bash
set -euo pipefail

declare -a KAMIDANA_OPTINOS
declare -a ADITIONALS_OPTIONS

if [ "${INPUTS_DEBUG:-false}" = "true" ]; then
    KAMIDANA_OPTINOS+=(--debug)
    set -x
fi

if [ -n "${INPUTS_DATA_FILE:-}" ]; then
    KAMIDANA_OPTINOS+=(--data "${INPUTS_DATA_FILE}")
fi
if [ -n "${INPUTS_VARIABLES:-}" ] && [ -n "${INPUTS_INPUT_FORMAT:-}" ]; then
    KAMIDANA_OPTINOS+=(--input-format "${INPUTS_INPUT_FORMAT}")
fi

# default additionals
while IFS= read -r line
do
    ADITIONALS_OPTIONS+=(--additionals "${line}")
done < <(find "${GITHUB_ACTION_PATH:-.}/additionals" -name '*.py' -not -name '__init__.py')

# inputs additionals
while IFS= read -r line
do
    ADITIONALS_OPTIONS+=(--additionals "${line}")
done < <(printf '%s' "${INPUTS_ADDITONALS:-}")

while IFS= read -r line
do
    KAMIDANA_OPTINOS+=(--extension "${line}")
done < <(printf '%s' "${INPUTS_EXTENSIONS:-}")

OUTPUT_FILE=${INPUTS_OUTPUT_FILE:-kamidana-output.txt}

# github actions context

if [ -n "${GITHUB_CONTEXT:-}" ]; then
    {
        echo '{ "github":'
        echo "${GITHUB_CONTEXT}"
        echo '}'
    } > "${RUNNER_TEMP}/github.json"
    KAMIDANA_OPTINOS+=(--data "${RUNNER_TEMP}/github.json")
fi

if [ -n "${JOB_CONTEXT:-}" ]; then
    {
        echo '{ "job":'
        echo "${JOB_CONTEXT}"
        echo '}'
    } > "${RUNNER_TEMP}/job.json"
    KAMIDANA_OPTINOS+=(--data "${RUNNER_TEMP}/job.json")
fi

if [ -n "${RUNNER_CONTEXT:-}" ]; then
    {
        echo '{ "runner":'
        echo "${RUNNER_CONTEXT}"
        echo '}'
    } > "${RUNNER_TEMP}/runner.json"
    KAMIDANA_OPTINOS+=(--data "${RUNNER_TEMP}/runner.json")
fi

# do kamidana

do_kamidana() {
    echo "${INPUTS_VARIABLES:-}" | kamidana "${KAMIDANA_OPTINOS[@]}" "${ADITIONALS_OPTIONS[@]}" "${INPUTS_TEMPLATE:-$1}" "${@:2:($#-1)}"
}

if [ "${INPUTS_DUMP_CONTEXT:-false}" = "true" ]; then
    kamidana --list-info "${ADITIONALS_OPTIONS[@]}"
    KAMIDANA_OPTINOS+=(--dump-context)
    do_kamidana "$@"
else
    do_kamidana "$@" | tee "${OUTPUT_FILE}"

    if [ -n "${GITHUB_OUTPUT:-}" ]; then
        {
            echo 'result<<EOF'
            cat "${OUTPUT_FILE}"
            echo 'EOF'
        }  >> "${GITHUB_OUTPUT}"
    fi
fi
