"""TODO."""

import argparse
import html
import json
import re
import sys

import pandas as pd

import utils


def main():
    """TODO."""

    user_cfg = get_user_cfg()

    print("Reading input JSON...")
    posts = utils.read_jsonfile(user_cfg["input_path"])

    if posts is None:
        print("Input does not have valid JSON! Exiting...")
        sys.exit(1)

    posts = filter_posts(user_cfg, posts)

    posts = clean_post_text(posts)

    posts = trim_post_keys(user_cfg, posts)

    out_path = user_cfg["output_path"]

    print(f"Writing {len(posts)} posts to '{out_path}'!\n")

    utils._write_list_to_jsonfile(posts, out_path)


def clean_post_text(posts):
    print(f"Cleaning post text fom {len(posts)} posts...")
    for post in posts:
        if "content" in post:
            post["content"] = re.sub(r"<.*?>", "", post["content"])
            post["content"] = html.unescape(post["content"])

    return posts


def filter_posts(user_cfg, posts):
    print(f"Filtering out posts by keyword from {len(posts)} total posts...")

    pattern = "|".join(user_cfg["keywords"])

    posts_df = pd.DataFrame(posts)

    posts_df = posts_df.loc[posts_df["language"] == "en"]

    filtered_posts_str = posts_df[posts_df["content"].str.contains(pattern, case=False)]

    filtered_posts = filtered_posts_str.to_json(orient="records")

    return json.loads(filtered_posts)


def trim_post_keys(user_cfg, posts):
    print(f"Trimming keys from {len(posts)} posts...")

    keys_to_keep = user_cfg["keys"]
    filtered_posts = []

    for post in posts:
        filtered_post_obj = {key: post[key] for key in keys_to_keep if key in post}
        filtered_posts.append(filtered_post_obj)

    return filtered_posts


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

    if user_cfg["input_path"] == user_cfg["output_path"]:
        print(
            "Output path is same as input path. Your original data would be overwritten!\n"
        )
        print("Please give a different output path and rerun! Exiting...\n")
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
