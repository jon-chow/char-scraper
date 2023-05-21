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
def get_all_names(mode=DEFAULT_MODE):
    """Retrieves all names of items for the specified mode."""
    match mode:
        # Get all artifact names.
        case Mode.ARTIFACTS.value:
            return get_all_artifact_names()
        # Get all character names.
        case Mode.CHARACTERS.value:
            return get_all_character_names()
        # Get all weapon names.
        case Mode.WEAPONS.value:
            return get_all_weapon_names()
        # Unknown mode.
        case _:
            raise Exception(f"Unknown mode ({mode}) selected.")


def scrape(mode=DEFAULT_MODE, query=""):
    """Scrapes HTML data of characters."""
    data = {}
    match mode:
        # Scrape artifact data.
        case Mode.ARTIFACTS.value:
            try:
                data = scrape_artifacts(query)
            except:
                raise Exception(f"Failed to scrape artifact '{query}'.")
        # Scrape character data.
        case Mode.CHARACTERS.value:
            try:
                data = scrape_characters(query)
            except:
                raise Exception(f"Failed to scrape character '{query}'.")
        # Scrape weapons data.
        case Mode.WEAPONS.value:
            try:
                data = scrape_weapons(query)
            except:
                raise Exception(f"Failed to scrape weapon '{query}'.")
        # Unknown mode.
        case _:
            raise Exception(f"Unknown mode ({mode}) selected.")
    return data
