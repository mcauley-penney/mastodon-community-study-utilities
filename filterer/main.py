"""TODO."""

import argparse
import json
import sys

import pandas as pd

import utils


def main():
    user_cfg = get_user_cfg()

    if user_cfg is None:
        print("User configuration is None! Exiting...")
        sys.exit(1)

    in_path = user_cfg["input_path"]
    out_path = user_cfg["output_path"]

    if in_path == out_path:
        print(
            "Output path is same as input path and your original data would be overwritten!\n"
        )
        print("Please give a different output path and rerun!\n")
        sys.exit(1)

    print(f"Reading posts from '{in_path}'\n")

    pattern = "|".join(user_cfg["keywords"])

    df = pd.read_json(in_path)

    df = df.loc[df["language"] == "en"]

    filtered_posts_str = df[df["content"].str.contains(pattern, case=False)]

    filtered_posts = filtered_posts_str.to_json(orient="records")

    parsed_filtered_posts = json.loads(filtered_posts)

    print(f"Writing {len(parsed_filtered_posts)} posts to '{out_path}'\n")

    with open(out_path, "w") as f:
        json.dump(parsed_filtered_posts, f, indent=2)


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
