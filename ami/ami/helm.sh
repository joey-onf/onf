#!/bin/bash
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------

function install_helm()
{
    local opt_helm='/opt/helm'
    local dst="${opt_helm}/3.5.2"

    mkdir -p "$opt_helm"
    chown -R nobody:nogroup "$opt_helm"
    pushd "$path" 2>/dev/null || { error 'pushd /opt/helm failed'; }

    curl -o 'helm-v3.5.2-linux-amd64.tar.gz' \
         --url https://get.helm.sh/helm-v3.5.2-linux-amd64.tar.gz
    tar zxvf 'helm-v3.5.2-linux-amd64.tar.gz'
    mv 'linux-amd64' "$dst"
    popd 2>/dev/null              || { error 'popd /opt/helm failed'; }

    chown -R nobody:nogroup "$opt_helm"

    
    
    # --install link name path priority [--slave link name path]...

    sudo update-alternatives --install /usr/bin/helm helm /opt/helm/3.15.3/helm  99
    sudo update-alternatives --install /usr/bin/helm  helm /opt/helm/3.5.2/helm  1
    sudo update-alternatives --auto helm # selects helm v3.15.3

    return
}

: # assign ($?=0) for source $script

# [EOF]
