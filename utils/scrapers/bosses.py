"""Module for scraping bosses.

Author: jon-chow
Created: 2023-05-28
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
def get_all_bosses_names():
    """Get all boss names from the wiki."""
    names = []
    
    # Get HTML data from main page.
    response = requests_session.get("https://genshin-impact.fandom.com/wiki/Enemies_of_Note")
    soup = BeautifulSoup(response.text, "lxml")
    
    # Find bosses list.
    bosses_div = soup.find("tbody")
    
    # Get names.
    for tr in bosses_div.find_all("tr"):
        try:
            name = tr.find("td").find("span", {"class": "item_text"}).find("a").text.strip()
            names.append(name)
        except:
            pass
    
    if names != []:
        return names
    else:
        return False


def scrape_bosses(query=""):
    """Scrape boss data from the wiki."""
    data = {}
    
    query = title_case(query).replace('"', '').replace(' ', '_')
    
    # Get HTML data from main page.
    response = requests_session.get("https://genshin-impact.fandom.com/wiki/Enemies_of_Note")
    soup = BeautifulSoup(response.text, "lxml")
    
    bosses_div = soup.find("tbody")
    
    # Get bosses data.
    try:
        # Get correct page and general data.
        for tr in bosses_div.find_all("tr"):
            try:
                if query.lower() == tr.find("td").find("span", {"class": "item_text"}).find("a").text.strip().replace('"', '').replace(' ', '_').lower():
                    challenge = tr.find_all("td")[3].find("a").get("href")
                    name = tr.find("td").find("span", {"class": "item_text"}).find("a").text.strip()
                    data["name"] = name
                    
                    title = tr.find_all("td")[1].text.strip()
                    if title != "":
                        data["title"] = title
                    else:
                        data["title"] = "-"
        
                    # Get HTML data from boss page.
                    response2 = requests_session.get(f"https://genshin-impact.fandom.com{challenge}")
                    soup2 = BeautifulSoup(response2.text, "lxml")
                    
                    # Get boss description.
                    desc_div = soup2.find("span", {"id": "Boss_Description"}).find_parent("h2").find_next_sibling("div").find("div", {"class": "description-content"})
                    for br in desc_div.find_all("br"):
                        br.replace_with("\n")
                    for div in desc_div.find_all("div"):
                        div.decompose()
                    data["description"] = desc_div.text.strip()
                    
                    # Get boss drops.
                    drops = []
                    drops_div = soup2.find_all("div", {"class": "card-container"})[:-5]
                    for drop in drops_div:
                        drops.append(drop.find("span").find("span").find("span").find("span").find("a").get("title").strip())
                    data["drops"] = list(set(drops))
                    data["drops"].sort()
                    
                    data["challenge"] = tr.find_all("td")[3].text.strip()
                    
                    # Get elements.
                    data["elements"] = []
                    for img in tr.find_all("td")[4].find_all("span"):
                        data["elements"].append(img.find("img").get("alt"))
                    data["elements"] = list(set(data["elements"]))
                    data["elements"].sort()
            except:
                pass
        
    except:
        return {}
    
    return data
