#!/bin/bash
## -----------------------------------------------------------------------
## Intent: View latest VERSION file string for a repository
## -----------------------------------------------------------------------

##-------------------##
##---]  GLOBALS  [---##
##-------------------##
set -euo pipefail

case "$OSTYPE" in
    darwin*) declare -x BROWSER="${BROWSER:-safari}" ;;
    *)
        # declare -x BROWSER="${BROWSER:-firefox}"
        # declare -x BROWSER="${BROWSER:-google-chrome}"
        declare -x BROWSER="${BROWSER:-opera}"
       ;;
esac

declare -g pgm="$(readlink --canonicalize-existing "$0")"
declare -g pgmbin="${pgm%/*}"
declare -g pgmroot="${pgmbin%/*}"
declare -g pgmname="${pgm%%*/}"

readonly pgm
readonly pgmbin
readonly pgmroot
readonly pgmname


## -----------------------------------------------------------------------
## Intent: Display an error message then exit with status
## -----------------------------------------------------------------------
function error()
{
    echo "${FUNCNAME[1]} ERROR: $*"
    exit 1
}

## -----------------------------------------------------------------------
## Intent: Display a message decorated for the calling function
## -----------------------------------------------------------------------
function func_echo()
{
    echo "${FUNCNAME[1]}: $*"
    return
}

## -----------------------------------------------------------------------
## Intent: Helper method
## -----------------------------------------------------------------------
## Usage : local path="$(join_by '/' 'lib' "${fields[@]}")"
## -----------------------------------------------------------------------
function join_by()
{
    local d=${1-} f=${2-}; if shift 2; then printf %s "$f" "${@/#/$d}"; fi;
}

## -----------------------------------------------------------------------
## Intent: --bat code review requests
## -----------------------------------------------------------------------
function usage
{
    cat <<EOH

Usage: $0 repo[, .. repo]
EOH

    return
}

##----------------##
##---]  MAIN  [---##
##----------------##
# https://gerrit.opencord.org/plugins/gitiles/voltha-docs/+/refs/heads/master/VERSION

declare -a repos=()
while [[ $# -gt 0 ]];
do
    ## shift @ARGV
    arg="$1"; shift
    case "$arg" in
        --help) usage; continue ;;
        --repo) repos+=("$1"); shift ;;
#            urls+=("$url_prefix/$arg/$url_suffix")
            # https://gerrit.opencord.org/plugins/gitiles/voltha-docs/+/refs/heads/master/VERSION
            -*) error "Detected invalid switch [$arg]" ;;
            # *) error "Detected invalid switch [$arg]" ;;
    esac
done

[[ ${#repos[@]} -eq 0 ]] && { error "--repo is required"; }

#declare -p repos
#if [[ ${#repos[@]} -eq 0 ]] && [[ -d .git ]]; then
#    readarray -t remote < <(git remote -v show)
#    declare -p remote
#fi

if [[ ${#repos[@]} -gt 0 ]]; then
    declare -a urls=()
    for repo in "${repos[@]}";
    do
        declare -a buffer=()
        buffer+=("https://gerrit.opencord.org/plugins/gitiles")
        buffer+=("/$repo/")
        buffer+=("+/refs/heads/master/VERSION")

        url="$(join_by '/' "${buffer[@]}")"
        urls+=("$url")
    done
    "${BROWSER}" "${urls[@]}" &
fi

# [EOF]
