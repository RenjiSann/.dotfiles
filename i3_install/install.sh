#! /bin/sh

# Load the utils
. ../utils/dotfile_functions.sh

echo "Installing i3 config"

declare -r DOT_CFG="$HOME/.config"
declare -r I3_CFG="$DOT_CFG/i3"

# Remove old symlinks
echo "Removing old config"
if [ -L "$I3_CFG" ]; then
    rm "$I3_CFG"
fi

# Create the new symlink
SRC="$(pwd)/i3"
DEST="$I3_CFG"
ln -sfv -T "$SRC" "$DEST"

if confirm_action "Install i3status config as well ?"; then
    echo "Installing i3status config"

    declare -r I3_STAT_CFG="$DOT_CFG/i3status"
    echo "Removing old config"
    if [ -L "$I3_STAT_CFG" ]; then
        rm "$I3_STAT_CFG"
    fi

    SRC="$(pwd)/i3status"
    DEST="$I3_STAT_CFG"
    ln -sfv -T "$SRC" "$DEST"
fi
