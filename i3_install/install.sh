#! /bin/sh

# Load the utils
. ../utils/dotfile_functions.sh

declare -r DOT_CFG="$HOME/.config"
declare -r I3_CFG="$DOT_CFG/i3"
echo "Installing i3 config"

create_symlink "$(pwd)/i3" "${I3_CFG}"

if confirm_action "Install i3status config as well ?"; then
    echo "Installing i3status config"
    declare -r I3_STATUS_CFG="$DOT_CFG/i3status"
    create_symlink "$(pwd)/i3status" "${I3_STATUS_CFG}"
fi

echo "Installing dunst config"
declare -r DUNST_CFG="$DOT_CFG/dunst"
create_symlink "$(pwd)/dunst" "${DUNST_CFG}"
