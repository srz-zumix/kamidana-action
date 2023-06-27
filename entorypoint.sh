#!/usr/bin/env bash
set -euox pipefail

declare -a KAMIDANA_OPTINOS

if [ -n "${INPUTS_DATA_FILE}" ]; then
    KAMIDANA_OPTINOS+=(--data "${INPUTS_DATA_FILE}")
fi
if [ -n "${INPUTS_VARIABLES}" ] && [ -n "${INPUTS_FORMAT}" ]; then
    KAMIDANA_OPTINOS+=(--input-format "${INPUTS_FORMAT}")
fi

OUTPUT_FILE=${INPUTS_OUTPUT_FILE:-kamidana-output.txt}

echo "${INPUTS_VARIABLES:-}" | kamidana "${KAMIDANA_OPTINOS[@]}" "${INPUTS_TEMPLATE}" | tee "${OUTPUT_FILE}"

{
    echo 'result<<EOF'
    cat "${OUTPUT_FILE}"
    echo 'EOF'
}  >> "${GITHUB_OUTPUT}"
