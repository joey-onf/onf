#!/bin/bash
## --------------------------------------------------------------------
## Intent: Construct a jira ticket query with attributes
## --------------------------------------------------------------------

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

[ByUser]
  --assignee    Tickets assided to user
  --reporter    Tickets created by user

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

[USAGE]
  $0 --asignee
  $0 --reported --or --text 'bbsim' --text 'release'
  $0 --text-and 'opencord' --text-and 'voltctl'

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
declare -a text_and=()
declare -a text_or=()

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
	-*assignee)
	    suffix0+=('assignee=currentUser()') ;;
	-*reporter)
	    suffix0+=('reporter=currentUser()') ;;
	
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

if [[ ${#text_and[@]} -gt 0 ]]; then
    for val in "${text_and[@]}";
    do
	declare -p val
	term+=("text ~ \"$val\"")
    done
    val=$(join_by ' AND ' "${term[@]}")
    suffix0+=("(${val})")
fi

declare -p text_or
if [[ ${#text_or[@]} -gt 0 ]]; then
    declare -a term=()
    for val in "${text_or[@]}";
    do
	declare -p val
	term+=("text ~ \"$val\"")
    done
    declare -p term
    val=$(join_by ' OR ' "${term[@]}")
    declare -p val
    suffix0+=("(${val})")
fi


declare -p suffix0
[[ "${suffix0[-1]}" != 'AND' ]] && suffix0+=('AND')

## Ticket resolution
case "$resolved" in
    0) suffix0+=('resolution IS EMPTY') ;;
    1) suffix0+=('resolution IS NOT EMPTY') ;;
    99) ;;
esac

suffix=$(join_by '%20' "${suffix0[@]}")

# https://jira.opennetworking.org/issues/?filter=15405&jql=text%20~%20bitergia%20AND%20resolution%20IS%20EMPTY

# url="https://jira.opennetworking.org/issues/?filter=15405&jql=text%20~%20${val}"
# url+="%20AND%20resolution%20IS%20EMPTY"
# url="https://jira.opennetworking.org/issues/?filter=15405&jql=text%20~%20${val}"
# url+="%20AND%20resolution%20IS%20EMPTY"


# url='https://jira.opennetworking.org/issues/?jql='
[[ ! -v server ]] && declare -g server='jira.opennetworking.org'

url="https://${server}/issues/?jql="

tmp="${url}${suffix}"
url="${tmp// /%20}"
echo "URL: $url"
/snap/bin/firefox "${url}"

# [EOF]
