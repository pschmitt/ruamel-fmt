{
  description = "Flake for ruamel-fmt development and packaging";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      nixpkgs,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python313;
        pyPkgs = python.pkgs;

        ruamelFmt = pyPkgs.buildPythonApplication {
          pname = "ruamel-fmt";
          version = "0.0.2";
          src = ./.;
          pyproject = true;
          nativeBuildInputs = with pyPkgs; [
            setuptools
            setuptools-scm
            wheel
          ];
          propagatedBuildInputs = [
            pyPkgs.ruamel-yaml
          ];
          pythonImportsCheck = [ "ruamel_fmt" ];
        };

        devTools = python.withPackages (
          ps: with ps; [
            black
            ipython
            neovim
            ruff
          ]
        );
      in
      {
        packages = {
          default = ruamelFmt;
          ruamel-fmt = ruamelFmt;
        };

        devShells.default = pkgs.mkShell {
          name = "ruamel-fmt-devshell";
          packages = [
            devTools
            pkgs.pre-commit
            pkgs.uv
            pkgs.git
          ];

          shellHook = ''
            export PYTHONPATH="''${PWD}:''${PYTHONPATH:-}"
            export UV_PROJECT_ENVIRONMENT=".venv"
            echo "Entering ruamel-fmt dev shell (Python ${python.version})."
            echo "Run 'uv sync' to populate .venv and 'ruamel-fmt < file.yaml' to format."
          '';
        };
      }
    );
}
