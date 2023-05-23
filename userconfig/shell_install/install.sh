#! /bin/sh

# Load the utils
. ../utils/dotfile_functions.sh

declare -r "ZSH_FILES=$(pwd)/zsh"

common_install() {
    echo "Common shell features"

    # .bash_aliases
    ln -sfv "$(pwd)/bash_aliases" "$HOME/.bash_aliases"
}

zsh_install() {
    echo "Installing zsh config"

    # .zshrc
    ln -sfv "${ZSH_FILES}/zshrc" "$HOME/.zshrc"

    # .oh-my-zsh
    git clone https://github.com/ohmyzsh/ohmyzsh "${HOME}/.oh-my-zsh"

    # Custom themes
    ln -sfv "${ZSH_FILES}/*.zsh-theme" "$HOME/.oh-my-zsh/custom/themes/"

    # Auto suggestion plugin
    #ln -sfv "${ZSH_FILES}/zsh-autosuggestions" "$HOME/.oh-my-zsh/custom/plugins/zsh-autosuggestions"
    git clone https://github.com/zsh-users/zsh-autosuggestions "${HOME}/.oh-my-zsh/custom/plugins/zsh-autosuggestions"

}

other_shell_install() {
    echo "There is no config for this shell"
}

SHELL_NAME=$(grep $USER /etc/passwd | cut -d: -f7 | xargs basename)
echo "Detected shell: $SHELL_NAME"

if confirm_action "Install ZSH dotfiles ?"; then
    zsh_install
fi

common_install
