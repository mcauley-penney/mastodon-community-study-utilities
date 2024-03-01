"""TODO."""

import argparse

from src import trimmer, utils


def main():
    """TODO."""

    user_cfg = get_user_cfg()

    trimmer.init(user_cfg)


def get_user_cfg():
    """
    Get path to and read from configuration file.

    Returns:
        dict: dictionary of configuration values
    """
    cfg_path = get_cli_args()

    return utils.read_jsonfile(cfg_path)


def get_cli_args() -> str:
    """
    Get initializing arguments from CLI.

    Returns:
        str: path to file with arguments to program
    """
    # establish positional argument capability
    arg_parser = argparse.ArgumentParser(
        description="Mine the Mastodon API",
    )

    # add repo input CLI arg
    arg_parser.add_argument(
        "input_json",
        help="Path to JSON file with initializing configuration",
    )

    return arg_parser.parse_args().input_json


if __name__ == "__main__":
    main()
