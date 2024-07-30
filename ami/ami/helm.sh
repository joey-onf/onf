#!/bin/bash
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------

function install_helm()
{
    # --install link name path priority [--slave link name path]...

    update-alternatives --install /usr/bin/helm helm /opt/helm/3.15.3/helm  99
    update-alternatives --install /usr/bin/helm  helm /opt/helm/3.5.2/helm  1
    update-alternatives --auto helm # selects helm v3.15.3

    return
}

: # assign ($?=0) for source $script

# [EOF]
