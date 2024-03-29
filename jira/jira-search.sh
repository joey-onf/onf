#!/bin/bash
## --------------------------------------------------------------------
## Intent: Construct a jira ticket query with attributes
## --------------------------------------------------------------------

# set -euo pipefail
#source ~/.sandbox/trainlab-common/common.sh '--common-args-begin--'

##-------------------##
##---]  GLOBALS  [---##
##-------------------##
declare -g -a text=()
declare -g -a text_and=()
declare -g -a text_or=()

declare -g -a urls_raw=()
declare -g -a urls_filt=()

declare -g -a labels_incl=()
declare -g -a labels_excl=()

declare -g -a projects=()

path="$(realpath $0 --canonicalize-existing)"
source "${path%\.sh}/utils.sh"
source "$pgmlib/fixversion.sh"
source "$pgmlib/resolved.sh"

## --------------------------------------------------------------------
## --------------------------------------------------------------------
function error()
{
    echo "ERROR ${FUNCNAME[1]}: $@"
    exit 1
}

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
function html_encode()
{
    local -n ref=$1; shift
    local tmp="$ref"

    tmp="${tmp//[[:space:]]/%20}"
    tmp="${tmp//\"/%22}"
    tmp="${tmp//\'/%27}"

    ref="$tmp"
    return
}

## -----------------------------------------------------------------------
## Intent: Insert a conjunction into the stream when prior statements exist
## -----------------------------------------------------------------------
function conjunction()
{
    return
    
    local -n ref=$1; shift
    [[ $# -gt 0 ]] && { local literal="$1"; shift; }

    ## -------------------------------
    ## Conjunction if prior statements
    ## -------------------------------
    if [ ${#ref[@]} -gt 0 ]; then
        if [[ -v literal ]]; then
            ref+=("$literal")
        elif [[ -v bool_and ]]; then
            ref+=('AND')
        else
            ref+=('OR')
        fi
    fi

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

## --------------------------------------------------------------------
## Intent: Query by component name filter
## --------------------------------------------------------------------
## Value: helm-charts
## --------------------------------------------------------------------
function do_components()
{
    declare -n args=$1; shift
    declare -n ans=$1; shift

    # [ -z ${args+word} ] && { args=(); }
    
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
## Intent: Query filter by labels assigned to a ticket:
##   o pods, failing, testing
## --------------------------------------------------------------------
# "project in (UKSCR, COMPRG) AND issuetype = Bug AND labels in (BAT)" and
## --------------------------------------------------------------------
function do_labels()
{
    declare -n incl=$1; shift # was args=
    declare -n excl=$1; shift
    declare -n ans=$1; shift

    ## --------------------------------
    ## Conjunction if stream tokens > 0
    ## --------------------------------
    conjunction ans

    declare -a tokens=()

    ## -----------------------------
    ## -----------------------------
    if [[ ${#incl[@]} -gt 0 ]]; then

        local modifier
        if [[ -v bool_not ]]; then
            modifier='NOT IN'
        else
            modifier='IN'
        fi

        local labels=$(join_by ',' "${incl[@]}")
        local -a tmp=(\
                      '('\
                          'label IS EMPTY' \
                          'OR' \
                          "labels ${modifier} ($labels)" \
                          ')'\
            )
        tokens+=("${tmp[@]}")
    fi

    conjunction tokens 'AND'

    ## -----------------------------
    ## -----------------------------
    if [[ ${#excl[@]} -gt 0 ]]; then
        local labels=$(join_by ',' "${excl[@]}")
        tokens+=('(' "labels NOT IN ($labels)" ')')
    fi

    ans+=("${tokens[@]}")
    return
}

## --------------------------------------------------------------------
## Intent: Modify search query by project type (SEBA, VOL)
## --------------------------------------------------------------------
function do_projects()
{
    declare -n ref=$1; shift

    [[ ${#projects[@]} -eq 0 ]] && { return; }

    local terms="$(join_by ',' "${projects[@]}")"
#    local -a buffer=('(' 'project' 'IN' "($terms)" ')')
#    ref+=("$(join_by '%20' "${buffer[@]}")")
    ref+=("(project IN ($terms))")
    return
}

## --------------------------------------------------------------------
## Intent: Query by compound text filters
## --------------------------------------------------------------------
function do_text()
{
    local -n ref=$1; shift
    local -n ans=$1; shift
    local val

    ## Accumulate
    if [[ ${#ref[@]} -gt 0 ]]; then

        if [[ -v bool_and ]]; then
            text_and+=("${ref[@]}")
        else
            text_or+=("${ref[@]}")
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
## Intent: Combine filter arguments into a search query
## --------------------------------------------------------------------
function gen_filter()
{
    declare -n ans=$1; shift
    declare -n args=$1; shift

    ## -----------------------------------
    ## Begin by joining major search terms
    ## -----------------------------------
    declare -a _tmp=()
    local val
    for val in "${args[@]}";
    do
        _tmp+=("$val" 'AND')
    done
    unset _tmp[-1]

    ## -----------------------
    ## Massage with html codes
    ## -----------------------
    ans="$(join_by '%20' "${_tmp[@]}")"
    return
}

## --------------------------------------------------------------------
## Intent: Combine filter arguments into a search query
## --------------------------------------------------------------------
function gen_url()
{
    declare -n ans=$1; shift
    declare -n args=$1; shift

    ## Which jira server to query (?)
    [[ ! -v server ]] && declare -g server='jira.opennetworking.org'
    tmp_url="https://${server}/issues/?jql="
    tmp="${tmp_url}${args}"
    ans="${tmp// /%20}"
    return
}

## --------------------------------------------------------------------
## Intent: Dispaly command usage
## --------------------------------------------------------------------
function usage()
{
    cat <<EOH
Usage: $0 VOL-xxxx
  --debug       Enable script debug mode
  --dry-run     Simulate

  VOL-{xxxx}    View a jira ticket by ID

[SERVER]
  --onf         jira.opennetworking.org (default)
  --opencord    jira.opencord.org

[WHAT]
  --component   Search by component name assigned to ticket
  --label       Search by label name assigned to ticket.
  --text        Search string(s)

[FIXVERSION] - Voltha-v2.12
  --fixversion-incl
  --fixversion-excl
  --fixversion-is-empty
  --fixversion-not-empty

[RESOLVED] - tokens={Declined, Won't Fix}
  --resolved-start ccyy-mm-dd
  --resolved-end   ccyy-mm-dd
  --resolved-incl {token(s)}
  --resolved-excl {token(s)}
  --resolved-is-empty   Query for open tickets
  --resolved-not-empty

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

[ALIASES]
  --all         Query for all unresolved tickets

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

  $0 --cord --label failing --label pod
     o Search jira.opencord for tests failing due to pod/hardware issuses.

  $0 --proj VOL --fixversion "VOLTHA v2.12" --resolved-is-empty
     o Query for unresolved release tickets
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

# declare -g -i debug=1

while [ $# -gt 0 ]; do

    if [ ${#suffix0[@]} -gt 0 ]; then
        suffix0+=('AND')
    fi

    arg="$1"; shift
    [[ -v debug ]] && echo "** argv=[$arg] [$*]"

    case "$arg" in

        -*help) usage; exit 0 ;;

        ##-----------------##
        ##---]  MODES  [---##
        ##-----------------##
        -*debug)   declare -g -i debug=1 ;;
        --dry-run) declare -g -i dry_run=1 ;;

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

        ##---------------------##
        ##---]  SEARCH-BY  [---##
        ##---------------------##
        --component|--comp*)
            arg="$1"; shift
            [[ ! -v components ]] && declare -g -a components=()
            components+=("$arg")
            ;;

        --label-excl)
            arg="$1"; shift
            labels_excl+=("$arg")
            ;;

        --label|--label-incl)
            arg="$1"; shift
            labels_incl+=("$arg")
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

        --all) set -- '--resolved-is-none' "$@" ;; # alias: --[un-]resolved

        --proj*) projects+=("$1"); shift ;;

        --fixversion-*)
            # function get_jql_fixversion()
            case "$arg" in
                  *excl)
                      [[ ! -v fixversion_excl ]] && { declare -g -a fixversion_excl=(); }
                      val="\"$1\""; shift
                      html_encode val
                      fixversion_excl+=("$val");
                      ;;

                  *incl)
                      [[ ! -v fixversion_incl ]] && { declare -g -a fixversion_incl=(); }
                      val="\"$1\""; shift
                      html_encode val
                      fixversion_incl+=("$val");
                      ;;

                  *not-empty) declare -g -i fixversion_not_empty=1 ;;
                   *is-empty) declare -g -i fixversion_is_empty=1  ;;

                  *) error "Detected invalid --fixversion-* modifier" ;;
            esac
            ;;

        --resolved-*)
            # function get_jql_reasons()
            case "$arg" in

                *start) declare -g resolved_start="$1"; shift ;;
                  *end) declare -g resolved_end="$1";   shift ;;

                *not-empty) declare -g resolved_not_empty="$1" ;;
                    *empty) declare -g resolved_is_empty="$1"  ;;

                  *excl)
                      [[ ! -v resolved_excl ]] && { declare -g -a resolved_excl=(); }
                      val="\"$1\""; shift
                      html_encode val
                      resolved_excl+=("$val");
                      ;;
                  *incl)
                      [[ ! -v resolved_incl ]] && { declare -g -a resolved_incl=(); }
                      val="\"$1\""; shift
                      html_encode val
                      resolved_incl+=("$val");
                      ;;
                 *) ;;
                     *) error "Detected invalid --resolved-* modifier" ;;
            esac
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

        [A-Z][A-Z][A-Z]-[0-9]*)
            case "$arg" in
                CORD-[0-9]*)
                    url="https://jira.opencord.org/browse/${arg}"
                    urls_raw+=('--new-window' "$url")
                    ;;

                INF-[0-9]*)
                    url="https://jira.opennetworking.org/browse/${arg}"
                    urls_raw+=('--new-window' "$url")
                    ;;

                VOL-[0-9]*)
                    url="https://jira.opencord.org/browse/${arg}"
                    urls_raw+=('--new-window' "$url")
                    ;;

                *) error "Detected invalid ticket [$arg]" ;;

            esac
            ;;

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
do_user                           suffix0
do_projects                       suffix0
[[ -v components ]] && { do_components components suffix0; }
do_labels labels_incl labels_excl suffix0
do_text  text                     suffix0
do_resolved                       suffix0
do_fixversion                     suffix0

filter=''
gen_filter filter suffix0

if [[ ! -v urls_raw ]]; then
    url=''
    gen_url url filter
    urls_filt+=("$url")
elif [ ${#urls_raw} -eq 0 ]; then
    url=''
    gen_url url filter
    urls_filt+=("$url")
fi

[[ -v debug ]] && [[ -v url ]] && echo "URL: $url"
# browser="${BROWSER:-/snap/bin/firefox}"
# browser="${BROWSER:-/opt/firefox/current/firefox}"
browser="${BROWSER:-opera}"
echo "$browser ${urls_filt[@]} ${urls_raw[@]}"

if [[ ! -v dry_run ]]; then
    "$browser" "${urls_filt[@]}" "${urls_raw[@]}" >/dev/null 2>/dev/null &
fi

# [SEE ALSO]
#   o https://support.atlassian.com/jira-software-cloud/docs/advanced-search-reference-jql-fields/

# [EOF]
