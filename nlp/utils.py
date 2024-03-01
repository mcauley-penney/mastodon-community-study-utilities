"""
Common utilites for the repository extractor.

Includes:
    - dictionary handling
    - file io

json docs:
    https://docs.python.org/3/library/json.html
"""

from datetime import datetime
import json
from json.decoder import JSONDecodeError
import os
import sys


def __datetime_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()

    raise TypeError("Type not serializable")


def write_merged_list_to_jsonfile(out_list, out_path: str) -> None:
    """
    Recursively merge dictionaries and write them to an output JSON file.

    Get the desired output path, open and read any JSON data that may
    already be there, and recursively merge in param data from the
    most recent round of API calls.

    Args:
        out_dict (dict): dict of data from round of API calls
            to merge and write.
        out_path (str): path to output file.
    """
    # attempt to read JSON out of output file. Will return
    # empty dict if no valid json is found
    base_list = read_jsonfile(out_path)

    if base_list is None:
        base_list = []

    # recursively merge all dicts and nested dicts in both dictionaries
    base_list.extend(out_list)

    # write JSON content back to file
    _write_list_to_jsonfile(base_list, out_path)


def read_jsonfile(in_path: str):
    """
    Read the contents of the provided JSON file into a dictionary.

    Args:
        in_path (str): path to JSON file to read from.

    Returns:
        dict: dictionary constructed from JSON contents.
    """
    try:
        with open(in_path, "r", encoding="UTF-8") as file_obj:
            json_text = file_obj.read()

    except FileNotFoundError:
        json_text = ""

    try:
        json_content = json.loads(json_text)

    except JSONDecodeError:
        json_content = None

    return json_content


def _write_list_to_jsonfile(out_list, out_path: str) -> None:
    """
    Ensure output file exists and write Python dictionary to it as JSON.

    Args:
        out_dict (dict): dictionary to write as JSON.
        out_path (str): path to write output to.

    Raises:
        FileNotFoundError: no file found at given path.
    """
    mk_json_outpath(out_path)

    try:
        with open(out_path, "w", encoding="UTF-8") as json_outfile:
            json.dump(
                out_list,
                json_outfile,
                ensure_ascii=False,
                indent=2,
                default=__datetime_serializer,
            )

    except FileNotFoundError:
        print(f"\nFile at {out_path} not found!")
        sys.exit(1)


def mk_json_outpath(out_path: str):
    """
    Create path to JSON file to write output data to.

    We cannot know if the user will always prepare output paths
    for us, so we must protect our operations by ensuring path
    existence

    Args:
        out_dir (str): dir to init output file in.

    Raises:
        FileExistsError: if the file that we are attempting to
        create already exists, simply move on. The extractor
        knows how to update already existing JSON outputs.

    Returns:
        str: path to output file
    """
    # ensures that path exists, no exception handling required
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Using open() instead of mknode() allows this program to be portable;
    # mknode appears to be *nix specific. We can use "x" mode to ensure that
    # the open call is used exclusively for creating the file. If the file
    # exists, though, "x" mode raises a FileExistsError, which we can
    # ignore.
    try:
        with open(out_path, "x", encoding="UTF-8") as fptr:
            fptr.close()

    except FileExistsError:
        pass
