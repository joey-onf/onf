#!/bin/bash
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------

function join_by()
{
    local d=${1-} f=${2-}; if shift 2; then printf %s "$f" "${@/#/$d}"; fi;
}

## -----------------------------------------------------------------------
## Intent: Create sandbox storage
## -----------------------------------------------------------------------
function sbx_all_get()
{
    local repo="$1" ; shift
    local -n ref=$1 ; shift

    if [[ ! -v sbx_all_get__root ]]; then
	local root0="${0%/*}"
	local root="$(realpath --canonicalize-existing "$root0")"
	local path="$root/${repo}-all"
	declare -g sbx_all_get__root="$path"
	readonly sbx_all_get__root
    fi

    ref="$sbx_all_get__root"
    return
}

## -----------------------------------------------------------------------
## Intent: Create sandbox storage
## -----------------------------------------------------------------------
function sbx_all_mkdir()
{
    local __repo="$1" ; shift
    local -n sbx_all_mkdir_ref=$1 ; shift

    local tmp=''
    sbx_all_get "$__repo" tmp
    declare -p tmp
    mkdir -p "$tmp"

    sbx_all_mkdir_ref="$tmp"
    return
}

## -----------------------------------------------------------------------
## Intent: Construct a sandbox-all path from arguments
## -----------------------------------------------------------------------
function sbx_all_path()
{
    local -n sbx_all_path_ref=$1    ; shift
    local sbx_all_path_repo="$1" ; shift

    local base=''
    sbx_all_get "$sbx_all_path_repo" base

    if [[ $# -gt 0 ]]; then
	sbx_all_path_ref=$(join_by '/' "$base" "$*")
    else
	sbx_all_path_ref="$base"
    fi

    return
}

## -----------------------------------------------------------------------
## Intent: Display sandbox attributes
## -----------------------------------------------------------------------
function sbx_meta()
{
    local dir="$1"; shift

    func_banner "Temp sandbox meta"

    pushd "$tmp_sbx" >/dev/null
    set -x
    git remote -v show
    echo
#   git branch -a | grep '*'
    git branch
    set +x
    echo
    popd >/dev/null

    return
}

# [EOF]
