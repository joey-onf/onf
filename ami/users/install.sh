#!/bin/bash
## -------------------------------------------------
## Intent: Bash builtins for filesystem path parsing
## -------------------------------------------------

##-------------------##
##---]  GLOBALS  [---##
##-------------------##
umask 0
set -euo pipefail


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
function error()
{
    cat <<EOF

** -----------------------------------------------------------------------
** IAM: ${FUNCNAME[1]}
** ERR: $@
** -----------------------------------------------------------------------
EOF

    exit 1
}

## -----------------------------------------------------------------------
## Intent: Parse command line paths
## -----------------------------------------------------------------------
function program_paths()
{
    declare -g pgm="$(readlink --canonicalize-existing "$0")"
    declare -g pgmbin="${pgm%/*}"
    declare -g pgmroot="${pgmbin%/*}"
    declare -g pgmname="${pgm%%*/}"

    declare -g pgmsrc
    pgmsrc="$(readlink --canonicalize-existing "${BASH_SOURCE[0]}")"
    readonly pgmsrc

    readonly pgm
    readonly pgmbin
    readonly pgmroot
    readonly pgmname

    declare -g start_pwd="$(realpath --canonicalize-existing '.')"
    readonly start_pwd
}

## -----------------------------------------------------------------------
## Intent: Parse command line paths
## -----------------------------------------------------------------------
function create_user()
{
    local user="$1"; shift

    declare -a args=()
    case "$(hostname)" in

        # different adduser syntax
        'aws-us-west-2-cord-jenkins-1.opencord.org')
            local -i relay_host=1
            ;;
    esac

    if [[ -v argv_login ]]; then
        : # --password [p] w/o exposing string
#    else
#        args+=('--disabled-login')
   fi

    
    if grep "^${user}:$" /etc/passwd; then
        : # NOP if exists

    elif [[ -v relay_host ]]; then
        args+=('--no-user-group')

    elif [[ -v argv_login ]]; then
        local -i passwd_expire=1

    else
        args+=('--shell' '/sbin/nologin')
        : # login disabled
    fi    

    adduser "${args[@]}" "$user"
    [[ -v passwd_expire ]] && { passwd --expire "$user"; }

    ## -----------------------------
    ## Display credential attributes
    ## -----------------------------
    cat <<EOM

** Account expiration attributes
** -----------------------------------------------------------------------
chage -l "${user}"
** -----------------------------------------------------------------------

EOM
    
    return
}

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
function pass_gen()
{
    local fyl="$1"; shift

    local -i passlen=12
    return
}

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
function gen_ssh()
{
    local user="$1"; shift
    local key="$1"; shift

    local home="/home/${user}"
    local ssh="${home}/.ssh"
    local auth="${ssh}/authorized_keys"
    local known="${ssh}/known_hosts"

    [[ ! -d "$home" ]] && { error "path [$home] does not exist"; }
    [[ -f "$auth" ]] && { return; } # exists

    echo "** ${FUNCNAME[0]}: init ~/.ssh"

    mkdir -p "${ssh}"
    touch "$auth"
    cp "$key" "${key}.bak"
    cat "$key" "$auth" | sort -u > "${auth}.tmp"

    echo "** ${FUNCNAME[0]}: Install user keys into: $auth"
    install -C -m 0400 -o "$user" -g "$user" "${auth}.tmp" "$auth"

    echo "** ${FUNCNAME[0]}: Touch $known"
    touch "$known"
    chmod 0600 "$known"

    echo "** ${FUNCNAME[0]}: Fix perms beneath $ssh"
    chmod -R og-rwx "$ssh"
    chown -R "${user}:${user}" "$ssh"
    return
}

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
function sudo_user()
{
    local user="$1"; shift
    local path="/etc/sudoers.d/10-${user}"

    if [[ ! -f "$path" ]]; then
        echo "** ${FUNCNAME[0]}: create $path"
        echo "${user} ALL=(ALL) NOPASSWD:ALL" >> "$path"
    fi
    chmod 0440 "$path"
    
    return
}

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
function usage()
{
    [[ $# -gt 0 ]] && { printf "ERROR: $@\n" "$@"; }

    cat <<EOF

% usage $0:
  ./install.sh --create --sudo --user {user} --key ./{user}-rsa.pub

    --create                         Create a user account (--user xxx)
    --key                            Install public ssh key for user.
    --login                          Generate a password for user else disabled
    --sudo                           Configure user for sudo access.
    --user-disabled                  Create user account but no shell access.
EOF
    return
}

##----------------##
##---]  MAIN  [---##
##----------------##
program_paths

declare -a action=()

while [[ $# -gt 0 ]]; do
    arg=$1; shift

    echo "ARGV=[$arg]"
    case "$arg" in
        '--help') usage; exit 0 ;;
        
        '--create') declare -i argv_create=1 ;;
        '--key') declare argv_key="$1"; shift ;;

	    '--login')
            declare -g argv_login='foo'
            echo > "$argv_login"
            chmod og-rwx "$argv_login"
            # openssl rand -base64 48 | cut -c1-${passlen}
            # gpg --gen-random --armor 1 14
            openssl rand -base64 14 >> "$argv_login"
            ;;
        
        '--ssh') declare argv_ssh="$1"; shift ;;
        '--sudo') declare -i argv_sudo=1 ;;

        '--user') declare argv_user="$1"; shift ;;
#        '--user-disabled') declare argv_user_disabled="$1"; shift ;;
        *) echo "[SKIP] unknown argument [$arg]" ;;
    esac
    
done

[[ -v argv_create ]] && { action+=('create'); }
[[ -v argv_ssh    ]] && { action+=('ssh');    }
[[ -v argv_sudo   ]] && { action+=('sudo');   }

[[ ! -v argv_user ]] && { error "--user is required"; }
[[ -v argv_create ]] && { create_user "$argv_user"; }

declare homedir="/home/${argv_user}"
if [[ ! -d "${homedir}/." ]]; then
    error "--create required to adduser [$argv_user]"
fi

if [[ -v argv_ssh ]]; then
    [[ ! -v argv_key ]]    && { error "--key is required"; }
    [[ ! -f "$argv_key" ]] && { error "--key $argv_key is not a file"; }
    gen_ssh "$argv_user" "$argv_key"
fi

[[ -v argv_sudo   ]] && { sudo_user "$argv_user"; }


echo '[FIN]'

# [EOF]
