#!/bin/bash
## -----------------------------------------------------------------------
## Intent: This script will apply common cleanup actions to sources.
## -----------------------------------------------------------------------

while [ $# -gt 0 ]; do
    case "$1" in
	-*debug) declare -g -i debug=1 ;;
	*) break ;;
    esac
    shift
done

declare -a sources=()
[[ $# -gt 0 ]] && sources+=("$*")

if [[ ${#source[@]} -eq 0 ]]; then
    readarray -t git_status < <(git ls-files --modified --deleted)
    sources+=("${git_status[@]}")
    declare -p sources
fi

for source in "${sources[@]}";
do
    # Cleanup whitespace
    sed -i 's/[[:blank:]]*$//' "$source"
done

# [EOF]
