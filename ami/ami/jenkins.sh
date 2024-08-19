#!/bin/bash
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------

## -----------------------------------------------------------------------
## Intent: Install the docker command
## -----------------------------------------------------------------------
function add_to_groups()
{
    usermod -a -G docker jenkins

    ## Add user ubuntu as well for local builds
    usermod -a -G docker ubuntu
    return
}

## -----------------------------------------------------------------------
## Intent: Install jenkins pub key as authorized
## -----------------------------------------------------------------------
function create_authorized_keys()
{
    local dir="$user_home_ssh"
    local auth_keys='authorized_keys'
    local auth_temp="${auth_keys}.temp"

    install -d -m 700 "$dir"
    cat <<EOKEY >"$auth_temp"
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCjsJjHzCzpcbyt1ik3DYfyO2DUUlhd+OpFprlIO+ntRfSect+qQQXcXSjrjHkckpg+t7v3fdIx2tjAlof1thGGxluwrddATjs8JYHzNa/x+4RZm35r14JQCgFFCU9J4a965TCcy2+PvMVzCTXv39ozAgKPZkkMzhMZPF2YpS1WOTJfSLXxwZinorcVbUzZSA6mldaTuwHFMpbD8hqzdD2CWO0TXQDKxxsjCpkifgspHC1viANsXBTf61WKyh46YH87dZJ/fmHvYau4OSiD/SqpWrACc1HvMEoitDqYBiRQnReR+VTlplgD1IUfizMMhoL/cmHxa6HFss29iGEXjr/n jenkins@jenkins.opencord.org
EOKEY

    install -m 400 --target-directory="$dir" "$auth_temp" "$auth_keys"
    /bin/rm -f "$auth_temp"

    return
}

## -----------------------------------------------------------------------
## Intent: Create user jenkins
## -----------------------------------------------------------------------
function create_jenkins()
{
    enter
    declare -a args=()
    # args+=('--disable-login')
    args+=('--disabled-password')
    args+=('--shell' '/bin/bash')

    create_authorized_keys
    leave
    return
}

: # assign ($?=0) for source $script

# [EOF]


