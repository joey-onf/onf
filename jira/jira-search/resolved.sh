#!/bin/bash

## --------------------------------------------------------------------
## Intent: Retrieve a list of reason query strings
## --------------------------------------------------------------------
function get_jql_reasons()
{
    local -n ref=$1; shift

    ref+=('Cannot Reproduce')
    ref+=('Duplicate')
    ref+=('Fixed')
    ref+=('Incomplete')
    ref+=("Won't Do")
    ref+=("Won't Fix")
    return
}

## --------------------------------------------------------------------
## Intent: Modify search query by ticket resolution
## --------------------------------------------------------------------
function do_resolved()
{
    declare -n ans=$1; shift
   # declare -g resolved

    [[ -v resolved_start ]] && { ans+=("(Resolved >= $resolved_start)"); }
    [[ -v resolved_end ]]   && { ans+=("(Resolved <= $resolved_end)"); }

    if [[ -v resolved_excl ]]; then
        filter="$(join_by ',' "${resolved_excl[@]}")"
        declare -p filter
        ans+=( "(resolution NOT IN ($filter))" )
    fi

    if [[ -v resolved_incl ]]; then
        filter="$(join_by ',' "${resolved_incl[@]}")"
        ans+=( "(resolution IN ($filter))" )
    fi

    [[ -v resolved_not_empty ]] && { ans+=('(resolved IS NOT EMPTY)'); }
    [[ -v resolved_is_empty ]] \
        && { ans+=('(resolved IS EMPTY)'); } \
        || { true; }

    return
}

: # ($?=0) for source $include

# [EOF]
