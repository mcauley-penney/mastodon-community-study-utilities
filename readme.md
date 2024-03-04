# Mastodon Community Study Utilities

## What is it?

This repository holds utilities for mining, cleaning, and filtering data from Mastodon's API.

These tools are useful for a workflow where you want to perform some or all of the following steps:

1. Get statuses from Mastodon containing a specific hashtag in reverse chronological order
1. finding a subset of statuses containing keywords
1. producing rudimentary sentiment analysis on statuses

## What's inside?

I intended for the modules to be used in the order they are given in the table below, and used them in this order for my own project.

`🚩 Attention:` Try not to overwrite the data you created at the previous stage with the data from the current stage. You may need it later.

| Module | Description | Input Configuration |
|---|---|---|
| `miner` | searches the Mastodon API for statuses related to a hashtag, then gathers them in reverse chronological order | - `email`: the email you used to sign up for the server you will mine. <br>- `password`: password for the account you have with the server.<br>- `tag`: the hashtag you want to mine for. <br>- `client_credentials_file`: See the [docs](https://mastodonpy.readthedocs.io/en/stable/04_auth.html) for more info. This is just a path in your file system. You won't really need to touch this file.<br>- `user_credentials_file`: Distinct from the client credentials file, but same concept. You probably won't need to touch it. Just give a path.<br>- `output_path`: path where you want the statuses you mine written. Should be a JSON file. The miner is capable of appending to a list of JSON objects in this file as well as starting a mining operation at the last status collected, so you may start mining, stop, then continue where you left off in time. |
| `cleaner` | iterates over a list of JSON objects and removes <br>1) posts that don't contain specific keywords and which aren't in English<br>2) keys specified in the input configuration, and <br>3) HTML tags and entities from the `content` key's string value. <br>This action is destructive, it will discard data you tell it to. Do not overwrite your input file with the output, keep your original data. | - `input_path`: path to a JSON file containing statuses you want to trim down.<br>- `output_path`: path where you want the statuses you mine written. Should be a JSON file.<br>- `keys`: keys in the status JSON objects you want to remove from each JSON object. These should be keys you won't use.<br>- `keywords`: a list of strings, where each string is a keyword that you'd like to filter statuses on. The filtering operation is logical OR; for example, if you want to find statuses that use either of the words "education" or "pedagogy", give both of those terms to this list. |
| `nlp` | produces sentiment analysis for each post's content and inserts it into the post object. | - `input_path`: path to a JSON file containing statuses you want to have sentiment analysis produced for.<br>- `output_path`: path where you want the statuses you mine written. Should be a JSON file. |
| `comparison` | Performs the Mann-Whitney U Test on two data sets | - `data1_input_path`: path to a JSON file containing the first set of statuses you want to compare.<br>- `data2_input_path`: path to a JSON file containing the second set of statuses you want to compare.<br>- `graph_path`: path to a png file displaying an overlaid histogram of the two data sets. |
| `sentiment_selector` | Finds all statuses in a data set that have a 95% to 100% positive or negative composite sentiment, then randomly selects a number of them | - `input_path`: path to a JSON file containing the first set of statuses you want to compare.<br>- `output_path`: path to a JSON file you want to write the selected statuses to.<br>- `num_posts_to_get`: integer value; the number of posts that you'd like to randomly select from the cumulative list of extreme sentiment posts. |

## Dependencies

- [Mastodon.py](https://pypi.org/project/Mastodon.py/)
- [pandas](https://pypi.org/project/pandas/)
- [nltk](https://pypi.org/project/nltk/)

### Virtual Environments

Installing these in a virtual environment is very easy and makes it so that these dependencies don't mingle with those on your system. It is best practice.

To create and use a simple `venv`, do

1. `python3 -m venv venv`
1. `source venv/bin/activate`
1. `pip install <dependency_name>`

To deactivate the venv when you're done with it: `deactivate`
