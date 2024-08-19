#!/bin/bash
## -----------------------------------------------------------------------
## Intent: This script will initialize a pristine AMI image for
## for use as a Broadband jenkins node.
## -----------------------------------------------------------------------
 
function checkout_sandbox()
{
    declare -a dirs=()
    dirs+=('/sandbox/etc')
   
    sudo mkdir -p "${dirs[@]}"
    sudo chown -R ubuntu:ubuntu /sandbox
    
    cd /sandbox
    git clone https://github.com/joey-onf/onf.git
    cp onf/ami/etc/checkout_repo.mk makefile
    return
}

function install_packages()
{
    declare -a pkgs=()
    pkgs+=('lsb-release')
    sud oapt-get install -y "${pkgs[@]}"

    return
}

if [[ -d '/sandbox' ]]; then
    echo '[SKIP] AMI already initialized'
else
    checkout_sandbox
    install_packages
fi

lsb_release -sr 2>/dev/null 		# 24.04

# [EOF]
