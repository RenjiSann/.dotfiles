#! /bin/sh

# Load the utils
. ./utils/dotfile_functions.sh

# Installation directories
declare -r VIM_INSTALL_DIR="vim_install"
declare -r I3_INSTALL_DIR="i3_install"
declare -r SHELL_INSTALL_DIR="shell_install"
declare -r KITTY_INSTALL_DIR="kitty_install"

# Install i3 config
ask_then_perform "Install i3 ?" 'cd ${I3_INSTALL_DIR} && ./install.sh && cd ..'

# Install shell config
ask_then_perform "Install shell config ?" 'cd ${SHELL_INSTALL_DIR} && ./install.sh && cd ..'

# Install kitty config
ask_then_perform "Install Kitty ?" 'cd ${KITTY_INSTALL_DIR} && ./install.sh && cd ..'

# Install vim config
ask_then_perform "Install Vim ?" 'cd ${VIM_INSTALL_DIR} && ./install.sh && cd ..'

ask_then_perform "Install libinput-gesture config ?" 'ln -sfv -T "$(pwd)/libinput-gestures.conf" ~/.config/libinput-gestures.conf'

echo "===> Installing .xprofile"
create_symlink "$(pwd)/xprofile" "${HOME}/.xprofile"

echo "===> Installing wallpaper"
create_symlink "$(pwd)/fehbg" "${HOME}/.fehbg"

#   # Wallpaper
#   echo "==> Add the lock wallpaper"

#   sudo cp ~/.dotfiles/resources/lock_wallpaper.png /usr/share/backgrounds/
