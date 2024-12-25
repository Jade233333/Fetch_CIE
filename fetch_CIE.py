import argparse
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import itertools
from tenacity import retry, stop_after_attempt, wait_random, RetryError


# Function to download files from the web
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

# Function to get user input for a list of items


def get_input(prompt, default=None):
    user_input = input(prompt).strip()
    return user_input.split() if user_input else [default]

# Function to generate URLs based on user inputs


def generate_urls(
        codes,
        seasons,
        years,
        paper_types,
        component_numbers,
        time_zones):
    url_template = "https://cie.fraft.cn/obj/Common/Fetch/redir/{}_{}{}_{}_{}{}.pdf"
    return [url_template.format(*combo) for combo in itertools.product(
        codes, seasons, years, paper_types, component_numbers, time_zones)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--destination",
                        help="Where to store downloaded files",
                        default="downloads")
    args = parser.parse_args()

    # Prompt user for input for each item
    codes = get_input("Enter code(s) (default 9701): ", "9701")
    seasons = get_input("Enter season(s) (default s): ", "s")
    years = get_input("Enter year(s) (default 23): ", "23")
    paper_types = get_input("Enter paper type(s) (default qp): ", "qp")
    component_numbers = get_input(
        "Enter component number(s) (default 2): ", "2")
    time_zones = get_input("Enter time zone(s) (default 1): ", "1")

    # Generate URLs using user inputs
    urls = generate_urls(codes, seasons, years, paper_types,
                         component_numbers, time_zones)

    successful_downloads = []
    failed_downloads = []

    # Use multi-threading to download the files
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(
            download_file_with_logging,
            url,
            args.destination): url for url in urls}
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
