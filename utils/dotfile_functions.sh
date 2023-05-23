# Terminal Colors
declare -r RESET='\e[0m'
declare -r BOLDGREEN='\e[1;32m'
declare -r BOLDRED='\e[1;31m'
declare -r BOLDYELLOW='\e[1;33m'

# Print a yes/no question and return the answer
confirm_action(){
    # Given argument should be a question
    while true; do
        read -p "$1 (y/N) " yn
        case "$yn" in
            [yY] ) return 0;
                break ;;
            * ) return 1;
        esac
    done
}

# Ask for the autorization to perform an action and execute
ask_then_perform(){
    # $1 is the string to ask confirmation
    # $2 is the command to evaluate
    if confirm_action "$1"; then
        if (eval "$2"); then
            echo -e "${BOLDGREEN}Success${RESET}\n"
        else 
            echo -e "${BOLDRED}Error${RESET}\n"
        fi
    else
        echo -e "${BOLDYELLOW}Passed${RESET}\n"
    fi
}

# Give 2 arguments (target) and (dst) and if dst already exists,
# ask before rewriting the config. return true if updated
create_symlink() {
    if [ $# != 2 ]; then exit 1; fi
    TARGET="$1"
    DST="$2"

    if [ -f "${DST}" ] || [ -d "${DST}" ] || [ -L "${DST}" ]; then
        if confirm_action "Config already exists, remove it ?"; then
            echo "Removing old config..."
            rm -rf "${DST}"
        else
            echo "Aborting..."
            return `false`
        fi
    fi
    ln -sfv -T "${TARGET}" "${DST}"
    return `true`
}

# Ask if a config file should be installed, and warn if overwriting
ask_then_create_symlink() {
    if [ $# != 3 ]; then exit 1; fi
    PROMPT="$1"
    TARGET="$2"
    DST="$3"

    if confirm_action "$1"; then
        create_symlink "${TARGET}" "${DST}"
        RES=`echo $?`
        if [ "${RES}" == 0 ] ; then
            echo -e "${BOLDGREEN}Success${RESET}\n"
        else 
            echo -e "${BOLDRED}Error : ${RES}${RESET}\n"
        fi
    else
        echo -e "${BOLDYELLOW}Passed${RESET}\n"
    fi
}

