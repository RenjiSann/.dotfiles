echo "Installing NeoVim config"

declare -r NVIM_LOCAL=$HOME/.local/share/nvim
declare -r NVIM_CFG=$HOME/.config/nvim
declare -r NVCHAD_GIT="$(pwd)/nvchad"

# Install NvChad, and remove the folder ~/.local/share/nvim
# as advised on https://nvchad.com/quickstart/install
if [ -d "$NVIM_LOCAL" ]; then
    echo "Removing old '$NVIM_LOCAL'..."
    rm -rf "$NVIM_LOCAL"
fi
if [ -d "$NVIM_CFG" ]; then
    echo "Removing old '$NVIM_CFG'..."
    rm -rf "$NVIM_CFG"
fi

ln -sfv -T "${NVCHAD_GIT}" "${NVIM_CFG}"

# Create a symlink to the custom config
declare -r SRC="$(pwd)/nvchad_custom"
declare -r DEST="$NVIM_CFG/lua/custom"

ln -sfv -T "$SRC" "$DEST"
