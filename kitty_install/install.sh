#! /bin/sh

declare -r KITTY_CFG="${HOME}/.config/kitty"

# Remove old link if exists
if [ -L "${KITTY_CFG}" ]; then
    rm "${KITTY_CFG}"
fi

SRC="$(pwd)/kitty"
DEST="${KITTY_CFG}"
ln -sfv -T "$SRC" "$DEST"
