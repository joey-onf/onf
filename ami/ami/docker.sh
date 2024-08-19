#!/bin/bash
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------

function docker_package_rm()
{
    local pkg
    for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
    return
}

## -----------------------------------------------------------------------
## Intent: Install the docker command
## -----------------------------------------------------------------------
function docker_apt_install()
{
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update


    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    
    return
}

## -----------------------------------------------------------------------
## Intent: Install the docker command
## -----------------------------------------------------------------------
function docker_verify()
{

    cat <<EOM

** -----------------------------------------------------------------------
** [NOTE] docker run hello-world must succeed
** -----------------------------------------------------------------------
EOM
    sudo docker run hello-world

    return
}

## -----------------------------------------------------------------------
## Intent: Install the docker command
## -----------------------------------------------------------------------
function install_docker()
{
    docker_package_rm
    docker_apt_install
    docker_verify
    return
}

## -----------------------------------------------------------------------
## Intent: Destructive removal of docker and friends
## -----------------------------------------------------------------------
function docker_uninstall()
{
    sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras

    sudo rm -rf /var/lib/docker
    sudo rm -rf /var/lib/containerd
    return
}

## -----------------------------------------------------------------------
## Intent: Install the docker command
## -----------------------------------------------------------------------
function install_docker_orig()
{
    banner "${FUNCNAME[0]}"
    enter

    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    ## Configure apt
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    sudo apt-get update
    # apt-get install docker

    declare -a pkgs=()
    # https://docs.docker.com/engine/install/ubuntu/
    if false; then
        pkgs+=('docker.io')
        pkgs+=('docker-registry')
        pkgs+=('docker-doc')
    else
        for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

        pkgs+=('containerd.io')    # - An open and reliable container runtime
        pkgs+=('containerd')       # - daemon to control runC
    fi
    

    
#    printf '\n** Fixing docker guid to match jenkins for building'
#    groupmod -g 998 docker

    leave
    return
}

: # assign ($?==0) for source $script

# [EOF]

