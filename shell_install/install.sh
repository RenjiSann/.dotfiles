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
    ln -sfv "${ZSH_FILES}/oh-my-zsh" "$HOME/.oh-my-zsh"

    # Auto suggestion plugin
    ln -sfv "${ZSH_FILES}/zsh-autosuggestions" "$HOME/.oh-my-zsh/custom/plugins/zsh-autosuggestions"

}

bash_install() {
    echo "Installing bash config"

    # .bashrc
    ln -sfv "$(pwd)/bashrc" "$HOME/.bashrc"
}

other_shell_install() {
    echo "There is no config for this shell"
}

SHELL_NAME=$(grep $USER /etc/passwd | cut -d: -f7 | xargs basename)
echo "Detected shell: $SHELL_NAME"

if confirm_action "Install only for detected shell ?"; then
    case "$SHELL_NAME" in
        zsh ) zsh_install ;;
        bash ) bash_install ;;
        * ) other_shell_install ;;
    esac
else
    zsh_install
    bash_install
fi

common_install
