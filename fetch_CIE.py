import argparse
import yaml
import os
import requests
import itertools
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, stop_after_attempt, wait_random, RetryError


@retry(stop=stop_after_attempt(5), wait=wait_random(min=5, max=10))
def download_file(url, destination):
    Path(destination).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    filename = os.path.join(destination, url.split("/")[-1])
    with open(filename, mode="wb") as file:
        file.write(response.content)
    print(f"{filename} Downloaded")
    return filename


def download_file_with_logging(url, destination):
    try:
        return download_file(url, destination)
    except RetryError:
        print(f"Failed to download {url} after multiple attempts.")
        return None


def generate_urls(codes, seasons, years, paper_types, component_numbers, time_zones):
    url_template = "https://cie.fraft.cn/obj/Common/Fetch/redir/{}_{}{}_{}_{}{}.pdf"
    return [
        url_template.format(*combo)
        for combo in itertools.product(
            codes, seasons, years, paper_types, component_numbers, time_zones
        )
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--destination",
        help="Where to store downloaded files",
        default="downloads",
    )
    parser.add_argument(
        "-c",
        "--config",
        help="config file path",
        default="config.yaml",
    )
    args = parser.parse_args()

    with open(args.config, "r") as file:
        config = yaml.safe_load(file)

    urls = generate_urls(
        config["codes"],
        config["seasons"],
        config["years"],
        config["paper_types"],
        config["component_numbers"],
        config["time_zones"],
    )

    successful_downloads = []
    failed_downloads = []

    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(download_file_with_logging, url, args.destination): url
            for url in urls
        }
        for future in as_completed(futures):
            url = futures[future]
            try:
                result = future.result()
                if result:
                    successful_downloads.append(result)
                else:
                    failed_downloads.append(url)
            except Exception as e:
                print(f"An error occurred: {e}")
                failed_downloads.append(url)

    total_files = len(urls)
    successful_files = len(successful_downloads)
    failed_files = len(failed_downloads)
    success_percentage = (successful_files / total_files) * 100

    print("\nDownload Summary:")
    print(f"Total files: {total_files}")
    print(f"Successfully downloaded: {successful_files}")
    print(f"Failed to download: {failed_files}")
    print(f"Success rate: {success_percentage:.2f}%")

    if failed_files > 0:
        print("\nFailed Downloads:")
        for url in failed_downloads:
            print(url)
