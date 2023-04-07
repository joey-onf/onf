#!/bin/bash
## --------------------------------------------------------------------
## Intent: Construct a jira ticket query with attributes
## --------------------------------------------------------------------

##-------------------##
##---]  GLOBALS  [---##
##-------------------##
declare -g -a text=()
declare -g -a text_and=()
declare -g -a text_or=()

## --------------------------------------------------------------------
## --------------------------------------------------------------------
function error()
{
    echo "ERROR ${FUNCNAME[1]}: $@"
    exit 1
}

## --------------------------------------------------------------------
## Intent: Query by component name filter
## --------------------------------------------------------------------
## Value: helm-charts
## --------------------------------------------------------------------
function do_components()
{
    declare -n args=$1; shift
    declare -n ans=$1; shift

    if [[ ${#args[@]} -gt 0 ]]; then

	local modifier
	if [[ -v bool_not ]]; then
	    modifier='NOT IN'
	else
	    modifier='IN'
	fi
	ans+=("component ${modifier} (${args[@]})")
       # alt: comp='foo' OR comp='bar'
    fi

    return
}

## --------------------------------------------------------------------
## Intent: Query by compound text filters
## --------------------------------------------------------------------
function do_text()
{
    declare -n ans=$1; shift
    local val

    ## Accumulate
    if [[ ${#text[@]} -gt 0 ]]; then
	if [[ -v bool_and ]]; then
	    text_and+=("${text[@]}")
	else
	    text_or+=("${text[@]}")
	fi
    fi

    ## Append terms: AND
    if [[ ${#text_and[@]} -gt 0 ]]; then
	declare -a term=()
	for val in "${text_and[@]}";
	do
	    term+=("text ~ \"$val\"")
	done
	val=$(join_by ' AND ' "${term[@]}")
	ans+=("($val)")
    fi

    ## Append terms: OR
    if [[ ${#text_or[@]} -gt 0 ]]; then
	declare -a term=()
	for val in "${text_or[@]}";
	do
	    term+=("text ~ \"$val\"")
	done
	val=$(join_by ' OR ' "${term[@]}")
	ans+=("($val)")
    fi

    return
}

## --------------------------------------------------------------------
## Intent: Query by assigned or requestor
## --------------------------------------------------------------------
## Note: Simple for now but support query by a list of suers
## --------------------------------------------------------------------
function do_user()
{
    declare -n ans=$1; shift

    [[ -v argv_nobody ]] && return

    local user='currentUser()'
    if [[ -v argv_user ]]; then
	user="$argv_user"
    fi

    if [[ -v argv_assigned ]]; then
	ans+=("assignee=${user}")
    fi

    if [[ -v argv_reported ]]; then
	ans+=("reporter=${user}")
    fi

    return
}

## --------------------------------------------------------------------
## Intent: Dispaly command usage
## --------------------------------------------------------------------
function usage()
{
    cat <<EOH
Usage: $0

[SERVER]
  --onf         jira.opennetworking.org (default)
  --opencord    jira.opencord.org

  --component   Search by component assigned to a ticket
  --text        Search string(s)
  --unresolved  Search for open tickets

[USER(s)]
  --me          Tickets assigned to or reported by me.
  --user [u]    Tickets assigned to this user.
  --nobody      Raw query, no filtering by user

[BY-USER]
  --assigned    Tickets assided to user
  --reported    Tickets created by user

[BOOL]
  --and            Join terms using 'AND'
  --or             Join terms using 'OR'

[MEMBER]
  --in             (default) Items belong (--component IN)
  --not-in         Negate item set (--component NOT IN)

[Contains]
  --text     [t]   (join modifer: --and, --or)
  --text-and [t]   All of these terms
  --text-or  [t]   Any of these terms

[RANGE]
  --newer [d]   Search for tickets created < [n] days ago.
  --older [d]   Search for tickets created > [n] days ago.

[TODO]

[USAGE]
  $0 --assigned
     o Display all tickets assigned to my login
  $0 --requested --user tux
     o Display all tickets requested by user tux
  $0 --reported --or --text 'bbsim' --text 'release'
     o Search for tickets that contain strings bbsim or release
  $0 --cord --text-and 'release' --text-and 'voltctl'
     o Search jira.opencord for tickets that contain release and voltctl
  $0 --text 'bitergia' --text 'Jira' -and
     o Search jira.opennetworking for tickets containing string bitergia and Jira
EOH

    return
}

## --------------------------------------------------------------------
# classpath=$(join_by ':' "${mypath[@]}")
## --------------------------------------------------------------------
function join_by()
{
    local d=${1-} f=${2-}; if shift 2; then printf %s "$f" "${@/#/$d}"; fi;
}

##----------------##
##---]  MAIN  [---##
##----------------##
declare -a suffix0=()

declare -g -i resolved=0
while [ $# -gt 0 ]; do

    if [ ${#suffix0[@]} -gt 0 ]; then
	   suffix0+=('AND')
    fi

    arg="$1"; shift
    [[ -v debug ]] && echo "** argv=[$arg] [$*]"

    case "$arg" in

	-*help) usage; exit 0 ;;

	##-------------------##
	##---]  BY USER  [---##
	##-------------------##
	--assigned) declare -g -i argv_assigned=1 ;;
	--reported) declare -g -i argv_reported=1 ;;
	--me)       declare -g -i argv_me=1       ;;
	--nobody)   declare -g -i argv_nobody=1   ;;
	--user)
	    arg="$1"; shift
	    declare -g argv_user="$arg"
	    ;;	

	##------------------##
	##---]  SERVER  [---##
	##------------------##
	-*onf) declare server='jira.opennetworking.org'; error "FOUND --onf" ;;
	-*cord) declare server='jira.opencord.org' ;;

	##----------------------------##
	##---]  Component Search  [---##
	##----------------------------##
	# https://support.atlassian.com/jira-software-cloud/docs/advanced-search-reference-jql-fields/
	--component|--comp*)
	    arg="$1"; shift
	    [[ ! -v components ]] && declare -g -a components=()
	    components+=("$arg")
	    ;;

	##-----------------------##
	##---]  Text Search  [---##
	##-----------------------##
	# jsearch.sh --text-and bbsim --text-and release
	-*text-and) text_and+=("$1"); shift ;;
	-*text-or) text_or+=("$1");   shift ;;

	# % js --and --text jenkins --text cord
	# text ~ "Jira Software"      # [WORDs]
	# text ~ "\"Jira Software\""  # [STRING]
	-*text)
	    arg="$1"; shift
	    echo "TEXT: $arg"
	    if [[ -v bool_and ]]; then
		text_and+=("$arg")
	    elif [[ -v bool_or ]]; then
		text_or+=("$arg")
	    else
		text+=("$arg")
	    fi
	    ;;

	# --[un-]resolved toggle
	--all) resolved=99 ;;

	-*resolved)
	    if [ $resolved -eq 0 ]; then
		resolved=1
	    else
		resolved=0
	    fi
	    ;;

	-*newer)
	    arg="$1"; shift
	    suffix0+=("created <= '-${arg}d'") ;;
	-*older)
	    arg="$1"; shift
	    suffix0+=("created >= '-${arg}d'") ;;

	##----------------##
	##---]  BOOL  [---##
	##----------------##
	--[aA][nN][dD]) declare -g -i bool_and=1 ;;
	--[oO][rR])     declare -g -i bool_or=1  ;;

	##------------------##
	##---]  MEMBER  [---##
	##------------------##
	--[iI][nN])     declare -g -i bool_in=1  ;;
	--[nN][oO][tT]) declare -g -i bool_not=1 ;;

	# -----------------------------------------------------------------------
	# https://support.atlassian.com/jira-software-cloud/docs/search-syntax-for-text-fields/
	# -----------------------------------------------------------------------
	# +jira atlassian -- must contain jira, atlassian is optional
	# -japan          -- exclude term
	# [STEM] summary ~ "customize"    -- finds stem 'custom' in the Summary field
	*)
	    declare -p text_and
	    error "Detected unknown argument $arg"
	    ;;
    esac
done

## ----------------------
## Construct query filter
## ----------------------
do_components components suffix0
do_text suffix0
do_user suffix0

declare -p suffix0
[[ "${suffix0[-1]}" != 'AND' ]] && suffix0+=('AND')

## Ticket resolution
case "$resolved" in
    0) suffix0+=('resolution IS EMPTY') ;;
    1) suffix0+=('resolution IS NOT EMPTY') ;;
    99) ;;
esac

## Massage with html codes
suffix=$(join_by '%20' "${suffix0[@]}")

## Which jira server to query (?)
[[ ! -v server ]] && declare -g server='jira.opennetworking.org'

url="https://${server}/issues/?jql="

tmp="${url}${suffix}"
url="${tmp// /%20}"
echo "URL: $url"

browser="${BROWSER:-/snap/bin/firefox}"

"$browser" "${url}"

# [EOF]
