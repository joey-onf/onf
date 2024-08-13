#!/bin/bash

declare -a args=()
args+=('-o' 'ServerAliveInterval=5')
args+=('-o' 'ServerAliveCountMax=1')

host='jenkins.opencord.org'
ssh "${args[@]}" "$host"

# [EOF]
