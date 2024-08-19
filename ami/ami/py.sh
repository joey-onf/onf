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

    apt-get install python3-gi-dev python-gobject-2-dev python-gtk2 

    apt-get install --reinstall networkd-dispatcher

    
    return
}

## -----------------------------------------------------------------------
## Intent: Install the interpreter and configure alternative defaults
## -----------------------------------------------------------------------
function install_python_interpreter()
{

    printf "[%s::SKIP] Modifying system python version will cause problems\n" \
	   "${FUNCNAME[0]}"
    return

    
#    apt-get install -y python3.6
#    apt-get install -y python3.7
    apt-get install -y python3.8
    
#    update-alternatives --install /usr/bin/lf-python python3 /usr/bin/python3.6 1
#    update-alternatives --install /usr/bin/lf-python python3 /usr/bin/python3.7 2
    update-alternatives --install /usr/bin/lf-python python3 /usr/bin/python3.8 3
    update-alternatives auto python3 # selects python3.8
    update-alternatives --display python3

    
    # 3.7-config not installed by libpython-3.7-dev
    # update-alternatives --install /usr/bin/python-config python-config /usr/bin/python3.7-config 37
#    update-alternatives --install /usr/bin/python-config python-config /usr/bin/python3.6-config 36
    update-alternatives --install /usr/bin/python-config python-config /usr/bin/python3.8-config 38
    update-alternatives auto python-config # selects 3.8
    update-alternatives --display python-config
    
    return
}

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
function install_python()
{
    install_python_interpreter
    networkd_dispatcher_deps
    return
}
: # assign ($?=0) for source $script

# [EOF]
