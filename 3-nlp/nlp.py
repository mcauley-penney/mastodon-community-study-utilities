"""TODO."""

import argparse
import sys

import matplotlib.pyplot as plt
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np
from scipy import stats

import utils


def main():
    user_cfg = get_user_cfg()

    in_path = user_cfg["input_path"]
    out_path = user_cfg["output_path"]

    posts = utils.read_jsonfile(in_path)

    if posts is None:
        print("Loaded content is not valid JSON! Exiting...\n")
        sys.exit(1)

    posts = get_posts_sentiments(in_path, posts)

    print(f"Writing {len(posts)} with sentiments to '{out_path}'...")

    utils._write_list_to_jsonfile(posts, out_path)

    get_nlp_output(user_cfg, posts)


def get_nlp_output(user_cfg, posts):
    print("Conducting comparative analysis of posts...")

    out_path = user_cfg["output_path"]

    sentiments: list = [post["sentiment"]["compound"] for post in posts]
    data = np.array(sentiments)

    data_standardized = (data - np.mean(data)) / np.std(data)

    ks_statistic, ks_pval = stats.kstest(data_standardized, "norm")

    print(ks_statistic, ks_pval)

    alpha = 0.05
    if ks_pval < alpha:
        print(f"The data at {out_path} is not normally distributed (p = {ks_pval}).")
    else:
        print(f"The data at {out_path} is normally distributed (p = {ks_pval}).")

    # Generate a Q-Q plot
    stats.probplot(data_standardized, dist="norm", plot=plt)

    plt.title(user_cfg["qq_plot_title"])
    plt.ylabel("Observed Quantiles, from data set")
    plt.xlabel("Theoretical Quantiles, from the standard normal distribution")

    # Display the plot
    plt.savefig(user_cfg["qq_plot_path"])


def get_posts_sentiments(input_path, posts):
    print(f"Analyzing the language of {len(posts)} posts from '{input_path}...'\n")

    nltk.download("vader_lexicon")

    sia = SentimentIntensityAnalyzer()

    for post in posts:
        score = sia.polarity_scores(post["content"])
        post["sentiment"] = score

    return posts


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
