import os
import subprocess
from argparse import ArgumentParser
from pathlib import Path

SKPKG_GITHUB_URL = "https://github.com/scikit-package/scikit-package"
SKPKG_CONFIG_FILE = "~/.skpkgrc"
try:
    config_file = os.environ["SKPKG_CONFIG_FILE"]
except KeyError:
    config_file = SKPKG_CONFIG_FILE
config_file = os.path.expandvars(config_file)
config_file = Path(config_file).expanduser()
exist_config = config_file.exists()


def create(entry_type):
    if entry_type == "workspace":
        run_cookiecutter(f"{SKPKG_GITHUB_URL}-workspace")
    elif entry_type == "system":
        run_cookiecutter(f"{SKPKG_GITHUB_URL}-system")
    elif entry_type == "public":
        run_cookiecutter(SKPKG_GITHUB_URL)
    elif entry_type == "conda-forge":
        run_cookiecutter(f"{SKPKG_GITHUB_URL}-conda-forge")
    elif entry_type == "manuscript":
        run_cookiecutter(f"{SKPKG_GITHUB_URL}-manuscript")


def update():
    # FIXME: Implement the update command.
    # As of now it does the same as the create public command.
    run_cookiecutter(SKPKG_GITHUB_URL)


def run_cookiecutter(repo_url):
    try:
        if exist_config:
            subprocess.run(
                [
                    "cookiecutter",
                    repo_url,
                    "--config-file",
                    config_file,
                ],
                check=True,
            )
        else:
            subprocess.run(
                [
                    "cookiecutter",
                    repo_url,
                ],
                check=True,
            )

    except subprocess.CalledProcessError as e:
        print(f"Failed to run scikit-package for the following reason: {e}")


def setup_subparsers(parser):
    # Create "create" subparser
    parser_create = parser.add_parser("create", help="Create a new package")

    # Add subcommands under "create"
    sub_create = parser_create.add_subparsers(dest="subcommand", required=True)

    # Define all "create" subcommands
    create_subcommands = [
        ("workspace", "Create a workspace package"),
        ("system", "Create a system package"),
        ("public", "Create a public package"),
        ("conda-forge", "Create a conda-forge recipe meta.yml file"),
        ("manuscript", "Create Overleaf LaTeX template of Billinge group."),
    ]

    for subcommand, help_text in create_subcommands:
        parser_sub = sub_create.add_parser(subcommand, help=help_text)
        parser_sub.set_defaults(func=create, subcommand=subcommand)

    # Create "update" subparser
    parser_update = parser.add_parser(
        "update", help="Update an existing package"
    )
    parser_update.set_defaults(func=update)


def main():
    """Entry point for the scikit-package CLI.

    Examples
    --------
    >>> package create workspace
    >>> package create system
    >>> package create public
    >>> package create manuscript
    >>> package create conda-forge
    >>> package update (Not implemented yet)
    """

    parser = ArgumentParser(
        description="Manage package operations with scikit-package."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    setup_subparsers(subparsers)
    args = parser.parse_args()
    args.func(args.subcommand)


if __name__ == "__main__":
    main()
