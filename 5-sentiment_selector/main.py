"""TODO."""

import argparse
import random
import sys

import matplotlib.pyplot as plt
from scipy import stats

import utils


def main():
    user_cfg = get_user_cfg()

    posts = utils.read_jsonfile(user_cfg["input_path"])

    if posts is None:
        print("Loaded content is not valid JSON! Exiting...\n")
        sys.exit(1)

    filter_statuses_by_sentiment(posts, user_cfg)


def filter_statuses_by_sentiment(posts, cfg):
    print("Filtering statuses by sentiment")

    filtered_posts: list = [
        post
        for post in posts
        if post["sentiment"]["compound"] <= -0.95
        or post["sentiment"]["compound"] >= 0.95
    ]

    num_posts_to_get = cfg["num_posts_to_get"]

    print(f"Selecting {num_posts_to_get} to collect...")

    i = 0
    selected_posts = []

    while i < num_posts_to_get:
        j = random.randint(0, len(filtered_posts))
        selected_posts.append(filtered_posts[j])

        i += 1

    utils._write_list_to_jsonfile(selected_posts, cfg["output_path"])


def get_user_cfg():
    """
    Get path to and read from configuration file.

    Returns:
        dict: dictionary of configuration values
    """
    cfg_path = __get_cli_args()

    user_cfg = utils.read_jsonfile(cfg_path)

    if user_cfg is None:
        print("User Configuration is not valid JSON! Exiting...")
        sys.exit(1)

    return user_cfg


def __get_cli_args() -> str:
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
