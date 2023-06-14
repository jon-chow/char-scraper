"""Module for scraping artifacts.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-06-05
"""

import lxml
import cchardet
from requests import Session, get
from bs4 import BeautifulSoup

from utils.settings import *
from utils.helpers import *

requests_session = Session()

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def get_all_artifacts_names():
    """Get all artifact names from the wiki."""
    # Get HTML data from main page.
    response = requests_session.get("https://genshin-impact.fandom.com/wiki/Artifact/Sets")
    soup = BeautifulSoup(response.text, "lxml")
    artifacts_trs = soup.find("tbody").find_all("tr")
    
    # Get names.
    names = []
    for tr in artifacts_trs:
        try:
            name = tr.find("td").find("a").get("title")
            if name != "Initiate":
                names.append(name)
        except:
            pass
    
    return names if names != [] else False


def scrape_artifacts(query=""):
    """Scrape artifact data from the wiki."""
    # Get HTML data from main page.
    data = {}
    query = title_case(query).replace('"', '').replace(' ', '_')
    response = requests_session.get(f"https://genshin-impact.fandom.com/wiki/{query}")
    soup = BeautifulSoup(response.text, "lxml")
    artifact_div = soup.find("aside", {"role": "region"})
    for br in artifact_div.find_all("br"):
        br.replace_with("\n")
    
    # Process data.
    data["name"] = artifact_div.find("h2", {"data-source": "title"}).text.strip()
    data["max_rarity"] = artifact_div.find_all("section")[1].find("div").find("ul").find_all("li")[-1].text.strip()[:1]
    try:
        data["2-piece_bonus"] = artifact_div.find("div", {"data-source": "2pcBonus"}).text.strip().replace("2-Piece Bonus\n", "")
        data["4-piece_bonus"] = artifact_div.find("div", {"data-source": "4pcBonus"}).text.strip().replace("4-Piece Bonus\n", "")
    except:
        data["1-piece_bonus"] = artifact_div.find("div", {"data-source": "1pcBonus"}).text.strip().replace("1-Piece Bonus\n", "")
    
    return data
