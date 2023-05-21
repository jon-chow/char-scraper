"""Module for webscraping.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-05-20
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
    match category:
        # Get all artifact names.
        case Category.ARTIFACTS.value:
            return get_all_artifact_names()
        # Get all character names.
        case Category.CHARACTERS.value:
            return get_all_character_names()
        # Get all weapon names.
        case Category.WEAPONS.value:
            return get_all_weapon_names()
        # Unknown category.
        case _:
            raise Exception(f"Unknown category ({category}) selected.")


def scrape(category=DEFAULT_CATEGORY, query=""):
    """Scrapes HTML data of characters."""
    data = {}
    match category:
        # Scrape artifact data.
        case Category.ARTIFACTS.value:
            try:
                data = scrape_artifacts(query)
            except:
                raise Exception(f"Failed to scrape artifact '{query}'.")
        # Scrape character data.
        case Category.CHARACTERS.value:
            try:
                data = scrape_characters(query)
            except:
                raise Exception(f"Failed to scrape character '{query}'.")
        # Scrape weapons data.
        case Category.WEAPONS.value:
            try:
                data = scrape_weapons(query)
            except:
                raise Exception(f"Failed to scrape weapon '{query}'.")
        # Unknown category.
        case _:
            raise Exception(f"Unknown category ({category}) selected.")
    return data
