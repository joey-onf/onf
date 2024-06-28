#!/bin/bash
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------

function install_golang()
{
    apt-get install -y golang-1.16
    apt-get install -y golang-1.18
    # wanted: golang-1.17.10

# /usr/lib/go-1.16/bin/gofmt
    for version in '1.16' '1.18';
    do
        # sudo update-alternatives --install <link> <name> <path> <priority>
        local bin="/usr/lib/go-${version}/bin"
        update-alternatives --install /usr/bin/go    go    "${bin}/go" 1
        update-alternatives --install /usr/bin/gofmt gofmt "${bin}/gofmt" 1
    done

    return
}

# install_golang # standalone script

# Highest priority (0) is auto, change priority to augment command
# update-alternatives --display go
# update-alternatives --auto go


: # assign ($?=0) for source $script

# [EOF]
