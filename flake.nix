{
  description = "cutler: declarative ffmpeg cli builder";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
  inputs.pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";
  inputs.treefmt-nix.url = "github:numtide/treefmt-nix";
  inputs.treefmt-nix.inputs.nixpkgs.follows = "nixpkgs";

  outputs =
    {
      nixpkgs,
      pyproject-nix,
      treefmt-nix,
      ...
    }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;

      project = pyproject-nix.lib.project.loadPyproject {
        projectRoot = ./.;
      };

      pythonFor =
        pkgs:
        pkgs.python3.override {
          packageOverrides = pyfinal: pyprev: {
            py-nickel = pyfinal.buildPythonPackage rec {
              pname = "py-nickel";
              version = "1.17.0";
              pyproject = true;

              src = pkgs.fetchFromGitHub {
                owner = "nickel-lang";
                repo = "nickel";
                rev = version;
                hash = "sha256-D+OI00Ouwm0v65igIYSCGPXKCl6/SZsOyz1wFM1VAF4=";
              };

              cargoDeps = pkgs.rustPlatform.fetchCargoVendor {
                inherit src;
                name = "${pname}-${version}";
                hash = "sha256-hIeTHajL+h6xhuje8TmfgkkM9R+tGwYFzlnSwaN3nK8=";
              };

              nativeBuildInputs = [
                pkgs.rustPlatform.cargoSetupHook
                pkgs.rustPlatform.maturinBuildHook
                pkgs.cargo
                pkgs.rustc
              ];

              maturinBuildFlags = [
                "-m"
                "py-nickel/Cargo.toml"
              ];

              pythonImportsCheck = [ "nickel" ];
            };
          };
        };

      treefmtFor =
        pkgs:
        treefmt-nix.lib.evalModule pkgs {
          projectRootFile = "flake.nix";
          programs.nixfmt.enable = true;
          settings.formatter.nickel = {
            command = lib.getExe (
              pkgs.writeShellApplication {
                name = "nickel-fmt";
                runtimeInputs = [ pkgs.nickel ];
                text = ''
                  for f in "$@"; do
                    nickel format "$f"
                  done
                '';
              }
            );
            includes = [ "*.ncl" ];
          };
        };
    in
    {
      devShells = forAllSystems (system: {
        default =
          let
            pkgs = nixpkgs.legacyPackages.${system};
            python = pythonFor pkgs;
            exampleDeps = [
              pkgs.ffmpeg
              pkgs.yt-dlp
              pkgs.curl
            ];
            pythonEnv = python.withPackages (
              ps:
              (project.renderers.withPackages { inherit python; } ps)
              ++ [
                ps.pip
                ps.hatchling
                ps.editables
              ]
            );
          in
          pkgs.mkShell {
            packages = [ pythonEnv ] ++ exampleDeps;

            shellHook = ''
              venv=".venv"
              if [ ! -e "$venv/bin/cutler" ]; then
                ${pythonEnv.interpreter} -m venv --system-site-packages "$venv"
                "$venv/bin/pip" install --no-build-isolation --no-deps --editable . >/dev/null
              fi
              source "$venv/bin/activate"
            '';
          };
      });

      packages = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pythonFor pkgs;
        in
        {
          default = python.pkgs.buildPythonPackage (project.renderers.buildPythonPackage { inherit python; });
        }
      );

      formatter = forAllSystems (
        system: (treefmtFor nixpkgs.legacyPackages.${system}).config.build.wrapper
      );
    };
}
