"""Module for scraping nations.

Author: jon-chow
Created: 2023-05-28
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
def get_all_nations_names():
    """Get all nation names from the wiki."""
    names = []
    
    # Get HTML data from main page.
    response = requests_session.get("https://genshin-impact.fandom.com/wiki/Teyvat")
    soup = BeautifulSoup(response.text, "lxml")
    
    # Find nations list.
    nations_div = soup.find("span", {"id": "Major_Nations"}).find_parent("h2").find_next_sibling("table").find("tbody")
    
    # Get names.
    for tr in nations_div.find_all("tr"):
        try:
            name = tr.find("td").find_all("a")[1].get("title")
            names.append(name)
        except:
            pass
    
    if names != []:
        return names
    else:
        return False


def scrape_nations(query=""):
    """Scrape nation data from the wiki."""
    data = {}
    
    query = title_case(query).replace('"', '').replace(' ', '_')
    
    # Get HTML data from main page.
    response = requests_session.get(f"https://genshin-impact.fandom.com/wiki/{query}")
    soup = BeautifulSoup(response.text, "lxml")
    # Get HTML data from Teyvat page.
    response2 = requests_session.get("https://genshin-impact.fandom.com/wiki/Teyvat")
    soup2 = BeautifulSoup(response2.text, "lxml")
    
    nation_info_div = soup.find("aside", {"role": "region"})
    archon_info_div = soup2.find("a", {"title": query}).find_parent("td").find_next_sibling("td").find_next_sibling("td")
    
    # Get nation data.
    try:
        data["name"] = nation_info_div.find("h2", {"data-source": "name"}).text.strip()
        data["element"] = nation_info_div.find("div", {"data-source": "element"}).find("div").find("a").text.strip()
        data["archon"] = {
            "name": archon_info_div.find_all("a")[0].text.strip(),
            "vessel": archon_info_div.find_all("a")[1].text.strip()
        }
        data["ideal"] = nation_info_div.find("div", {"data-source": "ideal"}).find("div").text.strip()
        data["mainCity"] = nation_info_div.find("div", {"data-source": "main city"}).find("div").find("a").text.strip()
        data["controllingEntity"] = nation_info_div.find("div", {"data-source": "controlling_entity"}).find("div").find("a").text.strip()
        
        # Get celebrated festivals.
        data["celebratedFestivals"] = []
        celebrated_festivals_div = nation_info_div.find("div", {"data-source": "festival"}).find("div")
        for a in celebrated_festivals_div.find_all("a"):
            data["celebratedFestivals"].append(a.text.strip())
    except:
        return {}
    
    return data
