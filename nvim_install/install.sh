NVIM_LOCAL=$HOME/.local/share/nvim
NVIM_CFG=$HOME/.config/nvim


# Install NvChad, and remove the folder ~/.local/share/nvim
# as advised on https://nvchad.com/quickstart/install
echo "Removing old '$NVIM_LOCAL'..."
rm -rf $NVIM_LOCAL
echo "Removing old '$NVIM_CFG'..."
rm -rf $NVIM_CFG

git clone https://github.com/NvChad/NvChad $NVIM_CFG --depth 1

# Create a symlink to the custom config
NVCHAD_CUST=nvchad_custom
SRC=$(pwd)/$NVCHAD_CUST
DEST=$NVIM_CFG/lua/custom

echo "Symlinking '$SRC' to '$DEST'"

ln -sf -T $SRC $DEST
