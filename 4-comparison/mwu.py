"""TODO."""

import argparse
import sys

import matplotlib.pyplot as plt
from scipy import stats

import utils


def main():
    user_cfg = get_user_cfg()

    data1_path = user_cfg["data1_input_path"]
    data2_path = user_cfg["data2_input_path"]

    data1 = utils.read_jsonfile(data1_path)
    data2 = utils.read_jsonfile(data2_path)

    if data1 is None or data2 is None:
        print("Loaded content is not valid JSON! Exiting...\n")
        sys.exit(1)

    get_comparative_analysis(data1, data2, user_cfg["graph_path"])


def get_comparative_analysis(data1, data2, graph_path):
    print("Conducting comparative analysis of posts...")

    alpha = 0.05

    data1_sentiments: list = [post["sentiment"]["compound"] for post in data1]
    data2_sentiments: list = [post["sentiment"]["compound"] for post in data2]

    u_statistic, mwu_pval = stats.mannwhitneyu(data1_sentiments, data2_sentiments)

    print(f"The U statistic is: {u_statistic}\n")

    alpha = 0.05  # Typical alpha value of 0.05 for statistical significance
    if mwu_pval < alpha:
        print(f"The difference is statistically significant (p = {mwu_pval}).")
    else:
        print(f"The difference is not statistically significant (p = {mwu_pval}).")

    plt.figure(figsize=(10, 6))

    plt.hist(data1_sentiments, bins=30, alpha=0.7, label="mastodon.social")
    plt.hist(data2_sentiments, bins=30, alpha=0.7, label="techhub.social")

    plt.title(
        "mastodon.social and techhub.social sentiments about ChatGPT in pedagogy"
    )
    plt.xlabel("Value")
    plt.ylabel("Frequency")

    plt.legend()

    plt.savefig(graph_path)


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
