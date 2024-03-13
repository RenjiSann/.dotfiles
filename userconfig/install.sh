#! /bin/sh

# Load the utils
. ../utils/dotfile_functions.sh

# Installation directories
declare -r VIM_INSTALL_DIR="vim_install"
declare -r I3_INSTALL_DIR="i3_install"
declare -r SHELL_INSTALL_DIR="shell_install"
declare -r KITTY_INSTALL_DIR="kitty_install"

# Install i3 config
ask_then_perform \
    "Install i3 ?" \
    "cd ${I3_INSTALL_DIR} && ./install.sh && cd .."

# Install shell config
ask_then_perform \
    "Install shell config ?" \
    "cd ${SHELL_INSTALL_DIR} && ./install.sh && cd .."

# Install kitty config
ask_then_perform \
    "Install Kitty ?" \
    "cd ${KITTY_INSTALL_DIR} && ./install.sh && cd .."

# Install vim config
ask_then_perform \
    "Install Vim ?" \
    "cd ${VIM_INSTALL_DIR} && ./install.sh && cd .."

# Install libinput gestures config
ask_then_create_symlink \
    "Install libinput-gesture config ?" \
    "$(pwd)/libinput-gestures.conf" \
    "${HOME}/.config/libinput-gestures.conf"

ask_then_create_symlink \
    "Install .xprofile ?" \
    "$(pwd)/xprofile" \
    "${HOME}/.xprofile"

ask_then_create_symlink \
    "Install .profile ?" \
    "$(pwd)/profile" \
    "${HOME}/.profile"

ask_then_create_symlink \
    "Install .fehbg ?" \
    "$(pwd)/fehbg" \
    "${HOME}/.fehbg"

ask_then_create_symlink \
    "Install .config/rofi ?" \
    "$(pwd)/rofi" \
    "${HOME}/.config/rofi"

