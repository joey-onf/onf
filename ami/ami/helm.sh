#!/bin/bash
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------

## -----------------------------------------------------------------------
## Intent: Configure apt for helm install
## -----------------------------------------------------------------------
##   Note: curl installation is a better option to avoid surprise upgrade
##         breakage, external dependencies, etc.  Convenience is worth
##         it for image prototyping.
## -----------------------------------------------------------------------
function helm_apt_install()
{
    curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
    sudo apt-get install apt-transport-https --yes
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
    sudo apt-get update
    sudo apt-get install helm
    return
}

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
function install_helm()
{
    helm_apt_install
    # helm_alternatives
}

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
function install_helm_no_deps()
{
    local opt_helm='/opt/helm'
    local dst="${opt_helm}/3.5.2"
    local tgz='helm-v3.5.2-linux-amd64.tar.gz'

    mkdir -p "$opt_helm"
    chown -R nobody:nogroup "$opt_helm"
    pushd "$path" 2>/dev/null || { error 'pushd /opt/helm failed'; }

    ## -----------------------------------------------------
    ## /usr/local/bin/helm may already be installed: v3.15.4
    ## -----------------------------------------------------
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
    chmod 700 get_helm.sh
    ./get_helm.sh
    
#    curl -o "${tgz}" \
#         --url https://get.helm.sh/helm-v3.5.2-linux-amd64.tar.gz
#    tar zxvf "${tgz}"
#    mv 'linux-amd64' "$dst"
    popd 2>/dev/null              || { error 'popd /opt/helm failed'; }

    chown -R nobody:nogroup "$opt_helm"
    rm -f "${tgz}"
    
    
    # --install link name path priority [--slave link name path]...

    sudo update-alternatives --install /usr/bin/helm helm /opt/helm/3.15.3/helm  99
    sudo update-alternatives --install /usr/bin/helm  helm /opt/helm/3.5.2/helm  1
    sudo update-alternatives --auto helm # selects helm v3.15.3

    return
}

: # assign ($?=0) for source $script

# [EOF]
