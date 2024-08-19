#!/bin/bash
## -----------------------------------------------------------------------
## Intent: This script can be run after an EC2 AMI has been created
##         to configure the instance for use as a jenkins node.
## -----------------------------------------------------------------------

umask 022

declare -g user_home='/home/jenkins'
readarray user_home
declare -g user_home_ssh="${user_home}/.ssh"
readarray user_home_ssh

source ami/docker.sh
source ami/python.sh
source ami/jenkins.sh

## -----------------------------------------------------------------------
## Intent: Display an error message then exit
## -----------------------------------------------------------------------
function error()
{
    cat <<EOF

** -----------------------------------------------------------------------
** IAM: ${BASH_SOURCE[0]} (LINENO:${BASH_LINENO[@]})
** ERR: $@
** -----------------------------------------------------------------------
EOF
    exit 1
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
    declare -a args=()
    # args+=('--disable-login')
    args+=('--disabled-password')
    args+=('--shell' '/bin/bash')

    create_authorized_keys
    add_to_groups
    return
}

## -----------------------------------------------------------------------
## Intent: Install packages for 18.04 use as jenkins nodes.
## -----------------------------------------------------------------------
function install_packages()
{
    readarray -t configs < <(find . -name '*.pkg' -print)
    declare -p configs
    
    for config in "${configs[@]}";
    do
        echo "** PACKAGES: $(declare -p config)"
        readarray -t packages < <(\
                                  grep '[a-z]' "$config" \
                                      | cut -d'#' -f1 \
                                      | grep '[[:alnum:]]'
        )

        local package
        for packge in "${packages[@]}";
        do
            apt-get install -y "$package"
        done
        
    done
    return
}

## -----------------------------------------------------------------------
## Intent: upgrade base distribution to the latest 18.04 LTS release
## -----------------------------------------------------------------------
## NOTE: DO NOT INSTALL THIS UPGRADE
##   New release '20.04.6 LTS' available.
##   Run 'do-release-upgrade' to upgrade to it.
## -----------------------------------------------------------------------
function apt_upgrade_180406lts()
{
    lsb_release -a
    # https://askubuntu.com/questions/1461235/how-to-upgrade-from-ubuntu-18-04-1-lts-to-ubuntu-18-04-6-lts

    apt-get update
    apt-get -y upgrade
    apt-get -y dist-upgrade

    local lts_release='Ubuntu 18.04.6 LTS'
    readarray -t release < <(lsb_release -a)
    if [[ ! "${release[@]}" =~ *"$lts_release"* ]]; then
        lsb_release -a
        error "Release version not found: ($lts_release)"
    fi

    return
}

## -----------------------------------------------------------------------
## Intent: upgrade base distribution to the latest 18.04 LTS release
## -----------------------------------------------------------------------
## NOTE: DO NOT INSTALL THIS UPGRADE
##   New release '20.04.6 LTS' available.
##   Run 'do-release-upgrade' to upgrade to it.
## -----------------------------------------------------------------------
function apt_upgrade()
{
    readarray -t version < <(lsb_release -sr 2>/dev/null) # 24.04

    case "${version[*]}" in
        *'24.04'*) ;; # fall through
        *'18.04'*)
            apt_upgrade_180406lts
            return
            ;;
    esac

    echo "** (LINENO:$LINENO) detected $(declare -p version)"
    apt-get update
    apt-get -y upgrade
    apt-get -y dist-upgrade
    return
}

##----------------##
##---]  MAIN  [---##
##----------------##
# apt_upgrade_180406lts
apt_upgrade
install_packages
create_jenkins
install_docker

## TODO: Download helm packages and copy into /opt/helm/{version}
if true; then
    echo '[SKIP] install_helm: Manual installation needed'
else
    install_helm
fi

## TODO: Download helm packages and copy into /opt/helm/{version}
if true; then
    echo '[SKIP] install_python: Manual installation needed'
else
    install_python
fi

# [EOF]

