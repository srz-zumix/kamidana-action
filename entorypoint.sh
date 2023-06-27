#!/usr/bin/env bash
set -euo pipefail

declare -a KAMIDANA_OPTINOS

if [ -n "#{INPUTS_DATA_FILE}" ]; then
    KAMIDANA_OPTINOS+=(--data "${INPUTS_DATA_FILE}")
fi
if [ -n "#{INPUTS_DATA_FORMAT}" ]; then
    KAMIDANA_OPTINOS+=(--data-format "${INPUTS_DATA_FORMAT}")
fi

OUTPUT_FILE=${INPUTS_OUTPUT_FILE:-kamidana-output.txt}

echo "${INPUTS_VARIABLES:-}" | kamidana -i env "${KAMIDANA_OPTINOS[@]}" | tee "${OUTPUT_FILE}"
