# Terminal Colors
declare -r RESET='\e[0m'
declare -r BOLDGREEN='\e[1;32m'
declare -r BOLDRED='\e[1;31m'
declare -r BOLDYELLOW='\e[1;33m'

# Print a yes/no question and return the answer
confirm_action() {
    # Given argument should be a question
    while true; do
        read -p "$1 (y/n) " yn
        case "$yn" in
            [yY] ) return 0;
                break ;;
            [nN] ) return 1;
                break ;;
            * ) echo "Invalid response"
        esac
    done
}

# Ask for the autorization to perform an action and execute
ask_then_perform(){
    # $1 is the string to ask confirmation
    # $2 is the command to evaluate
    if confirm_action "$1"; then
        if eval "$2"; then
            echo -e "${BOLDGREEN}Success${RESET}\n"
        else 
            echo -e "${BOLDRED}Error${RESET}\n"
        fi
    else
        echo -e "${BOLDYELLOW}Passed${RESET}\n"
    fi
}