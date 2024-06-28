#!/bin/bash
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------

function install_python()
{
    apt-get install -y python3.6
    apt-get install -y python3.7
    apt-get install -y python3.8
    
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 3

#    update-alternatives auto python3 # selects python3.8
    return
}

: # assign ($?=0) for source $script

# [EOF]
