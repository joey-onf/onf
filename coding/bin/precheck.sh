#!/bin/bash
## -----------------------------------------------------------------------
## Intent: Perform actions based on available sources
##   o Lint/syntax checking
##   o Cosmetic source cleanup (trailing whitespace, tab-to-space expansion)
##   o Verify copyright notice has been updated.
## -----------------------------------------------------------------------
## Cleanup common problems in source based on language:
##   o Replace tab with space:
##     - exception: makefile
##   o Remove trailing whitespace from EOLN
## -----------------------------------------------------------------------
## sed alternatives:
##   o expand -i -t 4 tab-file.txt > no-tab-file.txt
## -----------------------------------------------------------------------

umask 022

##-------------------##
##---]  GLOBALS  [---##
##-------------------##
declare -g tab_spaces="        "

## --------------------------------------------------------------------
## Intent: Display an error message then exit with status.
## --------------------------------------------------------------------
function error()
{
    echo "ERROR: $@"
    exit 1
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
## Intent: Create helper functions for emacs
## -----------------------------------------------------------------------
function configure_emacs()
{
    local emacs_dir="$HOME/.emacs.d/local"
    local conf="${emacs_dir}/precommit.el"
    declare -p conf
    [[ -e "$conf" ]] && return

    mkdir -p "$emacs_dir"

    cat <<EOC > "$conf"
;; -----------------------------------------------------------------------
;; Intent: Emacs batch functions to run prior to commit
;; -----------------------------------------------------------------------

(defun precommit-whitespace ()
  (interactive)
  (mark-whole-buffer)
   (untabify (point-min) (point-max))
   (indent-region (point-min) (point-max))
   (delete-trailing-whitespace (point-min) (point-max))
)

(global-set-key (kbd "<f12>") 'precommit-whitespace)
EOC
    return
}

## --------------------------------------------------------------------
## Intent: Display an error message then exit with status.
## --------------------------------------------------------------------
push_error_dir='precheck.tmp'
function push_err()
{
    local src="$1"; shift

    readarray -d'/' -t _fields <<<"$src"
    local name="$(join_by '-' "${_fields[@]}")"
    local log="$push_error_dir/$name"

    [[ ! -d "$push_error_dir" ]] && mkdir -p "$push_error_dir"
    touch "$log"
    echo "$*" >> "$log"
    return
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
## Intent: Verify copyright notice updated
## --------------------------------------------------------------------
function do_copyright
{
    local src="$1" ; shift
    if [[ ! -v this_year ]]; then
        this_year="$(date '+%Y')"
    fi

    # https://phoenixnap.com/kb/grep-regex

    # Copyright 2017-2023 Open Networking Foundation (ONF) and the ONF Contributors
    readarray -t lines < <(grep -Ei 'copyright \b([[:digit:]]{4})' "$src")
    # declare -p lines

    if ! [[ "${lines[@]}" = *"${this_year}"* ]]; then
        push_err "$src" "Source is not copyright [${this_year}]"
        # error "$src is not copyright [${this_year}]"
    fi

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

        golang)
            echo "NYI -- fix this: gofmt -w -s $src"
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
    local tmp="${src}.tmp"

    # Prune trailing whitespace
    sed -i -e "s/[[:blank:]]*$//g" "$src" # de-blank

    # ------------------------------
    # Define cleanup based on source
    # ------------------------------
    declare -a actions=()
    case "$_type_" in
        bash)
            actions+=('tab_replace')
            ;;
        golang)
            actions+=('gofmt')
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
            gofmt)
                gofmt -s -w "$src"
                ;;

            tab_replace_)
                declare -a eargs=()
                # eargs+=('-l' "~/.emacs")
                emacs -batch "${eargs[@]}" \
                      --eval="(require 'foo)" \
                      --eval="(require 'bar)" \
                      --eval="(some-function $*)"
                ;;

            tab_replace_orig)                
                expand -i -t 8 "$src" > "$tmp"
                mv -f "$tmp" "$src"
                # sed -i -e "s/\t/${tab_spaces}/g" "$src"
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
function init()
{
    configure_emacs
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
  --copyright                 Verify copyright dates
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
        --copyright) declare -g -i argv_copyright=1    ;;

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

init
error "OUTA HERE"


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
        *.go) language='golang'   ;;
        *.groovy) language='groovy'   ;;
        [mM]ake*|*.mk) language='makefile' ;;
        *.sh) language='bash'     ;;
        *.python) language='python'   ;;
        *) language='skip'     ;;
    esac

    reformat_source "$fyl" "$language"

    [[ $lint -gt 0 ]] && lint_check "$fyl" "$language"
    [[ -v argv_copyright ]] && do_copyright "$fyl"

    case "$language" in
        bash) func_check "$fyl" ;;
    esac
done

push_error_dir='precheck.tmp'
pushd "$push_error_dir" >/dev/null
readarray -t fyls < <(find '.' -type f -print | sort -i)
for fyl in "${fyls[@]}";
do
    echo
    echo "FYL: $fyl"
    cat "$fyl"
done
popd                    >/dev/null

/bin/rm -fr "$push_error_dir"

# EOF
