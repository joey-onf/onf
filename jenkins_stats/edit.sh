#!/bin/bash

declare -a fyls=()
fyls+=( $(find stats/spreadsheet -name '*.py' -print) )
fyls+=('jenkins_stats.py')

~/etc/emacs "${fyls[@]}" &

# [EOF]

