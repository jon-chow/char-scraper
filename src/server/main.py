"""Script for generating JSON character data from web scraping.

Author: jon-chow
Created: 2023-05-19
Last Modified: 2023-06-13
"""

import shutil
import sys
import time
import colorama
from json import dump
from os import path, makedirs
from colorama import Fore, Back, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.helpers import paginate_output
from utils.settings import *
from utils.scrapers import scrape, get_all_names


colorama.init(autoreset=True)

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def create_json(category=DEFAULT_CATEGORY, folders=[], lang=LANG):
    """Generates JSON files for each folder."""
    start_time = time.time()
    
    # Get all if none are specified.
    folders = get_all_names(category=category) if folders == [] else folders
    
    def create_folder(folder):
        """Creates a folder for each folder name."""
        folder_name = folder.replace(' ', '-').replace("'", '').replace('"', '').replace('(', '').replace(')', '').lower()
        folder_dir = path.join(DATA_SAVE_DIR, category, folder_name)
        try:
            data = scrape(category=category, query=folder)
            makedirs(folder_dir, exist_ok=True)
            with open(path.join(folder_dir, f"{lang}.json"), "w", encoding="utf-8") as f:
                dump(data, f, indent=2, ensure_ascii=False)
            return f"{Fore.CYAN}Created {path.join(folder_dir, f'{lang}.json')}"
        except Exception as e:
            # Failed to create JSON file.
            return f"{Fore.RED}Error: {e}"
    
    # Create a folder for each folder name.
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_folder, folder) for folder in folders]
        for future in as_completed(futures):
            print(f"{future.result()} in{Fore.YELLOW}{time.time() - start_time: .2f} seconds.")


def clear(category="", folders=[]):
    """Removes specified folders and its files."""
    # Remove all files and directories in all categories.
    if category == "":
        shutil.rmtree(DATA_SAVE_DIR)
        print(f"{Fore.CYAN}Removed {DATA_SAVE_DIR}")
        
    # Remove all files and directories in the specified category.
    elif folders == []:
        folder_dir = f"{DATA_SAVE_DIR}{category}"
        shutil.rmtree(folder_dir)
        print(f"{Fore.CYAN}Removed {folder_dir}")  
               
    # Remove specified files and directory in the specified category.
    else:
        for (folder) in folders:
            folder = folder.replace(' ', '-').replace("'", '').replace('"', '').replace('(', '').replace(')', '').lower()
            folder_dir = f"{DATA_SAVE_DIR}{category}/{folder}"
            shutil.rmtree(folder_dir)
            print(f"{Fore.CYAN}Removed {folder_dir}")


def list_category(category=""):
    """Lists items for the given category."""
    items = []
    # List all categories.
    if category == "":
        print(f"{Fore.CYAN}List of {Fore.YELLOW}Categories:")
        items = list(map(lambda x: x.value.title(), Category))
        items.sort(key=lambda x: x.lower())
    
    # List all items for the given category.
    else:
        data = get_all_names(category=category)
        print(f"{Fore.CYAN}List of {Fore.YELLOW}{category.title()} ({data.__len__()}):")
        items = list(map(lambda x: x, data))
        items.sort(key=lambda x: x.lower())
    
    # Paginate output.
    paginate_output(items, 10)


# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #
def genshin_scraper(function, category="", folders=[]):
    """Main function for running the script."""
    try:
        # Run the CLEAR function.
        if function == Functions.CLEAR.value:
            try:
                clear(category=category, folders=folders)
            except Exception as e:
                raise Exception(f"Invalid category '{category}' does not exist.")

        # Run the CREATE function.
        elif function == Functions.CREATE.value:
            if category == "":
                raise Exception("A category is required.")
            try:
                create_json(category=category, folders=folders)
            except Exception as e:
                raise Exception(f"Invalid category '{category}' does not exist.")

        # Run the LIST function.
        elif function == Functions.LIST.value:
            try:
                list_category(category=category)
            except Exception as e:
                raise Exception(f"Invalid category '{category}' does not exist.")

        # Invalid function.
        else:
            raise Exception(f"Invalid function '{function}' does not exist.")
    except Exception as e:
        raise e


if __name__ == "__main__":
    try:
        function = "" if len(sys.argv) < 2 else sys.argv[1]
        category = "" if len(sys.argv) < 3 else sys.argv[2]
        folders = [] if len(sys.argv) < 4 else sys.argv[3:]
        
        genshin_scraper(function, category, folders)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
