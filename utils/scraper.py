"""Module for webscraping.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-05-20
"""

from utils.settings import *
from utils.scrapers.characters import scrape_characters

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def scrape(mode=DEFAULT_MODE, url=URL, query=""):
    """Scrapes HTML data of characters from given URL."""
    data = {}
    match mode:
        # Scrape artifact data.
        case Mode.ARTIFACTS.value:
            raise Exception(f"Mode not implemented yet.")

        # Scrape character data.
        case Mode.CHARACTERS.value:
            try:
                data = scrape_characters(mode, url, query)
            except:
                raise Exception(f"Failed to scrape character {query}.")
        
        # Scrape weapons data.
        case Mode.WEAPONS.value:
            raise Exception(f"Mode not implemented yet.")
        
        # Unknown mode.
        case _:
            raise Exception(f"Unknown mode ({mode}) selected.")
    return data
