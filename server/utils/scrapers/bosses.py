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
    # Get HTML data from main page.
    response = requests_session.get("https://genshin-impact.fandom.com/wiki/Enemies_of_Note")
    soup = BeautifulSoup(response.text, "lxml")
    bosses_trs = soup.find("tbody").find_all("tr")
    
    # Get names.
    names = []
    for tr in bosses_trs:
        try:
            names.append(tr.find("td").find("span", {"class": "item_text"}).find("a").text.strip())
        except:
            pass
    
    return names if names != [] else False


def scrape_bosses(query=""):
    """Scrape boss data from the wiki."""
    # Get HTML data from main page.
    data = {}
    query = title_case(query).replace('"', '').replace(' ', '_')
    response = requests_session.get("https://genshin-impact.fandom.com/wiki/Enemies_of_Note")
    soup = BeautifulSoup(response.text, "lxml")
    bosses_div = soup.find("tbody")
    
    # Get bosses data.
    try:
        # Get correct page and general data.
        for tr in bosses_div.find_all("tr"):
            try:
                name = tr.find("td").find("span", {"class": "item_text"}).find("a").text.strip()
                if query.lower() == name.replace('"', '').replace(' ', '_').lower():
                    data["name"] = name
                    title = tr.find_all("td")[1].text.strip()
                    data["title"] = title if title != "" else "-"
        
                    # Get HTML data from boss page.
                    challenge = tr.find_all("td")[3].find("a").get("href")
                    response2 = requests_session.get(f"https://genshin-impact.fandom.com{challenge}")
                    soup2 = BeautifulSoup(response2.text, "lxml")
                    
                    # Get boss description.
                    desc_div = soup2.find("span", {"id": "Boss_Description"}).find_parent("h2").find_next_sibling("div").find("div")
                    for br in desc_div.find_all("br"):
                        br.replace_with("\n")
                    data["description"] = desc_div.text.strip()
                    
                    # Get boss drops.
                    drops = [drop.find("span").select_one("a").get("title").strip() for drop in soup2.find_all("div", {"class": "card-container"})[:-5]]
                    data["drops"] = list(set(drops))
                    data["drops"].sort()
                    
                    data["challenge"] = tr.find_all("td")[3].text.strip()
                    
                    # Get elements.
                    elements = [img.find("img").get("alt") for img in tr.find_all("td")[4].find_all("span")]
                    data["elements"] = list(set(elements))
                    data["elements"].sort()
            except:
                pass
        
    except:
        return {}
    
    return data
