#!/bin/bash
## -----------------------------------------------------------------------
## Intent: Perform actions based on available sources
##   o Lint/syntax checking
##   o Cosmetic source cleanup (trailing whitespace, tab-to-space expansion
## -----------------------------------------------------------------------
## Cleanup common problems in source based on language:
##   o Replace tab with space:
##     - exception: makefile
##   o Remove trailing whitespace from EOLN
## -----------------------------------------------------------------------
## sed alternatives:
##   o expand -i -t 4 tab-file.txt > no-tab-file.txt
## -----------------------------------------------------------------------

##-------------------##
##---]  GLOBALS  [---##
##-------------------##
declare -g tab_spaces="        "

## --------------------------------------------------------------------
## Intent: Display an error message then exit with status.
## --------------------------------------------------------------------
function error()
{
    echo "ERROR: $@*"
    exit 1
}

## ----------------------------------------------------
## If no specified default to checking locally modified
## ----------------------------------------------------
function do_git_add_deleted()
{
    readarray -t todos < <(git ls-files --deleted)

    git add "${todo[@]}"
    return
}

## ----------------------------------------------------
## If no specified default to checking locally modified
## ----------------------------------------------------
function do_git_add_others()
{
    readarray -t todos < <(git ls-files --others)

    local todo
    for todo in "${todos[@]}";
    do
	case "$todo" in
	    *~) ;;
	    *)
		echo "** ${FUNCNAME}: $todo"
		git add "$todo"
		;;
	esac
    done
    return
}

## ----------------------------------------------------
## If no specified default to checking locally modified
## ----------------------------------------------------
function do_git_add()
{
    [[ ! -v argv_git_add ]] && return
    [ ! -d '.git' ]         && return

    do_git_add_deleted
    do_git_add_others
    return
}

## ----------------------------------------------
## Intent: Check for unused function declarations
## ----------------------------------------------
function func_check()
{
    local src="$1"; shift

    readarray -t funcs < <(awk -F'[ (]' '/^function/ {print $2}' "$src")
    for func in "${funcs[@]}";
    do
	readarray -t found < <(grep -e "$func" "$src" \
			           | awk -F'#' '{print $1}' \
				   | grep -v grep)


	if [ ${#found[@]} -lt 2 ]; then
	    echo "ERROR: Detected unused function $func in $src"
	fi
    done

    return
}

## --------------------------------------------------------------------
## Intent: Syntax checking by file path
## --------------------------------------------------------------------
function lint_check
{
    local src="$1"    ; shift
    local _type_="$1" ; shift

    # ------------------------------
    # Define cleanup based on source
    # ------------------------------
    declare -a actions=()
    case "$_type_" in
	bash)
	    shellcheck "$src"
	    ;;

	groovy)
	    # groovy "$src" # cannot always use on jjb pipeline source
	    npm-groovy-lint "$src"
	    ;;

	makefile)
	    make --recon "$src"
	    ;;

	*)
	    echo "[SKIP] Unknown file to lint $src"
	    ;;
    esac

    return
}

## --------------------------------------------------------------------
## Intent: Cleanup common source problems
## --------------------------------------------------------------------
function reformat_source()
{
    local src="$1"    ; shift
    local _type_="$1" ; shift

    # Prune trailing whitespace
    sed -i -e "s/[[:blank:]]*$//g" "$src"

    # ------------------------------
    # Define cleanup based on source
    # ------------------------------
    declare -a actions=()
    case "$_type_" in
	bash)
	    actions+=('tab_replace')
	    ;;
	groovy)
	    actions+=('tab_replace')
	    ;;
	makefile)
	    ;;
	*)
	    echo "[SKIP] Unknown file type: $src"
	    ;;
    esac

    # -------------
    # Apply cleanup
    # -------------
    local action
    for action in "${actions[@]}";
    do
	case "$action" in
	    tab_replace)
		sed -i -e "s/\t/${tab_spaces}/g" "$src"
		;;
	    *)
		error "Detected unknown action [$action]"
		;;
	esac
    done
    
    return
}

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
function usage()
{
    cat <<EOH
Usage: $0 [options] file[, file]
Options:
  --all-source                Gather all sandbox files (default locally modified)
  --git-add                   Git add locally modified source

  --help                      Print this message and exit.
  --lint                      Perform source syntax checking.

Repair common syntax and formatting problems in source.
  - Check locally modified source in a git sandbox (default)
  - A list of files can be passed in.
EOH
}

##----------------##
##---]  MAIN  [---##
##----------------##
declare -i lint=0

declare -a fyls=() # todo

while [ $# -gt 0 ]; do
    arg="$1"; shift
    case "$arg" in
	-*help) usage; exit 0                          ;;
	-*git-add) declare -g -i argv_git_add=1        ;;
	-*all-source) declare -g -i all_source=1       ;;
	-*lint) lint=1                                 ;;
	-*) error "Detected unsupported switch [$arg]" ;;
	*)
	    if [ -f "$arg" ]; then
		fyls+=("$arg")
	    else
		error "File does not exist: $arg"
	    fi
	    ;;
		
    esac
done


## ----------------------------------------------------
## Process source by:
##   1) explicitly mentioned as command line arguments
##   2) locally modified files (--git-add)
##   3) check everything (--all-source)
## ----------------------------------------------------
[[ ${#fyls[@]} -eq 0 ]] && declare -g -i only_modified=1
do_git_add

## ----------------------------------------------------
## If no specified default to checking locally modified
## ----------------------------------------------------
if [ ${#fyls[@]} -eq 0 ]; then
    if [ -d '.git' ]; then
	readarray -t fyls < <(git ls-files --modified --others)
    fi
fi

if [ ${#fyls[@]} -eq 0 ]; then
    error "No source files detected"
fi

## -----------------------------------------------------------------------
## Iterate: reformat and lint
## -----------------------------------------------------------------------
for fyl in "${fyls[@]}";
do
    echo "** Checking: $fyl"
    ## Identify source type
    language=''
    case "$fyl" in
	     *.groovy) language='groovy'   ;;
	[mM]ake*|*.mk) language='makefile' ;;
	         *.sh) language='bash'     ;;
	     *.python) language='python'   ;;
	 	    *) language='skip'     ;;
    esac

    reformat_source "$fyl" "$language"
    
    [[ $lint -gt 0 ]] && lint_check "$fyl" "$language"

    case "$language" in
	bash) func_check "$fyl" ;;
    esac
done

# EOF
