"""TODO."""

import argparse
import sys

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

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

    posts = utils.read_jsonfile(in_path)

    if posts is None:
        print("Loaded content is not valid JSON! Exiting...\n")
        sys.exit(1)

    print(f"Analyzing the language of {len(posts)} posts from '{in_path}...'\n")

    nltk.download("vader_lexicon")

    sia = SentimentIntensityAnalyzer()

    for post in posts:
        score = sia.polarity_scores(post["content"])
        post["sentiment"] = score

    utils._write_list_to_jsonfile(posts, out_path)


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
