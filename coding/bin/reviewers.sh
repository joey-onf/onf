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

declare -a emails=()

early_exit=0
for val in "$@";
do
    case "$val" in

	-*nop) early_exit=1 ;;
	-*early*) early_exit=1 ;;
	
	-*bat)
	    case "$USER" in
		joey) emails+=('daf@opennetworking.org')         ;;
		*) emails+=('joey@opennetworking.org')           ;;
	    esac
	    ;;

	-*abhil*)  emails+=('abhilash.laxmeshwar@radisys.com')   ;;
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
	    ;;

#	-*voltha*)
#	    emails+=('gsilva@furukawalatam.com')
#	    emails+=('holger.hildebrandt@adtran.com')
#	    ;;
	
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
