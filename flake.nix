{
  description = "...";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      python_packages = pkgs.python311.withPackages (ps: with ps; [
        pyaml
        pycparser
        distro
      ]);
    in {
      devShells.default = pkgs.mkShell {
        packages = with pkgs; [doxygen clang-tools_17 python_packages tectonic];
      };
    });
}
