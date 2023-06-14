"""Module for scraping weapons.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-06-05
"""

import json
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
def rename_location(string):
    """Renames location."""
    return {
        "Wishes": "Gacha",
        "Weapon Event Wishes": "Gacha",
        "Chests": "Chest",
        "Paimon's Bargains": "Starglitter Exchange",
        "Battle Pass": "BP Bounty",
    }.get(string, string)


def get_all_weapons_names():
    """Get all weapon names from the wiki."""
    # Get HTML data from main page.
    response = requests_session.get("https://genshin-impact.fandom.com/wiki/Weapon/List")
    soup = BeautifulSoup(response.text, "lxml")
    weapons_trs = soup.find("tbody").find_all("tr")
    
    # Get names.
    names = []
    for tr in weapons_trs:
        try:
            names.append(tr.find("td").find("a").get("title"))
        except:
            pass
    
    return names if names != [] else False


# TODO: REFACTOR THIS
def scrape_weapons(query=""):
    """Scrape weapon data from the wiki."""
    data = {}
    
    query = title_case(query).replace('"', '').replace(' ', '_')
    
    # Get HTML data from main page.
    response = requests_session.get(f"https://genshin-impact.fandom.com/wiki/{query}")
    soup = BeautifulSoup(response.text, "lxml")
    
    weapon_info_div = soup.find("aside", {"role": "region"})
    stats_info_div = weapon_info_div.find("a", {"title": "Attribute"}).find_parent("h2").find_next_sibling("section").find("section")
    
    # Get weapon data.
    data["name"] = soup.find("span", {"class": "mw-page-title-main"}).text.strip()
    data["type"] = weapon_info_div.find("div", {"data-source": "type"}).find("div").text.strip()
    data["rarity"] = get_int_from_string(weapon_info_div.find("div", {"data-source": "quality"}).find("img").get("alt"))
    data["baseAttack"] = stats_info_div.find_all("section")[1].find("div").text.strip().split(" - ")[0]
    
    if data["rarity"] > 2 and "Prized_Isshin_Blade" not in query:
        refinement_info_div = weapon_info_div.find("a", {"title": "Refinement Rank"}).find_parent("h2").find_next_sibling("section").find("section")

        data["subStat"] = stats_info_div.find_all("section")[1].find_all("div")[1].text.strip()
        data["subStatBase"] = stats_info_div.find_all("section")[1].find_all("div")[2].text.strip().split(" - ")[0]
        data["passiveName"] = refinement_info_div.find("th", {"data-source": "eff_rank1_var1"}).text.strip()
        passive_desc = refinement_info_div.find("td", {"data-source": "eff_rank1_var1"})
        for br in passive_desc.find_all("br"):
            br.replace_with("\n")
        data["passiveDesc"] = passive_desc.text.strip()
    else:
        data["subStat"] = data["subStatBase"] = data["passiveName"] = data["passiveDesc"] = "-"
    
    if "Prized_Isshin_Blade" not in query:
        location = weapon_info_div.find("div", {"data-source": "obtain"}).find("div").find_all()[0].text.strip()
        data["location"] = rename_location(location)
    
        ascension_info_div = soup.find("span", {"id": "Ascensions_and_Stats"}).find_parent("h2").find_next_sibling("table").find("tr", {"class": "ascension"})
        data["ascensionMaterial"] = ascension_info_div.find("td").find("div").find_next_sibling().find("a").get("title").strip()
    else:
        data["location"] = "-"
        data["ascensionMaterial"] = "Mask Of The Wicked Lieutenant"
    
    return data
