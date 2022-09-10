#! /bin/sh

# Load the utils
. ./utils/dotfile_functions.sh

# Installation directories
declare -r NVIM_INSTALL_DIR="nvim_install"
declare -r VIM_INSTALL_DIR="vim_install"
declare -r I3_INSTALL_DIR="i3_install"
declare -r SHELL_INSTALL_DIR="shell_install"
declare -r KITTY_INSTALL_DIR="kitty_install"

# Install nvim
ask_then_perform "Install NeoVim ?" 'cd ${NVIM_INSTALL_DIR} && ./install.sh && cd ..'

# Install i3 config
ask_then_perform "Install i3 ?" 'cd ${I3_INSTALL_DIR} && ./install.sh && cd ..'

# Install shell config
ask_then_perform "Install shell config ?" 'cd ${SHELL_INSTALL_DIR} && ./install.sh && cd ..'

# Install kitty config
ask_then_perform "Install Kitty ?" 'cd ${KITTY_INSTALL_DIR} && ./install.sh && cd ..'

# Install kitty config
ask_then_perform "Install Vim ?" 'cd ${VIM_INSTALL_DIR} && ./install.sh && cd ..'


#   # INSTALL PACKAGES

#   sudo pacman -S --needed - < required_packages.txt


#   # SYMLINKS

#   echo "==> Symlinking..."

#   # Xprofile
#   ln -sfv ~/.dotfiles/.xprofile ~

#   # vim
#   rm -rf ~/.vim
#   ln -sfv ~/.dotfiles/.vim ~
#   ln -sfv ~/.dotfiles/.vimrc ~

#   # .bashrc etc...
#   ln -sfv ~/.dotfiles/.bashrc ~/
#   ln -sfv ~/.dotfiles/.bash_aliases ~

#   # git
#   ln -sfv ~/.dotfiles/.gitconfig ~
#   ln -sfv ~/.dotfiles/.git-prompt.sh ~

#   # kitty
#   rm -rf ~/.config/kitty
#   ln -sfv ~/.dotfiles/kitty ~/.config

#   # fehbg handling
#   ln -sfv ~/.dotfiles/.fehbg ~

#   # Thunderbird
#   ln -sfv ~/.dotfiles/.thunderbird ~

#   # Wallpaper
#   echo "==> Add the lock wallpaper"

#   sudo cp ~/.dotfiles/resources/lock_wallpaper.png /usr/share/backgrounds/
