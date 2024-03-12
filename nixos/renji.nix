{
  config,
  lib,
  pkgs,
  ...
}: {
  # My home-manager config

  # Use home-manager
  imports = [<home-manager/nixos>];

  home-manager.users.renji = {
    home.packages = with pkgs; [
      bat
      eza
      lazygit
      rustup
    ];
    programs.bash.enable = true;

    programs.git = {
      enable = true;
      userName = "Dorian Péron";
      userEmail = "dorianperon.i@gmail.com";
    };

    programs.zsh = {
      enable = true;
      enableCompletion = false; # enabled in oh-my-zsh
      initExtra = ''
        test -f ~/.dir_colors && eval $(dircolors ~/.dir_colors)
      '';
      shellAliases = {
        lzg = "lazygit";
        cat = "bat";
        ls = "eza";
      };
      plugins = [
        {
          # will source zsh-autosuggestions.plugin.zsh
          name = "zsh-autosuggestions";
          src = pkgs.fetchFromGitHub {
            owner = "zsh-users";
            repo = "zsh-autosuggestions";
            rev = "v0.7.0";
            sha256 = "0z6i9wjjklb4lvr7zjhbphibsyx51psv50gm07mbb0kj9058j6kc";
          };
        }
      ];
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

    home.stateVersion = "23.11";
  };
}
