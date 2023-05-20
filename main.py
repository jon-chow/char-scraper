"""Script for generating JSON character data from web scraping.

Author: jon-chow
Created: 2023-05-19
Last Modified: 2023-05-20
"""

import json
import os
import sys
from settings import *
from scraper import scrape

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def create_json(mode=DEFAULT_MODE, folders=FOLDERS, file_name=LANG):
    """Generates JSON files for each folder."""
    for (folder) in folders:
        folder_dir = f"{DATA_SAVE_DIR}{mode}/{folder.lower().replace(' ', '-')}"
        # Create directory if it doesn't exist.
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)
        
        # Create and store JSON data.
        with open(f"{folder_dir}/{file_name}.json", "w") as f:
            data = scrape(mode=mode, query=folder.title().replace(' ', '_'))
            json.dump(data, f, indent=2)


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
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        # Get folders from command line arguments if they exist.
        if len(sys.argv) > 2:
            folders = sys.argv[2:]
            create_json(mode=mode, folders=folders)
        # Otherwise, use default.
        else:
            create_json(mode=mode)
    else:
        print("No arguments passed. Exiting...")
        sys.exit(1)
    
if __name__ == "__main__":
    main()
