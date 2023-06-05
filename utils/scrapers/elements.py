"""Module for scraping elements.

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
def get_all_elements_names():
    """Get all element names from the wiki."""
    names = []
    
    # Get HTML data from main page.
    response = requests_session.get("https://genshin-impact.fandom.com/wiki/Element")
    soup = BeautifulSoup(response.text, "lxml")
    
    # Find elements list.
    elements_div = soup.find("span", {"id": "List_of_Elements"}).find_parent("h2").find_next_sibling("i").find_next_sibling("ul")
    
    # Get names.
    for li in elements_div.find_all("li"):
        try:
            name = li.find("a").get("title")
            names.append(name)
        except:
            pass
    
    if names != []:
        return names
    else:
        return False


def scrape_elements(query=""):
    """Scrape element data from the wiki."""
    data = {}
    
    query = title_case(query).replace('"', '').replace(' ', '_')
    
    # Get HTML data from main page.
    response = requests_session.get(f"https://genshin-impact.fandom.com/wiki/{query}")
    soup = BeautifulSoup(response.text, "lxml")
    
    element_info_div = soup.find("aside", {"role": "region"})
    resonances_div = soup.find("span", {"id": "Elemental_Resonance"}).find_parent("h2").find_next_sibling("p").find_next_sibling("ul")
    reactions_div = soup.find("span", {"id": "Elemental_Reactions"}).find_parent("h2").find_next_sibling("p").find_next_sibling("ul")
    
    # Get elements data.
    try:
        data["name"] = element_info_div.find("h2", {"data-source": "name"}).text.strip()
        data["key"] = data["name"].upper()
        
        # Get resonances.
        data["resonances"] = []
        for li in resonances_div.find_all("li"):
            res = {}
            try:
                for br in li.find_all("br"):
                    br.replace_with("\n")
                for div in li.find_all("div"):
                    div.decompose()
                res["name"] = li.find("b").text.replace(":", "").strip()
                res["description"] = li.text.replace(res["name"] + ": ", "").strip()
                data["resonances"].append(res)
            except:
                pass
        
        # Get reactions.
        data["reactions"] = []
        for li in reactions_div.find_all("li"):
            reaction = {}
            
            # Skip sublists.
            if li.find_parent("ul") != reactions_div:
                continue
            
            try:
                for br in li.find_all("br"):
                    br.replace_with("\n")
                for div in li.find_all("div"):
                    div.decompose()
                reaction["name"] = li.find("b").text.replace(":", "").strip()
                
                try:
                    reaction["elements"] = []
                    if (query == "Anemo" and reaction["name"] == "Swirl") or (query == "Geo" and reaction["name"] == "Crystallize"):
                        reaction["elements"] = ["Pyro", "Hydro", "Electro", "Cryo"]
                    else:
                        for img in li.find_all("img"):
                            reaction["elements"].append(img.get("alt"))
                        reaction["elements"] = list(set(reaction["elements"]))
                        reaction["elements"].sort()
                except:
                    pass
                
                reaction["description"] = li.text.replace(reaction["name"] + ": ", "").strip()
                data["reactions"].append(reaction)
            except:
                pass
        
    except:
        return {}
    
    return data
