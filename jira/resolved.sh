#!/bin/bash

declare -a args=()
args+=('--project' 'SEBA')
args+=('--project' 'VOL')

args+=('--opencord')
args+=('--resolved-start' '2022-12-31')
args+=('--resolved-end'   '2024-12-3'1)

args+=('--resolved-excl'  "Duplicate")
args+=('--resolved-excl'  "Won't Do")
args+=('--resolved-excl'  "Won't Fix")

args+=('--resolved-not-empty')

# args+=('--fixversion-excl'  'VOLTHA v2.13')
args+=('--fixversion-is-empty')
# args+=('--unresolved')

jira-search.sh "${args[@]}"

# [EOF]
