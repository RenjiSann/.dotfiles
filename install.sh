# /usr/bin/bash

# INSTALL PACKAGES

sudo pacman -S --needed - < required_packages.txt

# Make dmenu_run_history executable and move it to proper location
chmod +x resources/dmenu_run_history
sudo cp resources/dmenu_run_history /usr/bin/


# SYMLINKS

# vim
#ln -sfv ~/.dotfiles/vim .vimrc 
ln -sfv ~/.dotfiles/.vim ~
ln -sfv ~/.dotfiles/.vimrc ~


# .bashrc etc...
ln -sfv ~/.dotfiles/.bashrc ~/
ln -sfv ~/.dotfiles/.bash_aliases ~

# i3
rm -rf ~/.config/i3
ln -sfv ~/.dotfiles/i3 ~/.config/

# git
ln -sfv ~/.dotfiles/.gitconfig ~
ln -sfv ~/.dotfiles/.git-prompt.sh ~

# kitty
rm -rf ~/.config/kitty
ln -sfv ~/.dotfiles/kitty ~/.config
