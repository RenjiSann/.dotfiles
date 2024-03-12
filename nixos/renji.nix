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

    home.stateVersion = "23.11";
  };
}
