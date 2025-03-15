let
  # We pin to a specific nixpkgs commit for reproducibility.
  # Last updated: 2024-04-29. Check for new commits at https://status.nixos.org.
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/6607cf789e541e7873d40d3a8f7815ea92204f32.tar.gz") {};
  unstable-pkg = import (fetchTarball "https://github/NixOS/nixpkgs/archive/6607cf789e541e7873d40d3a8f7815ea92204f32.tar.gz") {};
in
  pkgs.mkShell {
    packages = [
      (pkgs.python3.withPackages (python-pkgs:
        with python-pkgs; [
          # select Python packages here
          notebook
          langchain
          pkgs.python312Packages.tree-sitter
          pkgs.python312Packages.gitpython
          pkgs.python312Packages.langchain-openai
          pkgs.python312Packages.langchain-text-splitters
          pkgs.python312Packages.langchain-community
          pandas
          requests
        ]))
    ];
  }
