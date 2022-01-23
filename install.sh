# /usr/bin/bash

# INSTALL PACKAGES

sudo pacman -S --needed - < required_packages.txt


# SYMLINKS

echo "==> Symlinking..."

# vim
rm -rf ~/.vim
ln -sfv ~/.dotfiles/.vim ~
ln -sfv ~/.dotfiles/.vimrc ~

# .bashrc etc...
ln -sfv ~/.dotfiles/.bashrc ~/
ln -sfv ~/.dotfiles/.bash_aliases ~

# .zshrc
ln -sfv ~/.dotfiles/.zshrc ~/


# i3
rm -rf ~/.config/i3
ln -sfv ~/.dotfiles/i3 ~/.config/

# git
ln -sfv ~/.dotfiles/.gitconfig ~
ln -sfv ~/.dotfiles/.git-prompt.sh ~

# kitty
rm -rf ~/.config/kitty
ln -sfv ~/.dotfiles/kitty ~/.config

# fehbg handling
ln -sfv ~/.dotfiles/.fehbg ~

# Thunderbird
ln -sfv ~/.dotfiles/.thunderbird ~

# Wallpaper
echo "==> Add the lock wallpaper"

sudo cp ~/.dotfiles/resources/lock_wallpaper.png /usr/share/backgrounds/
