"""Module for webscraping.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-05-28
"""

from utils.settings import *

from .artifacts import *
from .bosses import *
from .characters import *
from .elements import *
from .nations import *
from .weapons import *

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
                data = globals()[f"get_all_{category}_names"]()
            except:
                raise Exception(f"Failed to get names of {category}.")
    
    # Check if unknown category was selected.
    if is_unknown:
        raise Exception(f"Unknown category ({category}) selected.")
    
    # Check if data was scraped successfully.
    if data == {}:
        raise Exception(f"Failed to scrape {category} '{query}'.")
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
                raise Exception(f"Failed to scrape {category} '{query}'.")
    
    # Check if unknown category was selected.
    if is_unknown:
        raise Exception(f"Unknown category ({category}) selected.")
    
    # Check if data was scraped successfully.
    if data == {}:
        raise Exception(f"Failed to scrape {category} '{query}'.")
    else:
        return data