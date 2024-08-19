#!/bin/bash
## -----------------------------------------------------------------------
## Intent: This script can be run after an EC2 AMI has been created
##         to configure the instance for use as a jenkins node.
## -----------------------------------------------------------------------

umask 022

declare -g user_home='/home/jenkins'
# readarray user_home
declare -g user_home_ssh="${user_home}/.ssh"
# readarray user_home_ssh

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
## Intent: Display an error message then exit
## -----------------------------------------------------------------------
function banner()
{
    cat <<EOF

** -----------------------------------------------------------------------
** IAM: ${BASH_SOURCE[0]} (LINENO:${BASH_LINENO[@]})
** $@
** -----------------------------------------------------------------------
EOF
    return
}

## -----------------------------------------------------------------------
## Intent: Display an error message then exit
## -----------------------------------------------------------------------
function status()
{
    [[ $# -eq 0 ]] && { set -- ''; }
    printf '** %s: %s\n' "${FUNCNAME[0]}" "$@"
    return
}

## -----------------------------------------------------------------------
## Intent: Display an error message then exit
## -----------------------------------------------------------------------
function enter()
{
    [[ $# -eq 0 ]] && { set -- ''; }
    printf '** [ENTER] %s: %s\n' "${FUNCNAME[0]}" "$@"
    return
}

## -----------------------------------------------------------------------
## Intent: Display an error message then exit
## -----------------------------------------------------------------------
function leave()
{
    [[ $# -eq 0 ]] && { set -- ''; }
    printf '** [LEAVE] %s: %s\n' "${FUNCNAME[0]}" "$@"
    return
}

## -----------------------------------------------------------------------
## Intent: Install packages for 18.04 use as jenkins nodes.
## -----------------------------------------------------------------------
function install_packages()
{
    banner "${FUNCNAME[0]}"
    enter
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
        for package in "${packages[@]}";
        do
            status "PACKAGE: $package"
            sudo apt-get install -y "$package"
        done
        
    done
    leave
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
    banner "${FUNCNAME[0]}"
    enter
    readarray -t version < <(lsb_release -sr 2>/dev/null) # 24.04

    case "${version[*]}" in
        *'24.04'*) ;; # fall through
        *'18.04'*)
            apt_upgrade_180406lts
            return
            ;;
    esac

    echo "** (LINENO:$LINENO) detected $(declare -p version)"
    sudo apt-get update
    sudo apt-get -y upgrade
    sudo apt-get -y dist-upgrade

    leave
    return
}

##----------------##
##---]  MAIN  [---##
##----------------##
# apt_upgrade_180406lts
apt_upgrade
install_packages
sudo ami/jenkins.sh # create_jenkins()
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


cat <<EOM

** -----------------------------------------------------------------------
** Post install checklist
** -----------------------------------------------------------------------

  o Logout & relogin so docker group membership becomeds visibile.
  o docker run -it ubuntu bash
  o sudo docker run hello-world
EOM

#    # groups | grep docker
 #   echo '[NOTE]
    

# [EOF]

