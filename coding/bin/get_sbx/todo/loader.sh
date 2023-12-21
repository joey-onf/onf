#!/bin/bash

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
function __anonymous()
{
    readarray -t srcs < <(find "$pgm_root/get_sbx/todo" -name '*.sh' -print \
                              | grep -v 'loader.sh')
    for src in "${srcs[@]}";
    do
        source "$src"
    done

    return
}

__anonymous
unset __anonymous

# [EOF]
