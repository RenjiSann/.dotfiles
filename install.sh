# /usr/bin/bash

# INSTALL PACKAGES

sudo pacman -S --needed - < required_packages.txt


# SYMLINKS

# vim and neovim
#ln -sfv ~/.dotfiles/vim .vimrc 
ln -sfv ~/.dotfiles/nvim ~/.config/

# .bashrc etc...
ln -sfv ~/.dotfiles/.bashrc ~/
ln -sfv ~/.dotfiles/.bash_aliases ~

# i3
ln -sfv ~/.dotfiles/.i3 ~

# git
ln -sfv ~/.dotfiles/.gitconfig ~
ln -sfv ~/.dotfiles/.git-prompt.sh ~

# kitty
rm -rf ~/.config/kitty
ln -sfv ~/.dotfiles/kitty ~/.config
