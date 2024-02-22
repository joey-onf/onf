#!/bin/bash

## -----------------------------------------------------------------------
## Intent: Parse command line paths
## -----------------------------------------------------------------------
function program_paths()
{
    declare -g pgm="$(readlink --canonicalize-existing "$0")"
    declare -g pgmbin="${pgm%/*}"
    declare -g pgmlib="${pgmbin}/jira-search"

    readonly pgm
    readonly pgmbin
    readonly pgmlib
    return
}
program_paths
           
: # ($?=0) for source $include

# [EOF]
