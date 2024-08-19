#!/bin/bash
## -----------------------------------------------------------------------
## Intent: Install python dependencies
## -----------------------------------------------------------------------

## -----------------------------------------------------------------------
## Intent: Install dependencies for systemd service: networkd-dispatcher
## https://pygobject.gnome.org/getting_started.html
## -----------------------------------------------------------------------
function networkd_dispatcher_deps()
{
    apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0

    apt-get install python-gi-dev python-gobject-2-dev python-gtk2 

    apt-get install --reinstall networkd-dispatcher

    
    return
}

## -----------------------------------------------------------------------
## Intent: Install the interpreter and configure alternative defaults
## -----------------------------------------------------------------------
function install_python_interpreter()
{
    apt-get install -y python3.6
    apt-get install -y python3.7
    apt-get install -y python3.8
    
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 3
    update-alternatives auto python3 # selects python3.8
    update-alternatives --display python3

    
    # 3.7-config not installed by libpython-3.7-dev
    # update-alternatives --install /usr/bin/python-config python-config /usr/bin/python3.7-config 37
    update-alternatives --install /usr/bin/python-config python-config /usr/bin/python3.6-config 36
    update-alternatives --install /usr/bin/python-config python-config /usr/bin/python3.8-config 38
    update-alternatives auto python-config # selects 3.8
    update-alternatives --display python-config
    
    return
}

## -----------------------------------------------------------------------
## Intent: Configure apt to install older interpreter versions
## -----------------------------------------------------------------------
function python_configure_apt()
{
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt-get update
    return
}

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
function install_python()
{
    readarray -t version < <(lsb_release -sr 2>/dev/null)

    python_configure_apt
    
    case "${version[*]}" in
        *'24.04'*)
            declare -a pkgs=()
            pkgs+=('python3.7')
            pkgs+=('python3.7-dev')
            pkgs+=('python3.7-venv')
            pkgs+=('libpython3.7')
            pkgs+=('libpython3.7-dev')

            pkgs+=('python3.8')
            pkgs+=('python3.8-dev')
            pkgs+=('python3.8-venv')
            pkgs+=('libpython3.8')
            pkgs+=('libpython3.8-dev')

            sudo apt-get install "${pkgs[@]}"
            ;;
        
        *'18.04'*)
            install_python_interpreter
            networkd_dispatcher_deps
            ;;
    return
}
: # assign ($?=0) for source $script

# [EOF]
