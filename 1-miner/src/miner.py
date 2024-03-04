"""TODO."""

from pathlib import Path
import socket
import sys
import time

from mastodon import Mastodon
import mastodon.errors as mast_err

from src import utils


CLR = "\x1b[K"


def init(user_cfg):
    """TODO."""

    mastodon = init_instance(user_cfg)

    print("Beginning mining operation...")

    num_posts = 0
    starting_id = None

    existing_json_content = utils.read_jsonfile(user_cfg["output_path"])
    if existing_json_content is not None:
        num_posts = len(existing_json_content)
        starting_id = existing_json_content[-1]["id"]
        print(
            f"Resuming previous mining operation from {user_cfg['output_path']} at {starting_id}...\n"
        )
        print(f"There are currently {num_posts} posts...\n")

    mine_api(mastodon, user_cfg, starting_id, num_posts)


def init_instance(cfg):
    client_cred_file = cfg["client_credentials_file"]
    base_url = cfg["server_url"]

    if not Path(client_cred_file).exists():
        Mastodon.create_app(
            "community_miner", api_base_url=base_url, to_file=client_cred_file
        )

    mastodon = Mastodon(
        client_id=client_cred_file, api_base_url=base_url, ratelimit_method="throw"
    )

    mastodon.log_in(cfg["email"], cfg["password"], to_file=cfg["user_credentials_file"])

    return mastodon


def __sleep_miner():
    i = 300
    while i > 0:
        # modulo function returns time tuple
        minutes, seconds = divmod(i, 60)

        # format the time string before printing
        cntdown_str = f"{minutes:02d}:{seconds:02d}"

        print(
            f"{CLR}Time until limit reset: {cntdown_str}",
            end="\r",
        )

        time.sleep(1)
        i -= 1

    cur_time = time.strftime("%I:%M:%S %p", time.localtime())
    print(f"{CLR}Resuming mining! The time is {cur_time}...")


def mine_api(instance, cfg, max_id, num_posts):
    all_statuses = []

    while num_posts < cfg["max_posts"]:
        try:
            tag = cfg["tag"]
            results = instance.search(q=f"{tag}", result_type="statuses", max_id=max_id)

            statuses = results.get("statuses", [])
            if not statuses:
                print(f"No more statuses found. Terminating mining for {tag}.")
                break  # Break the loop if no more statuses are found

            all_statuses.extend(statuses)

            # Update min_id to the ID of the last status in this batch
            max_id = statuses[-1]["id"]
            num_posts += len(statuses)

            print(
                f"{CLR}Last status ID from batch: {max_id}, estimated total posts collected: {num_posts}, remaining API calls until ratelimiting: {instance.ratelimit_remaining}",
                end="\r",
            )

        except mast_err.MastodonRatelimitError:
            utils.write_merged_list_to_jsonfile(all_statuses, cfg["output_path"])
            __sleep_miner()

        except (
            KeyboardInterrupt,
            socket.error,
            socket.gaierror,
            mast_err.MastodonBadGatewayError,
            mast_err.MastodonAPIError,
        ):
            print("\nWriting gathered data...")
            utils.write_merged_list_to_jsonfile(all_statuses, cfg["output_path"])
            print(f"Terminating at ID {max_id}\n")
            print("---------------------------------------------\n")
            sys.exit(1)

    utils.write_merged_list_to_jsonfile(all_statuses, cfg["output_path"])
