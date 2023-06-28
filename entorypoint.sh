#!/usr/bin/env bash
set -euox pipefail

declare -a KAMIDANA_OPTINOS

if [ -n "${INPUTS_DATA_FILE}" ]; then
    KAMIDANA_OPTINOS+=(--data "${INPUTS_DATA_FILE}")
fi
if [ -n "${INPUTS_VARIABLES}" ] && [ -n "${INPUTS_INPUT_FORMAT}" ]; then
    KAMIDANA_OPTINOS+=(--input-format "${INPUTS_INPUT_FORMAT}")
fi

while IFS= read -r line
do
    KAMIDANA_OPTINOS+=(--additionals "${line}")
done < <(printf '%s' "${INPUTS_ADDITONALS}")

OUTPUT_FILE=${INPUTS_OUTPUT_FILE:-kamidana-output.txt}

echo "${INPUTS_VARIABLES:-}" | kamidana "${KAMIDANA_OPTINOS[@]}" "${INPUTS_TEMPLATE}" | tee "${OUTPUT_FILE}"

{
    echo 'result<<EOF'
    cat "${OUTPUT_FILE}"
    echo 'EOF'
}  >> "${GITHUB_OUTPUT}"
