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

echo "${INPUTS_VARIABLES:-}" | kamidana -i env "${KAMIDANA_OPTINOS[@]}" | tee "${OUTPUT_FILE}"
