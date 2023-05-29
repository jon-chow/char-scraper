"""Script for generating JSON character data from web scraping.

Author: jon-chow
Created: 2023-05-19
Last Modified: 2023-05-28
"""

import json
import os
import sys
import time
import colorama
from colorama import Fore, Back, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.helpers import paginate_output
from utils.settings import *
from utils.scraper import scrape, get_all_names

colorama.init(autoreset=True)

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def create_json(category=DEFAULT_CATEGORY, folders=[], lang=LANG):
    """Generates JSON files for each folder."""
    start_time = time.time()
    
    # Get all if none are specified.
    if folders == []:
        folders = get_all_names(category=category)
    
    def create_folder(folder):
        """Creates a folder for each folder name."""
        folder_name = folder.replace(' ', '-').replace("'", '').replace('"', '').replace('(', '').replace(')', '').lower()
        folder_dir = f"{DATA_SAVE_DIR}{category}/{folder_name}"
        try:
            data = scrape(category=category, query=folder)
            # Create directory if it doesn't exist.
            if not os.path.exists(folder_dir):
                os.makedirs(folder_dir)
            # Create JSON file.
            with open(f"{folder_dir}/{lang}.json", "w") as f:
                json.dump(data, f, indent=2)
                return (f"{Fore.CYAN}Created /{folder_dir}/{lang}.json")
        except Exception as e:
            # Failed to create JSON file.
            return (f"{Fore.RED}Error: {e}")
    
    # Create a folder for each folder name.
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_folder, folder) for folder in folders]
        for future in as_completed(futures):
            print(f"{future.result()} in{Fore.YELLOW}{time.time() - start_time: .2f} seconds.")


def clear(category="", folders=[]):
    """Removes specified folders and its files."""
    # Remove all files and directories in all categories.
    if category == "":
        for root, dirs, files in os.walk(DATA_SAVE_DIR, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                dir_dir = os.path.join(root, name).replace('\\', '/')
                os.rmdir(dir_dir)
                print(f"{Fore.CYAN}Removed /{dir_dir}")
                    
    # Remove all files and directories in the specified category.
    elif folders == []:
        folder_dir = f"{DATA_SAVE_DIR}{category}"
        if os.path.exists(folder_dir):
            for root, dirs, files in os.walk(folder_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    dir_dir = os.path.join(root, name).replace('\\', '/')
                    os.rmdir(dir_dir)
                    print(f"{Fore.CYAN}Removed /{dir_dir}")
                
    # Remove specified files and directory in the specified category.
    else:
        for (folder) in folders:
            folder = folder.replace(' ', '-').replace("'", '').replace('"', '').replace('(', '').replace(')', '').lower()
            folder_dir = f"{DATA_SAVE_DIR}{category}/{folder}"
            if os.path.exists(folder_dir):
                for file in os.listdir(folder_dir):
                    os.remove(f"{folder_dir}/{file}")
                os.rmdir(folder_dir)
                print(f"{Fore.CYAN}Removed {folder_dir}")


def list_category(category=""):
    """Lists items for the given category."""
    items = []
    # List all categories.
    if category == "":
        print(f"{Fore.CYAN}List of {Fore.YELLOW}Categories:")
        for (item) in Category:
            items.append(item.value.title())
        items.sort(key=lambda x: x.lower())
    
    # List all items for the given category.
    else:
        data = get_all_names(category=category)
        print(f"{Fore.CYAN}List of {Fore.YELLOW}{category.title()} ({data.__len__()}):")
        for (item) in data:
            items.append(item)
        items.sort(key=lambda x: x.lower())
    
    # Paginate output.
    paginate_output(items, 10)


# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #
def main():
    """Main function."""
    if len(sys.argv) > 1:
        function = sys.argv[1]
        
        match function:
            # Clear function.
            case Functions.CLEAR.value:
                try:
                    if len(sys.argv) > 2:
                        category = sys.argv[2]
                        if len(sys.argv) > 3:
                            folders = sys.argv[3:]
                            clear(category=category, folders=folders)
                        else:
                            clear(category=category)
                    else:
                        clear()
                except Exception as e:
                    raise Exception(f"Invalid category '{category}' does not exist.")
            
            # Create function.
            case Functions.CREATE.value:
                try:
                    category = sys.argv[2]
                    if len(sys.argv) > 3:
                        folders = sys.argv[3:]
                        create_json(category=category, folders=folders)
                    else:
                        create_json(category=category)
                except Exception as e:
                    raise Exception(f"Invalid category '{category}' does not exist.")
            
            # List function.
            case Functions.LIST.value:
                try:
                    if len(sys.argv) > 2:
                        category = sys.argv[2]
                        list_category(category=category)
                    else:
                        list_category()
                except Exception as e:
                    raise Exception(f"Invalid category '{category}' does not exist.")
            
            # Unknown function.
            case _:
                raise Exception(f"Invalid function '{function}' does not exist.")
    else:
        raise Exception(f"Missing arguments.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
