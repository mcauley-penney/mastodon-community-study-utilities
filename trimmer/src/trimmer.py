"""TODO."""

import sys

from src import utils


def init(user_cfg):
    """TODO."""

    out_path = user_cfg["output_path"]

    if user_cfg["input_path"] == out_path:
        print(
            "Output path is same as input path and your original data would be overwritten!\n"
        )
        print("Please give a different output path and rerun!\n")
        sys.exit(1)

    print("Reading input JSON...")
    posts = utils.read_jsonfile(user_cfg["input_path"])

    if posts is None:
        print("Input does not have valid JSON! Exiting...")
        sys.exit(1)

    print(f"Beginning filtering operation on {len(posts)} post objects...\n")

    keys_to_keep = user_cfg["keys"]
    filtered_posts = []

    for post_obj in posts:
        filtered_post_obj = {
            key: post_obj[key] for key in keys_to_keep if key in post_obj
        }
        filtered_posts.append(filtered_post_obj)

    print(f"Writing output to '{out_path}'!\n")

    utils._write_list_to_jsonfile(filtered_posts, out_path)
