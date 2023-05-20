"""Module for getting the names of all playable characters.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-05-20
"""

import re
import requests
from bs4 import BeautifulSoup

from utils.helpers import *

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def get_all_character_names():
    names = []
    
    # Get HTML data from main page.
    response = requests.get("https://genshin-impact.fandom.com/wiki/Character/List")
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find playable characters list.
    playable_characters_div = soup.find("span", {"id": "Playable_Characters"}).find_parent("h2").find_next_sibling("p").find_next_sibling("table").find("tbody")
    
    # Get names.
    for tr in playable_characters_div.find_all("tr"):
        try:
            name = tr.find("td").find("a").get("title").lower()
            names.append(name)
        except:
            pass
    
    if names != []:
        return names
    else:
        return False
