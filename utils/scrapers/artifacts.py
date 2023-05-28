"""Module for scraping artifacts.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-05-20
"""

import re
import requests
import lxml
import cchardet
from bs4 import BeautifulSoup

from utils.settings import *
from utils.helpers import *

requests_session = requests.Session()

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def get_all_artifact_names():
    """Get all artifact names from the wiki."""
    names = []
    
    # Get HTML data from main page.
    response = requests_session.get("https://genshin-impact.fandom.com/wiki/Artifact/Sets")
    soup = BeautifulSoup(response.content, "lxml")
    
    # Find playable characters list.
    artifacts_div = soup.find("span", {"id": "List_of_Artifact_Sets"}).find_parent("h2").find_next_sibling("p").find_next_sibling("table").find("tbody")
    
    # Get names.
    for tr in artifacts_div.find_all("tr"):
        try:
            name = tr.find("td").find("a").get("title")
            if name != "Initiate":
                names.append(name)
        except:
            pass
    
    if names != []:
        return names
    else:
        return False


def scrape_artifacts(query=""):
    """Scrape artifact data from the wiki."""
    data = {}
    
    query = title_case(query).replace('"', '').replace(' ', '_')
    
    # Get HTML data from main page.
    response = requests_session.get(f"https://genshin-impact.fandom.com/wiki/{query}")
    soup = BeautifulSoup(response.content, "lxml")
    
    artifact_info_div = soup.find("aside", {"role": "region"})
    star_info_div = artifact_info_div.find_all("section")[1].find("div").find("ul")
    
    # Get artifact data.
    data["name"] = artifact_info_div.find("h2", {"data-source": "title"}).text.strip()
    data["max_rarity"] = star_info_div.find("li").find_next_sibling("li").text.strip()[:1]
    
    try:
        two_piece = artifact_info_div.find("div", {"data-source": "2pcBonus"})
        for br in two_piece.find_all("br"):
            br.replace_with("\n")
        data["2-piece_bonus"] = two_piece.text.strip().replace("2-Piece Bonus\n", "")
        
        four_piece = artifact_info_div.find("div", {"data-source": "4pcBonus"})
        for br in four_piece.find_all("br"):
            br.replace_with("\n")
        data["4-piece_bonus"] = four_piece.text.strip().replace("4-Piece Bonus\n", "")
    except:
        one_piece = artifact_info_div.find("div", {"data-source": "1pcBonus"})
        for br in one_piece.find_all("br"):
            br.replace_with("\n")
        data["1-piece_bonus"] = one_piece.text.strip().replace("1-Piece Bonus\n", "")
    
    return data
