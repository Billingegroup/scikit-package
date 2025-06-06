from argparse import ArgumentParser

from scikit_package.cli import add, create
from scikit_package.cli.update import cf

SKPKG_GITHUB_URL = "https://github.com/scikit-package/scikit-package"


def _add_subcommands(subparsers, commands, func, special_args={}):
    """Helper function to add subcommands to a parser."""
    for command, help_text in commands:
        parser_sub = subparsers.add_parser(command, help=help_text)
        if command in special_args:
            special_args[command](parser_sub)
        parser_sub.set_defaults(func=func, subcommand=command)


def _add_news_flags(p):
    """Helper function to add flags for `package add news/no-news`."""
    p.add_argument("-m", "--message", required=True, help="News item.")
    p.add_argument("-a", "--add", action="store_true", help="Added")
    p.add_argument("-c", "--change", action="store_true", help="Changed")
    p.add_argument("-d", "--deprecate", action="store_true", help="Deprecated")
    p.add_argument("-r", "--remove", action="store_true", help="Removed")
    p.add_argument("-f", "--fix", action="store_true", help="Fixed")
    p.add_argument("-s", "--security", action="store_true", help="Security")


def setup_subparsers(parser):
    # "create" subparser
    parser_create = parser.add_parser("create", help="Create a new package")
    subparsers_create = parser_create.add_subparsers(
        dest="subcommand", required=True
    )
    create_commands = [
        ("workspace", "Create a workspace package"),
        ("system", "Create a system package"),
        ("public", "Create a public package"),
        ("conda-forge", "Create a conda-forge recipe meta.yml file"),
        ("manuscript", "Create Overleaf LaTeX template of Billinge group."),
    ]
    _add_subcommands(subparsers_create, create_commands, create.package)
    # "add" subparser
    parser_add = parser.add_parser(
        "add", help="Add a new file like a news item"
    )
    subparsers_add = parser_add.add_subparsers(
        dest="subcommand", required=True
    )
    add_commands = [
        ("news", "Add a news item under the news directory."),
        ("no-news", "Add no news item under the news directory."),
    ]
    _add_subcommands(
        subparsers_add,
        add_commands,
        add.news_item,
        special_args={
            "news": _add_news_flags,
            "no-news": _add_news_flags,
        },
    )
    # "update" subparser
    parser_update = parser.add_parser(
        "update", help="Update existing package."
    )
    subparsers_update = parser_update.add_subparsers(
        dest="subcommand", required=True
    )
    update_commands = [
        (
            "conda-forge",
            "Update conda-forge recipe meta.yml file after release.",
        ),
    ]
    _add_subcommands(subparsers_update, update_commands, cf.update)


def main():
    """Entry point for the scikit-package CLI.

    Examples
    --------
    >>> package create workspace
    >>> package create system
    >>> package create public
    >>> package create manuscript
    >>> package create conda-forge
    >>> package add news -a -m "Add awesome news item."
    >>> package add no-news -m "It was a simple typo."
    >>> package update conda-forge
    >>> package update (Not implemented yet)
    """
    parser = ArgumentParser(
        description="Reduce effort for maintaining and developing packages."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    setup_subparsers(subparsers)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
