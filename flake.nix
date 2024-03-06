{
  description = "TTSystemd - a systemd explorer for your terminal";

  inputs.pyproject-nix.url = "github:nix-community/pyproject.nix";
  inputs.pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";

  nixConfig = {
    bash-prompt = ''\n\[\033[1;34m\][\[\e]0;\u@\h: \w\a\]\u@\h:\w]\\$\[\033[0m\] '';
  };

  outputs = {
    nixpkgs,
    pyproject-nix,
    ...
  }: let
    inherit (nixpkgs) lib;

    project = pyproject-nix.lib.project.loadPyproject {
      projectRoot = ./.;
    };

    pkgs = nixpkgs.legacyPackages.x86_64-linux;

    python = pkgs.python3;
  in {
    devShells.x86_64-linux.default = let
      arg = project.renderers.withPackages {inherit python;};
      pythonEnv = python.withPackages arg;
    in
      pkgs.mkShell {
        packages = [
          pkgs.pdm
          pythonEnv
        ];
      };

    packages.x86_64-linux.default = let
      attrs = project.renderers.buildPythonPackage {inherit python;};
    in
      python.pkgs.buildPythonPackage (attrs
        // {
          env.CUSTOM_ENVVAR = "hello";
        });
  };
}
