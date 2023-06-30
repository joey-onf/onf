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

set -euo pipefail

## -----------------------------------------------------------------------
## Intent: --bat code review requests
## -----------------------------------------------------------------------
function get_bat_email()
{
    declare -n ref=$1; shift
    ref+=('daf@opennetworking.org')
    ref+=('jan@opennetworking.org')
    ref+=('joey@opennetworking.org')
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

[DEV MODE]
  --nop      Early exit
EOH

    return
}

##----------------##
##---]  MAIN  [---##
##----------------##
declare -a emails=()

early_exit=0
for val in "$@";
do
    
    case "$val" in

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

declare -p reviewers \
    | grep '@' \
    | tr ' ' '\n'

if [ $early_exit -gt 0 ]; then
    echo "[DEUBG] git review --reviewers ${reviewers[@]}"
else
    set -x
    git review --reviewers "${reviewers[@]}"
    set +x
fi

# [EOF]
