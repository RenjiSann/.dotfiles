{
    config,
        lib,
        pkgs,
        ...
}: {

    home.packages = with pkgs; [
        bat
            eza
            lazygit
            rustup
    ];

    home.file.".gdbinit".text = ''
        set tui
        set auto-load safe-path /nix/store
        '';

    programs.git = {
        enable = true;
        userName = "Dorian Péron";
        userEmail = "dorianperon.i@gmail.com";
    };

    programs.zsh = {
        enable = true;
        enableCompletion = false; # enabled in oh-my-zsh
	enableAutosuggestions = true;
            initExtra = ''
            test -f ~/.dir_colors && eval $(dircolors ~/.dir_colors)
		if [ -e /home/renji/.nix-profile/etc/profile.d/nix.sh ]; then . /home/renji/.nix-profile/etc/profile.d/nix.sh; fi # added by Nix installer

# Alias ssh if using xterm kitty, so the SSH session is not broken,
setup_kitty_aliases() {
    alias kssh="kitty +kitten ssh"
    alias icat="kitty +kitten icat"
}
[ "$TERM" = "xterm-kitty" ] && setup_kitty_aliases
            '';
        shellAliases = {
            lzg = "lazygit";
            cat = "bat";
            ls = "eza";
        };
        oh-my-zsh = {
            enable = true;
            plugins = [
                "git"
            ];
            theme = "robbyrussell";
        };
    };

    programs.vim = {
        enable = true;
        plugins = with pkgs.vimPlugins; [
            vim-airline
                onedark-vim
        ];
        extraConfig = ''
            colorscheme onedark
            set termguicolors
            set number
            syntax enable
            set ttymouse=xterm2
            set mouse=a

            " Display spaces at EOL in red
            highlight ExtraWhitespace ctermbg=red guibg=red
            match ExtraWhitespace /\s\+$/

            " Indentation
            set expandtab           " TAB inserts a tabulation instead of spaces
            set autoindent          " Auto indent new lines depending on the one above
            set tabstop=4           " Make TAB length equal to 4 spaces
            set softtabstop=4       " Set the number of tabs to clear when hitting backspace
            set shiftwidth=4        " Set the indent shift width
            '';
    };

    programs.tmux = {
        enable = true;
        extraConfig = ''
            set -g mouse on
            set -g status-right '#[fg=black,bg=color15] #{cpu_percentage}  %H:%M '
            run-shell ${pkgs.tmuxPlugins.cpu}/share/tmux-plugins/cpu/cpu.tmux
            '';
    };
}
