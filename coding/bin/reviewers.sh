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

	get_meta $(realpath 'review.log') cid gid rep

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
    ref+=('roger@opennetworking.org')

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
  --bat      Request infra code reviews
  --bisdn    Jan and Roger
  --tst      Request a code review from VOLTHA TST members

  --none     Simple git review with logging

[DEV MODE]
  --nop      Early exit
EOH

    return
}

##----------------##
##---]  MAIN  [---##
##----------------##

update_meta 'review_log'
error "EARLY EXIT"

echo "$0: $*"

declare -a emails=()

declare -A ARGV=()
early_exit=0
for val in "$@";
do
    case "$val" in

	-*none) declare -i ARGV['none']=1; ;;

	-*help) usage; exit 0  ;;
	-*nop) early_exit=1    ;;
	-*todo*)  todo         ;;
	-*early*) early_exit=1 ;;

	-*abhil*)  emails+=('abhilash.laxmeshwar@radisys.com')   ;;
	
	-*bat|-*infra)
	    declare -a bat=()
	    declare -a excl=()
	    case "$USER" in
		# Avoid requesting from yourself
		daf|jan|joey|roger)
		    excl+=("${USER}@opennetworking.org")
		    get_bat_email bat excl
		    ;;
		*)
		    get_bat_email bat
		    ;;
	    esac
	    emails+=("${bat[@]}")
	    ;;

	-*bisdn*)
	    emails+=('jan@opennetworking.org')
	    emails+=('roger@opennetworking.org')                 ;;
		    
	-*daf)     emails+=('daf@opennetworking.org')            ;;
	-*gustavo) emails+=('gsilva@furukawalatam.com')          ;;
#	-*holger)  emails+=('holger.hildebrandt@adtran.com')     ;;
	-*joey)    emails+=('joey@opennetworking.org')           ;;
	-*mahir)   emails+=('mahir.gunyel@netsia.com')           ;;
        -*serkant) emails+=('serkant.uluderya@netsia.com')       ;;	
#	-*torsten) emails+=('torsten.thieme@adtran.com') ;;
	-*vinod)   emails+=('vinod.kumar@radisys.com')           ;;
#	-*zack)    emails+=('zack.williams@intel.com')           ;;

        -*tst*)
	    emails+=('amit.ghosh@radisys.com')
	    emails+=('mahir.gunyel@netsia.com')
            emails+=('serkant.uluderya@netsia.com')
	    emails+=('abhilash.laxmeshwar@radisys.com')
	    emails+=('burak.gurdag@netsia.com')
	    ;;

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
    echo "[DEUBG] git review --reviewers ${reviewers[@]}"

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
update_meta 'review_log'
    

# [EOF]

# remote: 
# remote: Processing changes: (\)        
# remote: Processing changes: (|)        
# remote: Processing changes: (/)        
# remote: Processing changes: (-)        
# remote: Processing changes: (\)        
# remote: Processing changes: (|)        
# remote: Processing changes: (/)        
# remote: Processing changes: (-)        
# remote: Processing changes: (\)        
# remote: Processing changes: refs: 1, new: 1 (\)        
# remote: Processing changes: refs: 1, new: 1 (\)        
# remote: Processing changes: refs: 1, new: 1 (\)        
# remote: Processing changes: refs: 1, new: 1, done            
# remote: commit bd9673f: warning: subject >50 characters; use shorter first paragraph        
# remote: 
# remote: SUCCESS        
# remote: 
# remote:   https://gerrit.opencord.org/c/voltha-lib-go/+/34417 [VOL-5053] - Pre-release triage build of voltha-lib-go [NEW]        
# remote: 
# To ssh://gerrit.opencord.org:29418/voltha-lib-go.git
#  * [new reference]   HEAD -> refs/for/master%topic=dev-joey
# #!/bin/bash
# 
# changeid="$(git log -1 | grep 'Change-Id:' | awk -F: '{print $2}')"
# declare -p changeid
# 
# # remote:   https://gerrit.opencord.org/c/voltha-lib-go/+/34417 [VOL-5053] - Pre-release triage build of voltha-lib-go [NEW]        
# 
# url="$(grep '://' review.log | grep 'remote:' | awk '{print $2}')"
# gerrit_id="${url##*/}"
# 
# revparse="$(git rev-parse --show-toplevel)"
# repo="${revparse##*/}"
# 
# # $sbx/.get
# # $sbx/.get/change_id/{xxxx}
# # --------------------------
# # #!/bin/bash
# # 
# # repo="ci-management"
# # change_id="I09385c0544221cc87839b5182200977e0571039a"
# # gerrit_id="33686"
# #
# # # [EOF]
# 
# # $sbx/.get/change_id/gerrit_id
# # -----------------------------
# #   o symlink to change_id 
# 
# # EOF
