#!/bin/bash
## -----------------------------------------------------------------------
## Intent: Wrapper script for requesting code reviews
## -----------------------------------------------------------------------
## Usage:
##   git clone ci-management
##   cd ci-management
##     [...]
##   reviewers.sh --bat
##   reviewers.sh --tst
##   reviewers.sh --tst daf@opennetworking.org
## -----------------------------------------------------------------------

##-------------------##
##---]  GLOBALS  [---##
##-------------------##
set -euo pipefail

declare -g pgm="$(readlink --canonicalize-existing "$0")"
declare -g pgmbin="${pgm%/*}"
declare -g pgmroot="${pgmbin%/*}"
declare -g pgmname="${pgm%%*/}"

readonly pgm
readonly pgmbin
readonly pgmroot
readonly pgmname

## -----------------------------------------------------------------------
## Intent: Display an error message then exit with status
## -----------------------------------------------------------------------
function error()
{
    echo "${FUNCNAME[1]} ERROR: $*"
    exit 1
}

## -----------------------------------------------------------------------
## Intent: Display a message decorated for the calling function
## -----------------------------------------------------------------------
function func_echo()
{
    echo "${FUNCNAME[1]}: $*"
    return
}

## -----------------------------------------------------------------------
## Intent: Helper method
## -----------------------------------------------------------------------
## Usage : local path="$(join_by '/' 'lib' "${fields[@]}")"
## -----------------------------------------------------------------------
function join_by()
{
    local d=${1-} f=${2-}; if shift 2; then printf %s "$f" "${@/#/$d}"; fi;
}

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
function get_meta()
{
    local log="$1"; shift

    local -n refc=$1; shift # change id
    local -n refg=$1; shift # gerrit id
    local -n refr=$1; shift # repo

    local url
    url="$(grep '://' "$log" | grep 'remote:' | awk '{print $2}')"
    local gerrit_id="${url##*/}"

    local dir="${log%/*}"
    pushd "$dir" >/dev/null

    local revparse
    revparse="$(git rev-parse --show-toplevel)"
    local repo="${revparse##*/}"

    local change_id
    change_id="$(git log -1 | grep 'Change-Id:' | awk -F':' '{print $2}' | sed -e 's/[[:blank:]]//g')"
    declare -p change_id
    refc="$change_id"

    refc="$change_id"
    refg="$gerrit_id"
    refr="$repo"

    declare -p refc
    declare -p refg
    declare -p refr

    popd >/dev/null

    return
}

## -----------------------------------------------------------------------
## Intent: Display a message decorated for the calling function
## -----------------------------------------------------------------------
function update_meta()
{
    local log="$1"; shift
    local conf="$pgmroot/.get"
    declare -p conf

    [[ $USER != 'joey' ]] && return

    func_echo 'ENTER'

    ## Depth first traversal toward root
    ## Detect .get/ storage
    local path
    path_raw=$(realpath --canonicalize-existing '.')
    readarray -d'/' -t fields <<<"$path_raw"

    for idx in $(seq 0 $((${#fields[@]} -1)) | sort -nr);
    do
        local check="$(join_by '/' "${fields[@]:0:idx}" '.get')"
        if [[ -e "$check" ]]; then
            declare get_root="$check"
            echo "FOUND: $check"
            break
        fi
    done

    if [[ -v get_root ]]; then
        local cid=''
        local gid=''
        local rep=''

        get_meta "$log" cid gid rep

        local cpath="$get_root/change_id/$cid"
        if [[ ${#cid} -gt 0 ]] && [[ ! -e "$cpath" ]]; then
            func_echo "Create: $cpath"
            cat <<EOD>"$cpath"
#!/bin/bash

repo="${rep}"
change_id="${cid}"
gerrit_id="${gid}"

# [EOF]
EOD
        fi

        ## ----------------------------------------------
        ## ----------------------------------------------
        local gpath="$get_root/gerrit_id/$gid"
        if [[ ${#gid} -gt 0 ]] && [[ ! -e "$gpath" ]]; then
            func_echo "Create: $gpath"
            local dir="${gpath%/*}"
            pushd "$dir" >/dev/null
            ln -vfns "$gid" "../$cid"
            popd         >/dev/null
        fi
    fi

    func_echo 'LEAVE'

    return
}

## -----------------------------------------------------------------------
## Intent: --bat code review requests
## -----------------------------------------------------------------------
function get_bat_email()
{
    declare -n ref=$1; shift
    ref+=('daf@opennetworking.org')
    ref+=('joey@opennetworking.org')

    # Not paying attention to reviews atm so filter as a default
    ref+=('jan@opennetworking.org')
#    ref+=('roger@opennetworking.org')

    ## -------------------------------------------
    ## Remove exclusions from the list
    ## ie: Avoid requesting a review from yourself
    ## -------------------------------------------
    if false && [ $# -gt 0 ]; then
        declare -n __excls=$1; shift
        local __excl
        for __excl in "${__excls[@]}";
        do
            ## Hmmm ?!? single quotes causing a problem.
            ##   with - no filtering, list remains intact
            ##   w/o  - email address filtered leaving only quotes (fail!)
            ref=( "${ref[@]/$__excl/}" )
        done
    fi

    return
}

## -----------------------------------------------------------------------
## Intent: Future enhancements
## -----------------------------------------------------------------------
function todo
{
    cat <<EOT
 o Any benfit to creating aliases --adtran, --netsia, etc ?
EOT
    return
}

## -----------------------------------------------------------------------
## Intent: --bat code review requests
## -----------------------------------------------------------------------
function usage
{
    cat <<EOH

Usage: $0
  --none     Simple git review with logging

  --bat      Request infra code reviews
  --bisdn    Jan and Roger
  --tst      Request a code review from VOLTHA TST members

[TRANSIENT SWITCHES]
  --review-make   Send out requests for makefile reviewers
  --golang        Voltha golang upgrade for VGC

[DEV MODE]
  --nop      Early exit
EOH

    return
}

##----------------##
##---]  MAIN  [---##
##----------------##

# update_meta 'review_log'
# error "EARLY EXIT"

echo "$0: $*"

declare -a emails=()

declare -A ARGV=()
early_exit=0

declare -a todo=("$@")
while [[ ${#todo[@]} -gt 0 ]];
do

    val="${todo[0]}"
    unset todo[0]
    todo=("${todo[@]}") # reindex: array[1] => array[0]

    # echo "** val=[$val], todo=[${todo[@]}]"

    case "$val" in

        # --make) declare -g -i argv_review_make=1 ;;
                                                   
        -*none) declare -i ARGV['none']=1; ;;
        --help) usage; exit 0 ;;

        --review-make)
            todo+=('--bat')
            todo+=('--mahir')
            ;;

        --golang) # reviewers for 
            todo+=('--abhilash')
            todo+=('--mahir')
            todo+=('--sridhar')
            ;;

        -*help) usage; exit 0  ;;
        -*nop) early_exit=1    ;;
        -*todo*)  todo         ;;
        -*early*) early_exit=1 ;;

        -*bat|-*infra)
            todo+=('--daf')
            todo+=('--joey')
            ;;

        -*bisdn*)
            todo+=('--jan')
            todo+=('--roger')
 #           todo+=('--christina')
            ;;

        ## users
        --abhil*)    emails+=('abhilash.laxmeshwar@radisys.com') ;;
        --amit)      emails+=('amit.ghosh@radisys.com')          ;;

        --burak)     emails+=('burak.gurdag@netsia.com')         ;;
        
        -*daf)       emails+=('daf@opennetworking.org')          ;;
        -*gustavo)   emails+=('gsilva@furukawalatam.com')        ;;
        #   -*holger)  emails+=('holger.hildebrandt@adtran.com') ;;

        ## Linux Foundation
        --jess*)     emails+=('jwagantall@linuxfoundation.org')  ;;
        --thanh)     emails+=('thanh.ha@linuxfoundation.org')    ;;  
      
        # Mirko Deckert -- voltha-onos
        -*mirko*)    emails+=('mirko.deckert@adtran.com')        ;;
        

        -*joey)      emails+=('joey@opennetworking.org')         ;;
        -*larry)     emails+=('llp@opennetworking.org')          ;;
        -*mahir)     emails+=('mahir.gunyel@netsia.com')         ;;
        -*nikesh)    emails+=('tesseract12345678@gmail.com')     ;;
        -*serkant)   emails+=('serkant.uluderya@netsia.com')     ;;
        -*sridhar)   emails+=('sridhar.ravindra@radisys.com')    ;;

 
        #   -*torsten) emails+=('torsten.thieme@adtran.com')     ;;
        -*vinod)   emails+=('vinod.kumar@radisys.com')           ;;
        #   -*zack)    emails+=('zack.williams@intel.com')       ;;

        -*tst*)
            todo+=('--abhilash')
            todo+=('--amit')
            todo+=('--burak')
            todo+=('--mahir')
            todo+=('--serkant')
            ;;
 
        --christina) emails+=('cristina@opennetworking.org')     ;;
        --jan)       emails+=('jan@opennetworking.org')          ;;
        --roger)     emails+=('roger@opennetworking.org')        ;;
       
        *@*) emails+=("$val") ;;

        *)
            echo "ERROR: Unknown reviewer [$val]"
            exit 1
            ;;
    esac
done


declare -a reviewers=()
for email in "${emails[@]}";
do
    reviewers+=("'$email'")
done

[[ ${#reviewers[@]} -gt 0 ]] \
    && declare -p reviewers \
        | grep '@' \
        | tr ' ' '\n'

declare -a review_args=()
if [ $early_exit -gt 0 ]; then
    echo "[DEUBG] git review --reviewers ${reviewers[@]} [--work-in-progress]"

elif [[ -v ARGV['none'] ]]; then
    echo "** Running in dev mode"
    :
elif [[ ${#reviewers[@]} -eq 0 ]]; then
    usage
    error "At least one reviewer is required"
else
    review_args+=('--reviewers' "${reviewers[@]}")
fi

set -x
git review "${review_args[@]}" 2>&1 | tee review.log
set +x
update_meta "$(realpath --canonicalize-existing 'review.log')"

# [EOF]
