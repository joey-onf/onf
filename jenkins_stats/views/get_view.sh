#!/bin/bash
# ---------------------------------------------------------------------------
# Intent: Retrieve view detail from jenkins
# ---------------------------------------------------------------------------

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

declare serv='jenkins.opencord.org'
# view='voltha-soak'
declare -a views=()

## ---------------------------------------------------------------------------
## Intent: Display a message then exit with status.
## ---------------------------------------------------------------------------
function error()
{
    echo "ERROR: $*"
    exit 1
}

##------------------##
##---]  Getopt  [---##
##------------------##
while [ $# -gt 0 ]; do
    arg="$1"; shift

    case "$arg" in
	-*host) serv="$1"     ; shift ;;
	-*type) url_type="$1" ; shift ;; # default is xml
	-*view) views+=("$1") ; shift ;;
	*) echo "[SKIP] Detected unknown arg [$arg]" ;;
    esac
done

if [ ${#views[@]} -eq 0 ]; then
    error "At least one view is required"
fi

##----------------##
##---]  MAIN  [---##
##----------------##

## Could infer the type from arg passed -> view.{json,xml}
# url_type="xml"
# url="${serv}/view/${view}/api/xml"
# url="${serv}/view/${view}/api/json"

token="${HOME}/.ssh/${serv}/api/token.curl"
[ ! -f "$token" ] && error "netrc api key does not exist: $token"

declare -a args=()
# args+=('--location')
args+=('--silent')
args+=('-X' 'POST')
args+=('--netrc-file' "$token")

for raw0 in "${views[@]}";
do
    case "$raw0" in
	hardcoded-1) raw0="VOLTHA 2.x verify.xml" ;;
	hardcoded-2) raw0="All Jobs" ;;
	hardcoded-3) raw0="OMEC CI" ;;
	hardcoded-4) raw0="ONOS Apps" ;;
    esac
    raw="${raw0//[[:space:]]/%20}"
    
    case "$raw" in
	*.json) url_type='json' ;;
	     *) url_type='xml' ;;
    esac
    mkdir -p "$url_type"

    view="${raw%.*}"
    tview="${view}.tmp"

    declare -p raw
    declare -p view
    declare -p tview
    
    url="https://${serv}/view/${view}/api/${url_type}"
    # echo "VALID: https://jenkins.opencord.org/view/VOLTHA%202.x%20verify/api/xml"
    echo "VALID: https://jenkins.opencord.org/view/VOLTHA-2.8/api/xml"
    set -x
    curl -o "$tview" "${args[@]}" "$url"
    set +x

    if [ ! -e "$tview" ]; then
	echo "ERROR: Failed to retrieve view: $view"
    elif grep -q Error "$tview"; then
	echo "ERROR: get_view failed:"
	grep Error "$tview"
	exit 1
    fi

    # --pretty 2 (--pretty 1 is --format)
    xmllint --format "$tview" --output "$url_type/$view"
    /bin/rm -f "$tview"
done

# [SEE ALSO]
# Auth needed
# https://www.jenkins.io/doc/book/using/remote-access-api/

# https://pypi.org/project/python-jenkins/
# https://www.jenkins.io/doc/book/system-administration/authenticating-scripted-clients/

# [EOF]
