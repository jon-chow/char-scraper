"""Module for webscraping.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-05-21
"""

from utils.settings import *

from utils.scrapers.artifacts import scrape_artifacts, get_all_artifact_names
from utils.scrapers.characters import scrape_characters, get_all_character_names
from utils.scrapers.weapons import scrape_weapons, get_all_weapon_names

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def get_all_names(category=DEFAULT_CATEGORY):
    """Retrieves all names of items for the specified category."""
    is_unknown = True
    data = []
    
    # Iterate through all categories.
    for case in Category:
        if case.value == category:
            is_unknown = False
            try:
                data = globals()[f"get_all_{category[:-1]}_names"]()
            except:
                raise Exception(f"Failed to get names of {category[:-1]}.")
    
    # Check if unknown category was selected.
    if is_unknown:
        raise Exception(f"Unknown category ({category}) selected.")
    
    # Check if data was scraped successfully.
    if data == {}:
        raise Exception(f"Failed to scrape {category[:-1]} '{query}'.")
    else:
        return data


def scrape(category=DEFAULT_CATEGORY, query=""):
    """Scrapes HTML data of characters."""
    is_unknown = True
    data = {}
    
    # Iterate through all categories.
    for case in Category:
        if case.value == category:
            is_unknown = False
            try:
                data = globals()[f"scrape_{case.value}"](query=query)
            except:
                raise Exception(f"Failed to scrape {category[:-1]} '{query}'.")
    
    # Check if unknown category was selected.
    if is_unknown:
        raise Exception(f"Unknown category ({category}) selected.")
    
    # Check if data was scraped successfully.
    if data == {}:
        raise Exception(f"Failed to scrape {category[:-1]} '{query}'.")
    else:
        return data
