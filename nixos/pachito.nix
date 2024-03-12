{
  config,
  lib,
  pkgs,
  ...
}: {
  # Enable unstable features.
  nix.settings.experimental-features = ["nix-command" "flakes"];

  # Import my home manager config
  imports = [./renji.nix];

  boot.loader.systemd-boot.enable = true;
  # Do not wait for screen with nvidia GPU.
  boot.kernelParams = ["nomodeset" "video=uvesafb:mode_options=1024x768-16@60,mtrr=0,scroll=ywrap,noedid"];

  services.xserver.videoDrivers = ["nvidia"];

  nixpkgs.config.allowUnfree = true;
  hardware.nvidia = {
    modesetting.enable = false;
    open = true;
    nvidiaSettings = true;
    package = config.boot.kernelPackages.nvidiaPackages.stable;
  };

  # Pick only one of the below networking options.
  networking.interfaces.enp6s0.wakeOnLan.enable = true;

  # Open ports in the firewall.
  # networking.firewall.allowedTCPPorts = [ ... ];
  # networking.firewall.allowedUDPPorts = [ ... ];
  # Or disable the firewall altogether.
  # networking.firewall.enable = false;

  # Set your time zone.
  time.timeZone = "Europe/Paris";

  # Select internationalisation properties.
  i18n.defaultLocale = "en_US.UTF-8";
  console = {
    font = "Lat2-Terminus16";
    # keyMap = "us";
    useXkbConfig = true; # use xkb.options in tty.
  };

  # Configure keymap in X11
  services.xserver.xkb.layout = "us";
  services.xserver.xkb.options = "eurosign:e,caps:escape";

  # Define a user account. Don't forget to set a password with ‘passwd’.
  users.extraUsers.renji = {
    isNormalUser = true;
    createHome = true;
    home = "/home/renji";
    extraGroups = ["wheel" "docker"];
    group = "users";
    openssh.authorizedKeys.keys = [
      "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGwd3vcKQYugab+rDEMnRpkHsqk//LQBsTpgNglAiNe1 renji@opale"
    ];
  };

  # List packages installed in system profile. To search, run:
  environment.systemPackages = with pkgs; [
    # docker
    # rnix-lsp
    alejandra
    gcc
    git
    gnumake
    htop
    nix-index
    tree
    tmux
    vim
    wget
  ];

  # Some programs need SUID wrappers, can be configured further or are
  # started in user sessions.
  # programs.mtr.enable = true;
  # programs.gnupg.agent = {
  #   enable = true;
  #   enableSSHSupport = true;
  # };

  programs.direnv.enable = true;
  programs.vim.defaultEditor = true;

  # List services that you want to enable:

  # Enable the OpenSSH daemon.
  services.openssh = {
    enable = true;
    settings.PasswordAuthentication = true; # Allow, as the server should in theory be kept by the bastion
  };

  # Virtualization
  virtualisation.docker.enable = true;

  # Copy the NixOS configuration file and link it from the resulting system
  # (/run/current-system/configuration.nix). This is useful in case you
  # accidentally delete configuration.nix.
  # system.copySystemConfiguration = true;

  # This option defines the first version of NixOS you have installed on this particular machine,
  # and is used to maintain compatibility with application data (e.g. databases) created on older NixOS versions.
  #
  # Most users should NEVER change this value after the initial install, for any reason,
  # even if you've upgraded your system to a new NixOS release.
  #
  # This value does NOT affect the Nixpkgs version your packages and OS are pulled from,
  # so changing it will NOT upgrade your system.
  #
  # This value being lower than the current NixOS release does NOT mean your system is
  # out of date, out of support, or vulnerable.
  #
  # Do NOT change this value unless you have manually inspected all the changes it would make to your configuration,
  # and migrated your data accordingly.
  #
  # For more information, see `man configuration.nix` or https://nixos.org/manual/nixos/stable/options#opt-system.stateVersion .
  system.stateVersion = "23.11"; # Did you read the comment?
}
