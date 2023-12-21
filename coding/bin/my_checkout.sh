#!/bin/bash
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------

make_path="$HOME/projects/sandbox"

sbx_root="$(realpath '.')"
source ~/.sandbox/trainlab-common/common_args.sh

pgm_path="$(realpath --canonicalize-existing "${BASH_SOURCE[0]}")"
pgm_root="${pgm_path%/*}"
# source "${BASH_SOURCE[0]%/*}/get_sbx/sbx-all.sh"
source "$pgm_root/get_sbx/sbx-all.sh"

pgm=$(realpath "$0")
# pgmdir="${pgm%/*}"

declare -a repos=()
repos+=('bbsim')
repos+=('ci-management')
repos+=('helm-charts')
repos+=('pod-configs')
repos+=('voltha-docs')
repos+=('voltha-go')
repos+=('voltha-protos')
repos+=('voltctl')
repos+=('voltha-helm-charts')

here="$(realpath '.')"
storage="${here}/.get"
declare -p storage
review_log="${storage}/review.log"
review_tmp="${review_log}.tmp"

declare -A cs=()

## -----------------------------------------------------------------------
## Intent: Checkout a repository and create a developer branch when needed.
## -----------------------------------------------------------------------
function func_echo()
{
    echo "** ${FUNCNAME[1]}: $@"
    return
}

## -----------------------------------------------------------------------
## Intent: Checkout a repository and create a developer branch when needed.
## -----------------------------------------------------------------------
function func_banner()
{
    cat <<EOB

** -----------------------------------------------------------------------
** ${FUNCNAME[1]}: $@"
** -----------------------------------------------------------------------
EOB

    return
}

## -----------------------------------------------------------------------
## Intent: Checkout a repository and create a developer branch when needed.
## -----------------------------------------------------------------------
function error()
{
    echo -e "** ERROR: $@"
    exit 1
}

## -----------------------------------------------------------------------
## Intent: Given a sandbox path, remove when clean=1 is set.
## -----------------------------------------------------------------------
function clean()
{
    local path="$1"; shift
    declare -g clean

    func_echo "ENTER"
    declare -p clean

    ## --------------------------------------------------------------------
    ## --------------------------------------------------------------------
    if [[ clean -ne 0 ]] || [[ -v __clean_sandbox__ ]]; then
        if [ -d "$path" ]; then
            /bin/rm -fr "$path"
        fi
    fi

    [ -d "$path" ] && error "Sandbox Exists: $path"

    func_echo "LEAVE"
    return
}

## -----------------------------------------------------------------------
## Intent: Launch an editor in the recently checked out sandbox
## -----------------------------------------------------------------------
function review_init
{
    mkdir -p "${review_log%/*}"
    touch "$review_log"
    return
}

## -----------------------------------------------------------------------
## Intent: Launch an editor in the recently checked out sandbox
## -----------------------------------------------------------------------
function checkout_by_make()
{
    local __repo="$1"; shift

    func_banner "REPO: $repo"

    func_echo "make -f \"$make_path/makefile\" \"${__repo}\" TOP=\"$sbx_root\""
    make -f "$make_path/makefile" "${__repo}" TOP="$sbx_root" \
         >/dev/null
    return
}

## -----------------------------------------------------------------------
## Intent:
## -----------------------------------------------------------------------
function create_myenv()
{
    local path="$1"; shift

    echo
    echo "** Create myenv chdir/source"
    echo
    echo "cd $path" > myenv
    echo "## source myenv"
    return
}

## -----------------------------------------------------------------------
## Intent: Launch an editor in the recently checked out sandbox
## -----------------------------------------------------------------------
function edit_mode()
{
    local dir="$1"; shift

    [[ ! -v argv_edit_mode ]] && return

    pushd "$dir" >/dev/null
    emacs .
    popd         >/dev/null

    return
}

## -----------------------------------------------------------------------
## Usage:
##    contains list value
## -----------------------------------------------------------------------
function contains()
{
    declare -n list="$1"; shift
    local value="$1"; shift

    [[ " $list " =~ " $value " ]]
    #    [[ $1 =~ (^|[[:space:]])$2($|[[:space:]]) ]] && true || false
    return
}

## -----------------------------------------------------------------------
## Intent: Protect default sandbox/$repo/ code checkout
## -----------------------------------------------------------------------
## Thought:
##   - Implement as a simple rename
##   - into {repo}-all/wip/${timestamp}
## -----------------------------------------------------------------------
function archive_sandbox()
{
    local action="$1" ; shift
    local sbx="$1"    ; shift

    local sbx_all="${sbx}-all"

    case "$action" in
        -*push)
            [[ ! -d "$sbx" ]] && return

            echo
            func_echo "Archive sandbox for review checkout: $sbx"

            local ts="$(date '+%Y%m%d%H%M%s.%N')"
            local dst="$sbx_all/$ts"
            [[ -d "$dst" ]] && error "Destination exists: $dst"

            func_echo "Archive existing sandbox: $sbx"

            declare -g -a archived_sandboxes
            archvied_sandboxes+=("$dst")
            mv -v "$sbx" "$dst"
            ;;

        -*pop)
            [[ !  archived_sandboxes ]] && return
            declare -p archived_sandboxes

            local path="${archived_sandboxes[0]}"
            echo
            func_echo "Restore archived sandbox: $src"
            mv -v "$path" "$src"
            archived_sandboxes=() # array cleanup needed
            ;;

        *)
            func_echo "Detected unknown argument: $action"
            error 'outa here'
            ;;
    esac

    func_echo "archived_sandboxes = $(declare -p archived_sandboxes)"
    return
}

## -----------------------------------------------------------------------
## Intent: Checkout a repository and create a developer _branch_ when needed.
## -----------------------------------------------------------------------
## create_branch "${__repo__}" '--branch' "${__branch__}"
## create_branch "${__repo__}" '--review' "${__review__}"
## create_branch "${__repo__}" 'master' 'master' for simple checkout
## -----------------------------------------------------------------------
function create_branch()
{
    local _repo_="$1"   ; shift
    local _branch_="$1" ; shift
    local _id_="$1"     ; shift  # destination
    declare -g clean

    func_echo "ENTER"

    ## --------------------------------------------------------------------
    ## --------------------------------------------------------------------
    if [[ clean -ne 0 ]]; then
        [ -d "$_repo_" ] && /bin/rm -fr "$_repo_"
    fi

    ## --------------------------------------------------------------------
    ## --------------------------------------------------------------------
    if [ ! -d "$_repo_" ]; then
        cat <<EOM

** -----------------------------------------------------------------------
**  ! -d ${_repo_}
** checkout_by_make "$_repo_"
** -----------------------------------------------------------------------
EOM
        checkout_by_make "$_repo_"
        func_echo "PWD: $(/bin/pwd)"
        func_echo " LS: $(/bin/ls)"
    fi

    echo
    echo "---------------------------------------------------------------------------"
    declare -p _repo_
    declare -p _branch_
    declare -p _id_
    echo "---------------------------------------------------------------------------"

    case "$_branch_" in

        master) : ;; # fall through

        --branch)
            echo "** --branch $branch"
            pushd "$_repo_" >/dev/null
            git checkout -b "$_id_"
            popd          >/dev/null
            ;;

        --review)
            echo "** --review $review"
            
            pushd "$_repo_" >/dev/null
            # clean "$_id_"
            func_echo "PWD: $(/bin/pwd)"

            git review -d "$_id_"
            popd          >/dev/null
            mv -v "${_repo_}" "${_id_}"
            ;;

        *)
            pushd "$_repo_" >/dev/null
            git checkout -b "$_branch_"
            popd          >/dev/null
            ;;
    esac

    func_echo "LEAVE"

    return
}

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
function do_changeset()
{
    local conf="$1"; shift

    source "$conf"

    [[ ! -v repo      ]] && { echo "repo= is required"; exit 1; }
    [[ ! -v change_id ]] && { echo "repo= is required"; exit 1; }

    repo_all="${repo}-all"

    sbx_id="${repo_all}/${change_id}"
    clean "$sbx_id"

    ## ----------------------
    ## Review branch checkout
    ## ----------------------
    mkdir -p "${repo_all}"
    pushd "${repo_all}" >/dev/null

    [ ! -e 'rebase.sh' ] && ln -fns ../rebase.sh

    [ -d "$repo" ] && rm -f "$repo"
    checkout_by_make "$repo"
    # make -f "$sbx_root/makefile" "$repo" TOP="$sbx_root"

    echo
    pushd "$repo" >/dev/null
    git review -d "$change_id"
    echo
    git branch
    popd          >/dev/null

    ## -----------------------------------
    ## Create convenience links to current
    ## -----------------------------------
    mv "${repo}" "${change_id}"
    ln -fns "$change_id" current
    echo $(realpath 'current')

    echo "$(/bin/date '+%Y%m%d%H%M%S'): ${repo} ($change_id)" >> checkouts
    popd >/dev/null # repo_all

    return
}

## -----------------------------------------------------------------------
## Intent: Checkout sandbox in a temp directory
## -----------------------------------------------------------------------
function create_temp_sandbox()
{
    local repo="$1"; shift
    local -n ref=$1; shift

    local temp_sandbox
    common_tempdir_mkdir temp_sandbox

    declare -p temp_sandbox
    pushd "$temp_sandbox"
    checkout_by_make "$repo"
    # make -f "$sbx_root/makefile" "$repo" TOP="$sbx_root"
    popd

    ref="${temp_sandbox}/${repo}"
    return
}

## -----------------------------------------------------------------------
## Intent: Checkout sandbox in a temp directory
## -----------------------------------------------------------------------
function create_temp_sandbox_v2()
{
    local -n ref=$1; shift
    local repo="$1"; shift

    while [[ $# -gt 0 ]]; do
        local arg="$1"; shift
        case "$arg" in
            --branch) local ctsv2_branch="$1"; shift ;;
            --review) local ctsv2_review="$1"; shift ;;
            *) error "Detected invalid argument $arg" ;;
        esac
    done

    local temp_sandbox
    common_tempdir_mkdir temp_sandbox

    declare -p temp_sandbox
    pushd "$temp_sandbox"

    if [[ -v ctsv2_branch ]]; then
        create_branch "${repo}" '--branch' "${ctsv2_branch}"
    elif [[ -v ctsv2_review ]]; then
        create_branch "${repo}" '--review' "${ctsv2_review}"
    else
        create_branch "${repo}" 'master' 'master'
    fi

    popd

    ref="${temp_sandbox}/${repo}"
    return
}

## -----------------------------------------------------------------------
## Intent: Infer command line switches from past usage
## -----------------------------------------------------------------------
function memory_recall()
{
    local review_id="$1"; shift
    local -n ref=$1; shift

    func_echo "Checking $review_id"
    ## memory load
    local conf="$storage/change_id/${review_id}"
    declare -p conf
    /bin/ls -ld "$conf"
    if [ -e "$conf" ]; then
        source "$conf"
        # --review => change_id

        func_echo "$(declare -p repo)"
        [[ ! -v __repo__ ]] && ref+=('--repo' "$repo")
        # repo="ci-management"
        # change_id="I09385c0544221cc87839b5182200977e0571039a"
        # gerrit_id="33686"
    fi
    return
}

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
function usage()
{
    cat <<EOH
Usage: $0 [options] [targets] ....
Options:
  --review [r]      Checkout gerrit Chageset-Id patch
  --repo   [r]      Repository to checkout
  --clean           Remove an existing sandbox ford a pristine checkout.

  --todo            Display pending tasks

Examples
  % $0 --review Ie2e879dbaba4442c2ec0203049a4e48f950d9322 --repo infra-docs
  % $0 --clean --repo voltha-docs
  % $0 --repo bbsim --jira 'VOL-5152' --branch foobar

[TODO]
  % $0 --repo bbsim --jira 'VOL-5152' --review 'I71c2d49243329c7544046fd5fdcdaf66ad47b5cc'

EOH
    exit 0
}

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
function do_changeset()
{
    cat <<EOH
Usage: $0 [options] [targets] ....
Options:
  --clean           Remove an existing sandbox ford a pristine checkout.
  --branch b        Checkout sandbox branch b (default=master)
  --review r        Checkout a patchset under review.

EOH
    exit 0
}

##----------------##
##---]  MAIN  [---##
##----------------##
declare branch="dev-${USER}"
declare review=''
declare -g clean=0
declare -g mirror=0

if [ $# -eq 1 ]; then
    case "$1" in
        I*) ;;
        [0-9]*) ;;
        --todo)
            source "$pgm_root/get_sbx/todo/loader.sh"
            echo
            error "EARLY EXIT"
            ;;


        *) set -- '--clean' '--repo' "$1" ;;
    esac
fi

# clean=0
# mirror=0
declare -a args=('--nop')
declare -A co_args=()
while [ $# -gt 0 ]; do
    arg="$1"; shift
    declare -p arg
    # readarray -t ans < <(find "${sbx_root}/.get" -name "$arg" -print)

    case "$arg" in
        -*help)
            usage
            exit 0
            ;;

        -*edit) declare -g -i argv_edit_mode=1 ;;
        -*name) __name__="$1"; shift           ;;

        -*branch)
            branch="$1"; shift
            args+=('--branch' "$branch")
            declare -g __branch__="$branch"
            readonly __branch__
            ;;

        --review)
            review="$1"; shift
            declare -g __review__="$review"
            readonly __review__

            declare -a tmp=()
            if memory_recall "$review" tmp; then
                set -- "${tmp[@]}"
            fi
            ;;

        -*clean)
            clean=1
            declare -g -i __clean_sandbox__=1
            ;;

        --jira)
            arg="$1"; shift
            __jira__="$arg"
            ;;

        -*master) branch='master'    ;;

        -*mirror) mirror=1           ;;

        -*repo*)
            arg="$1"; shift
            [[ ${arg:0:1} == '-' ]] && error "--repo requires an argument not a switch"
            declare -g __repo__="$arg"
            readonly __repo__
            ;;

        *)
            # --edit Ia167a9d46ee48fbf27c6cd09d78fcf31f3d4aedf
            error "SHOULD NOT BE HERE:\n     $(declare -p arg)"
            ;;
    esac
done

## -----------------------------------------------------------------------
## Secondary switch detection
## -----------------------------------------------------------------------
# if [[ -v __repo__ ]]; then
# fi

if [[ -v __repo__ ]]; then
    if false; then
        :

    elif [[ -v __jira__ ]]; then
        func_echo "Create-by-jira: $__jira__"

        dst=''
        sbx_all_path dst "$__repo__" "$__jira__"
        clean "$dst"

        declare -a args=()
        [[ -v __branch__ ]] && args+=('--branch' "${__branch__}")
        [[ -v __review__ ]] && args+=('--review' "${__review__}")

        tmp_sbx=''
        create_temp_sandbox_v2 tmp_sbx "$__repo__" "${args[@]}"

        sbx_meta "$tmp_sbx"

        mkdir -p "$dst"
        rsync -r --checksum "$tmp_sbx/." "$dst/."

        create_myenv "$dst"

        # unset review
    elif [[ -v __name__ ]]; then

        sbx_all=''
        sbx_all_mkdir "${__repo__}" sbx_all # 20230818

        # voltha-docs-all/__name__
        dst="$sbx_all/${__name__}"
        clean "$dst"

        path=''
        common_tempdir_mkdir path # create_temp_sandbox "${__repo__}" path
        declare -p path

        pushd "$path"
        func_echo "Create sandbox: ${__name__}"
        
        create_branch "${__repo__}" '--branch' 'dev-joey' "${_name_}"
        popd

        mkdir -p "$dst"
        rsync -rv --checksum "${path}/." "${sbx_all}/." # renamed so copy
cat <<EOM

** -----------------------------------------------------------------------
** Remove path: $path
** -----------------------------------------------------------------------
EOM
bash

        # rm -fr "$path"
        create_myenv "$dst"
        edit_mode "$dst"
    elif [[ -v __review__ ]]; then

        sbx_all=''
        sbx_all_mkdir "${__repo__}" sbx_all # 20230818
#        sbx_all_mkdir "$__repo__" sbx_all

        # voltha-docs-all/I8a847fcaa01ae9bf261b2db6bd34262f08d71009
        dst="$sbx_all/${__review__}"
        # if [[ -d "$dst" ]]; then
        clean "$dst"
        ## [[ -d "$dst" ]] && error "Destination sandbox exists: $dst"

        path=''
        common_tempdir_mkdir path # create_temp_sandbox "${__repo__}" path
        declare -p path

        pushd "$path"
        func_echo "Edit review: ${__review__}"
        create_branch "${__repo__}" '--review' "${__review__}"
        popd

        mkdir -p "$dst"
        rsync -rv --checksum "${path}/." "${sbx_all}/." # renamed so copy

        create_myenv "$dst"
        #   echo#
        #   echo "cd $dst" > myenv
        #   echo "## source myenv

        edit_mode "$dst"

        #   archive_sandbox '--pop' "$src"

    elif [[ -v __branch__ ]]; then
        func_echo "Create-by-branch: $__branch__"
        create_branch "${__repo__}" '--branch' "${__branch__}"

    else
        br="dev-${USER}"
        declare -p br
        func_echo "Create-by-branch: $br"
        create_branch "${__repo__}" '--branch' "$br"
    fi

else
    error "--repository is required"
fi

# [EOF]
