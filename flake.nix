{
  description = "Python environment from requirements.txt using Nix Flakes";

  nixConfig = {
    extra-substituters = [
      "https://nix-community.cachix.org"
      "https://vrheadcache.cachix.org"
    ];
    extra-trusted-public-keys = [
      "nix-community.cachix.org-1:mB9FSh9qf2dCimDSUo8Zy7bkq5CX+/rkCWyvRCYg3Fs="
      "vrheadcache.cachix.org-1:v0XsYmHf9iA9ZtIsdc+Bjyqtzx6DO5f/fiXq2Lq+blA="
    ];
  };

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
          config = {
            allowUnfree = true;
            # cudaSupport = true;
          };
        };
        python = pkgs.python312;
        pythonEnv = python.withPackages (ps:
          with ps; [
            pip
            asttokens
            certifi
            charset-normalizer
            cmake
            contourpy
            cycler
            decorator
            exceptiongroup
            executing
            filelock
            fonttools
            idna
            imageio
            importlib-resources
            ipython
            jedi
            jinja2
            joblib
            kiwisolver
            lazy-loader
            lit
            lmdb
            markupsafe
            matplotlib
            matplotlib-inline
            mpmath
            networkx
            numpy
            opencv4
            packaging
            parso
            pexpect
            pillow
            prompt-toolkit
            ptyprocess
            pure-eval
            pygments
            pyparsing
            python-dateutil
            requests
            scikit-image
            scikit-learn
            scipy
            six
            stack-data
            sympy
            threadpoolctl
            tifffile

            torch-bin
            torchvision-bin

            tqdm
            traitlets
            typing-extensions
            urllib3
            wcwidth
            zipp
            # triton

            ninja
          ]);
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python312Packages.python-lsp-server
            black
            pythonEnv

            # For CUDA support if you already have it remove these two lines
            cudaPackages.cudatoolkit
            cudaPackages.cudnn

            pkg-config
            # ffmpeg

            gtk2.dev
            libGL.dev
          ];

          shellHook = ''
            export CUDA_PATH=${pkgs.cudatoolkit}
            export LD_LIBRARY_PATH=${pkgs.cudatoolkit}/lib:$LD_LIBRARY_PATH
            export EXTRA_CCFLAGS="-I/usr/include"
            echo "Welcome to the Python development environment!"
            echo "You can start working with your Python packages now."
          '';
        };
        packages.default = pythonEnv;
      }
    );
}
