"""Script for generating JSON data from web scraping.

Author: jon-chow
Created: 2023-05-19
Last Modified: 2023-05-19
"""

import json
import os
import requests
import sys
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------- #
#                             CONSTANTS / VARIABLES                            #
# ---------------------------------------------------------------------------- #
URL = "https://en.wikipedia.org/wiki/"
DATA_SAVE_DIR = "assets/data/"
IMG_SAVE_DIR = "assets/images/"
FOLDERS = ["potato"]
LANG = "en"

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def scrape(url=URL, query=""):
    """Scrapes HTML data from given URL."""
    data = {}
    
    try:
        # Get HTML data from URL.
        page = requests.get(f"{URL}{query}")
        soup = BeautifulSoup(page.content, "html.parser")
        
        # TODO: Get data from HTML.
        data["title"] = soup.find("span", { "class": "mw-page-title-main" }).text
        data["first"] = soup.find("span", { "class": "mw-headline" }).text
    except:
        print(f"Error: Could not scrape {URL}{query}.")
    
    return data


def create_json(folders=FOLDERS, file_name=LANG):
    """Generates JSON files for each folder."""
    for (folder) in folders:
        folder_dir = f"{DATA_SAVE_DIR}{folder}"
        # Create directory if it doesn't exist.
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)
        
        # Create and store JSON data.
        with open(f"{folder_dir}/{file_name}.json", "w") as f:
            data = scrape(query=folder)
            json.dump(data, f, indent=4)


def clean_up(folders=FOLDERS):
    """Removes specified folders and its files."""
    for (folder) in folders:
        folder_dir = f"{DATA_SAVE_DIR}{folder}"
        # Remove files and directory if it exists.
        if os.path.exists(folder_dir):
            for file in os.listdir(folder_dir):
                os.remove(f"{folder_dir}/{file}")
            os.rmdir(folder_dir)

# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #
def main():
    """Main function."""
    # Get folders from command line arguments if they exist.
    if len(sys.argv) > 1:
        folders = sys.argv[1:]
        create_json(folders)
    # Otherwise, use default.
    else:
        create_json()
    
if __name__ == "__main__":
    main()
