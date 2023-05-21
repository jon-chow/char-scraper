"""Module for webscraping.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-05-20
"""

from utils.settings import *

from utils.scrapers.data.characters import scrape_characters
from utils.scrapers.data.artifacts import scrape_artifacts
from utils.scrapers.data.weapons import scrape_weapons

from utils.scrapers.names.artifacts import get_all_artifact_names
from utils.scrapers.names.characters import get_all_character_names
from utils.scrapers.names.weapons import get_all_weapon_names

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


def scrape(mode=DEFAULT_MODE, url=URL, query=""):
    """Scrapes HTML data of characters from given URL."""
    data = {}
    match mode:
        # Scrape artifact data.
        case Mode.ARTIFACTS.value:
            try:
                data = scrape_artifacts(url, query)
            except:
                raise Exception(f"Failed to scrape artifact '{query}'.")
        # Scrape character data.
        case Mode.CHARACTERS.value:
            try:
                data = scrape_characters(url, query)
            except:
                raise Exception(f"Failed to scrape character '{query}'.")
        # Scrape weapons data.
        case Mode.WEAPONS.value:
            try:
                data = scrape_weapons(url, query)
            except:
                raise Exception(f"Failed to scrape weapon '{query}'.")
        # Unknown mode.
        case _:
            raise Exception(f"Unknown mode ({mode}) selected.")
    return data
