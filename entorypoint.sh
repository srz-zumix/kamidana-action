#!/usr/bin/env bash
set -euox pipefail

declare -a KAMIDANA_OPTINOS
declare -a ADITIONALS_OPTIONS

if [ -n "${INPUTS_DATA_FILE}" ]; then
    KAMIDANA_OPTINOS+=(--data "${INPUTS_DATA_FILE}")
fi
if [ -n "${INPUTS_VARIABLES}" ] && [ -n "${INPUTS_INPUT_FORMAT}" ]; then
    KAMIDANA_OPTINOS+=(--input-format "${INPUTS_INPUT_FORMAT}")
fi

while IFS= read -r line
do
    ADITIONALS_OPTIONS+=(--additionals "${line}")
done < <(printf '%s' "${INPUTS_ADDITONALS}")

# while IFS= read -r line
# do
#     KAMIDANA_OPTINOS+=(--extension "${line}")
# done < <(printf '%s' "${INPUTS_EXTENSIONS}")

OUTPUT_FILE=${INPUTS_OUTPUT_FILE:-kamidana-output.txt}

# github actions context

if [ -n "${GITHUB_CONTEXT}" ]; then
    {
        echo '{ "github":'
        echo "${GITHUB_CONTEXT}"
        echo '}'
    } > "${RUNNER_TEMP}/github.json"
    KAMIDANA_OPTINOS+=(--data "${RUNNER_TEMP}/github.json")
fi

if [ -n "${JOB_CONTEXT}" ]; then
    {
        echo '{ "job":'
        echo "${JOB_CONTEXT}"
        echo '}'
    } > "${RUNNER_TEMP}/job.json"
    KAMIDANA_OPTINOS+=(--data "${RUNNER_TEMP}/job.json")
fi

if [ -n "${RUNNER_CONTEXT}" ]; then
    {
        echo '{ "runner":'
        echo "${RUNNER_CONTEXT}"
        echo '}'
    } > "${RUNNER_TEMP}/runner.json"
    KAMIDANA_OPTINOS+=(--data "${RUNNER_TEMP}/runner.json")
fi

# do kamidana

if [ "${INPUTS_DUMP_CONTEXT}" = "true" ]; then
    kamidana --list-info "${ADITIONALS_OPTIONS[@]}"
    KAMIDANA_OPTINOS+=(--dump-context)
fi
if [ "${INPUTS_DEBUG}" = "true" ]; then
    KAMIDANA_OPTINOS+=(--debug)
fi

echo "${INPUTS_VARIABLES:-}" | kamidana "${KAMIDANA_OPTINOS[@]}" "${ADITIONALS_OPTIONS[@]}" "${INPUTS_TEMPLATE}" | tee "${OUTPUT_FILE}"

{
    echo 'result<<EOF'
    cat "${OUTPUT_FILE}"
    echo 'EOF'
}  >> "${GITHUB_OUTPUT}"
