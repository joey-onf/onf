#!/bin/bash

## --------------------------------------------------------------------
## Intent: Retrieve a list of reason query strings
## --------------------------------------------------------------------
function get_jql_fixversion()
{
    local -n ref=$1; shift

    ref+=('VOLTHA-v2.12')
    return
}

## --------------------------------------------------------------------
## Intent: Modify search query by release fix version string
## --------------------------------------------------------------------
function do_fixversion()
{
    declare -n ans=$1; shift
    declare -g fixversion

    if [[ -v fixversion_excl ]]; then
        filter="$(join_by ',' "${fixversion_excl[@]}")"
        ans+=("(fixVersion NOT IN ($filter))")
    fi
    
    if [[ -v fixversion_incl ]]; then
        filter="$(join_by ',' "${fixversion_incl[@]}")"
        ans+=("(fixVersion IN ($filter))")
    fi

    [[ -v fixversion_not_empty ]] && { ans+=('(fixVersion IS NOT EMPTY)'); }
    [[ -v fixversion_is_empty ]] \
        && { ans+=('(fixversion IS EMPTY)'); } \
        || { true; }

    return
}

: # ($?=0) for source $include

# [EOF]
