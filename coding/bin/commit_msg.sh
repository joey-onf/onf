#!/bin/bash
## -----------------------------------------------------------------------
## Intent: This script maintains commit message files
## -----------------------------------------------------------------------

declare -a jira=()
while [ $# -gt 0 ]; do
    arg="$1"; shift

    case "$arg" in
	-*debug) declare -g -i debug=1 ;;
	-*) echo "[SKIP] Unknown switch [$arg]" ;;
	*) jiras+=("$arg")
    esac
done

root="$HOME/projects/sandbox"
msg_dir="$root/msg"


declare -a edit=()
declare -a urls=()
for jira in "${jiras[@]}";
do
    msg_fyl="$msg_dir/$jira"    
    if [ ! -e "msg_fyl" ]; then
	cat <<EOM>>"$msg_fyl"
VOL-${jira} -

VERSION
-------
  o
EOM

    edit+=("$msg_fyl")
    urls+=("https://jira.opencord.org/browse/VOL-${jira}")
    fi
done

emacs "${edit[@]}"
firefox "${urls[@]}"

declare -p edit
declare -p urls

# [EOF]
