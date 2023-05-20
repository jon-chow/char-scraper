"""Script for generating JSON character data from web scraping.

Author: jon-chow
Created: 2023-05-19
Last Modified: 2023-05-20
"""

import json
import os
import sys
import colorama
from colorama import Fore, Back, Style

from utils.settings import *
from utils.scraper import scrape

colorama.init(autoreset=True)

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def create_json(mode=DEFAULT_MODE, folders=FOLDERS, lang=LANG):
    """Generates JSON files for each folder."""
    for (folder) in folders:
        folder_dir = f"{DATA_SAVE_DIR}{mode}/{folder.lower().replace(' ', '-')}"
        try:
            data = scrape(mode=mode, query=folder.replace('-', ' ').title().replace(' ', '_'))
            # Create directory if it doesn't exist.
            if not os.path.exists(folder_dir):
                os.makedirs(folder_dir)
            # Create JSON file.
            with open(f"{folder_dir}/{lang}.json", "w") as f:
                json.dump(data, f, indent=2)
                print(f"{Fore.CYAN}Created {folder_dir}/{lang}.json")
        except Exception as e:
            # Failed to create JSON file.
            print(f"{Fore.RED}Error: {e}")


def clean_up(folders=""):
    """Removes specified folders and its files."""
    folder_dir = f"{DATA_SAVE_DIR}characters"
    if folders == "":
        # Remove all files and directories in the data save directory.
        if os.path.exists(folder_dir):
            for file in os.listdir(folder_dir):
                for subfile in os.listdir(f"{folder_dir}/{file}"):
                    os.remove(f"{folder_dir}/{file}/{subfile}")
                os.rmdir(f"{folder_dir}/{file}")
                print(f"{Fore.CYAN}Removed {folder_dir}/{file}")
    else:
        # Remove specified files and directory if they exist.
        for (folder) in folders:
            folder_dir = f"{folder_dir}/{folder}"
            if os.path.exists(folder_dir):
                for file in os.listdir(folder_dir):
                    os.remove(f"{folder_dir}/{file}")
                os.rmdir(folder_dir)
                print(f"{Fore.CYAN}Removed {folder_dir}")

# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #
def main():
    """Main function."""
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        match mode:
            # Artifacts mode.
            case Mode.ARTIFACTS.value:
                raise Exception(f"Mode not implemented yet.")
            
            # Characters mode.
            case Mode.CHARACTERS.value:
                # Get folders from command line arguments if they exist.
                if len(sys.argv) > 2:
                    folders = sys.argv[2:]
                    create_json(mode=mode, folders=folders)
                else:
                    create_json(mode=mode)
            
            # Weapons mode.
            case Mode.WEAPONS.value:
                raise Exception(f"Mode not implemented yet.")
            
            # Clean mode.
            case Mode.CLEAN.value:
                # Get folders from command line arguments if they exist.
                if len(sys.argv) > 2:
                    folders = sys.argv[2:]
                    clean_up(folders=folders)
                else:
                    clean_up()
            
            # Unknown mode.
            case _:
                raise Exception(f"Invalid mode '{mode}' does not exist.")
    else:
        raise Exception(f"No arguments were passed.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
