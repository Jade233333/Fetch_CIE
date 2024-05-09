from concurrent.futures import ThreadPoolExecutor
import requests
import itertools
import argparse

# Function to download files from web
def download_file(url):
    response = requests.get(url)
    status_code = response.status_code
    filename = url.split("/")[-1]
    if response.status_code == 200:
        with open(f"{args.destination}{filename}", mode="wb") as file:
            file.write(response.content)
        print(f"{filename} Downloaded")
    else:
        print(f"{filename} Error status_code {response.status_code}") 

# Function to get user input for a list of items
def get_input(prompt, items, default=None):
    user_input = input(prompt).strip()
    if user_input:
        items.extend(user_input.split())
    elif default is not None:
        items.append(default)


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--destination", help="where to store downloaded file", default="")
args = parser.parse_args()

# Initialize empty lists for each item
codes = []
seasons = []
years = []
paper_types = []
component_numbers = []
time_zones = []

# Prompt user for input for each item
get_input("Enter code(s) (default 9701): ", codes, "9701")
get_input("Enter season(s) (default s): ", seasons, "s")
get_input("Enter year(s) (default 23): ", years, "23")
get_input("Enter paper type(s) (default qp): ", paper_types, "qp")
get_input("Enter component number(s) (default 2): ",component_numbers, "2")
get_input("Enter time zone(s) (default 1): ", time_zones, "1")

# URL template
url_template = "https://cie.fraft.cn/obj/Fetch/redir/{}_{}{}_{}_{}{}.pdf"

# Generate URLs using itertools.product
urls = [url_template.format(*combo) for combo in itertools.product(codes, seasons, years, paper_types, component_numbers, time_zones)]
print(urls)

# Use multi-treading to download the files
with ThreadPoolExecutor() as executor:
    executor.map(download_file, urls)