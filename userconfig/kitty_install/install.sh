#! /bin/sh

# Load the utils
. ../utils/dotfile_functions.sh


declare -r KITTY_CFG="${HOME}/.config/kitty"
echo "Installing kitty config"

create_symlink "$(pwd)/kitty" "${KITTY_CFG}"
