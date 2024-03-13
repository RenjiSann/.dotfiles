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
        imports = [ ./home-renji.nix ];
        home.stateVersion = "23.11";
    };
}
