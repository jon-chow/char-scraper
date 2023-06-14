"""Module for scraping characters.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-06-14
"""

import json
import lxml
import cchardet
from re import search
from requests import Session, get
from bs4 import BeautifulSoup

from utils.settings import *
from utils.helpers import *

requests_session = Session()

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def get_all_characters_names():
    """Get all character names from the wiki."""
    # Get HTML data from main page.
    response = requests_session.get("https://genshin-impact.fandom.com/wiki/Character/List")
    soup = BeautifulSoup(response.text, "lxml")
    characters_trs = soup.find("tbody").find_all("tr")
    
    # Get names.
    names = []
    for tr in characters_trs:
        try:
            name = tr.find("td").find("a").get("title")
            if name != "Traveler":
                names.append(name)
            else:
                elements = ["Unaligned", "Anemo", "Geo", "Electro", "Dendro"] # "Hydro", "Pyro", "Cryo"
                names.extend([f"Traveler ({element})" for element in elements])
        except:
            pass
    
    return names if names != [] else False


# TODO: REFACTOR THIS
def scrape_travelers(resonance="Anemo"):
    """Scrape traveler data from the wiki."""
    data = {}
    
    # Get HTML data from main page.
    mainRes = requests_session.get(f"https://genshin-impact.fandom.com/wiki/Traveler_({resonance})")
    mainSoup = BeautifulSoup(mainRes.text, "lxml")
    
    talent_div = mainSoup.find("table", {"class": "talent-table"})
    constellation_div = mainSoup.find("table", {"class": "constellation-table"})
    
    # Pre-populate with general data about the traveler.
    data["name"] = "Traveler"
    data["title"] = "Outlander"
    data["vision"] = "None"
    data["weapon"] = "Sword"
    data["gender"] = ["Male (Aether)", "Female (Lumine)"]
    data["nation"] = "-"
    data["affiliation"] = "-"
    data["specialDish"] = "-"
    data["namecard"] = "-"
    data["rarity"] = 5
    data["constellation"] = "Viator/Viatrix"
    data["birthday"] = "-"
    data["description"] = "A traveler from another world who had their only kin taken away, forcing them to embark on a journey to find The Seven."
    
    # Get skill talents data.
    skill_talents = []
    if resonance != "Unaligned":
        def get_skill_talent(title):
            skill_div = talent_div.find("a", {"title": title}).find_parent("td").find_parent("tr")
            skill_name = skill_div.find_all("td")[1].find("a").text.strip()
            
            upgrades=[]
            upgrades_div = skill_div.find_next_sibling("tr").find("div", {"data-expandtext": "▼Attribute Scaling▼"}).find("table", {"class": "wikitable"}).find("tbody")
            for tr in upgrades_div.find_all("tr")[1:]:
                try:
                    name = tr.find("th").text.strip()
                    value = tr.find("td").text.strip()
                    
                    if "%" in name:
                        name = name.replace("(%)", "").strip()
                        value = convert_to_percentage_string(value)
                    
                    upgrades.append({
                        "name": name,
                        "value": value
                    })
                except:
                    pass
            
            # Combine "Low Plunge DMG" and "High Plunge DMG" into "Low / High Plunge DMG".
            for i in range(len(upgrades)):
                if upgrades[i]["name"] == "Low Plunge DMG":
                    upgrades[i]["name"] = "Low / High Plunge DMG"
                    upgrades[i]["value"] = f"{upgrades[i]['value']} / {upgrades[i+1]['value']}"
                    upgrades.pop(i+1)
                    break
            
            skill_desc = skill_div.find_next_sibling("tr").find("td")
            for br in skill_desc.find_all("br"):
                br.replace_with("\n")
            for div in skill_desc.find_all("div"):
                div.decompose()
            skill_desc = skill_desc.text.strip()
            
            skill_talents.append({
                "name": skill_name,
                "unlock": title,
                "description": skill_desc,
                "upgrades": upgrades,
                "type": title.upper().replace(" ", "_")
            })
        
        get_skill_talent(title="Normal Attack")
        get_skill_talent(title="Elemental Skill")
        get_skill_talent(title="Elemental Burst")
        
        data["skillTalents"] = skill_talents
        
        # Get passive talents data.
        passive_talents = []
        first_passive_talent_div = talent_div.find("a", {"title": "1st Ascension Passive"}).find_parent("td").find_parent("tr")
        first_passive_name = first_passive_talent_div.find_all("td")[1].find("a").text.strip()
        first_passive_desc = first_passive_talent_div.find_next_sibling("tr").find("td")
        for br in first_passive_desc.find_all("br"):
            br.replace_with("\n")
        for div in first_passive_desc.find_all("div"):
            div.decompose()
        first_passive_desc = first_passive_desc.text.strip()
        passive_talents.append({
            "name": first_passive_name,
            "unlock": f"Unlocked at Ascension {1}",
            "description": first_passive_desc,
            "level": 1
        })
        
        fourth_passive_talent_div = talent_div.find("a", {"title": "4th Ascension Passive"}).find_parent("td").find_parent("tr")
        fourth_passive_name = fourth_passive_talent_div.find_all("td")[1].find("a").text.strip()
        fourth_passive_desc = fourth_passive_talent_div.find_next_sibling("tr").find("td")
        for br in fourth_passive_desc.find_all("br"):
            br.replace_with("\n")
        for div in fourth_passive_desc.find_all("div"):
            div.decompose()
        fourth_passive_desc = fourth_passive_desc.text.strip()
        
        data["passiveTalents"] = passive_talents
        
        # Get constellations data.
        constellations = []
        def get_constellations(level):
            constellations_div = constellation_div.find("tbody")
            constellation_name = constellations_div.find_all("tr")[level * 2 - 1].find_all("td")[1].find("a").text.strip()
            constellation_desc = constellations_div.find_all("tr")[level * 2].find("td")
            for br in constellation_desc.find_all("br"):
                br.replace_with("\n")
            for div in constellation_desc.find_all("div"):
                div.decompose()
            constellation_desc = constellation_desc.text.strip()
            
            constellations.append({
                "name": constellation_name,
                "unlock": f"Constellation Lv. {level}",
                "description": constellation_desc,
                "level": level
            })
        
        for i in range(1, 7):
            get_constellations(i)
        
        data["constellations"] = constellations
    else:
        data["skillTalents"] = [{
            "name": "Normal Attack",
            "unlock": "Normal Attack",
            "description": "Normal Attack: Perform up to 5 rapid strikes.\n\nCharged Attack: Consumes a certain amount of Stamina to unleash 2 rapid sword strikes.\n\nPlunging Attack: Plunges from mid-air to strike the ground below, damaging opponents along the path and dealing AoE DMG upon impact.",
            "upgrades": [
                { "name": "1-Hit DMG", "value": "44.5%" },
                { "name": "2-Hit DMG", "value": "43.4%" },
                { "name": "3-Hit DMG", "value": "53.0%" },
                { "name": "4-Hit DMG", "value": "58.3%" },
                { "name": "5-Hit DMG", "value": "70.8%" },
                { "name": "Charged Attack DMG", "value": ["55.9% + 60.7% (Aether)", "55.9% + 72.2% (Lumine)"] },
                { "name": "Charged Attack Stamina Cost", "value": "20" },
                { "name": "Plunge DMG", "value": "63.9%" },
                { "name": "Low / High Plunge DMG", "value": "127.8% / 159.7%" }
            ]
        }]
        data["passiveTalents"] = []
        data["constellations"] = []
    
    # Misc data.
    data["vision_key"] = "NONE"
    data["weapon_type"] = "SWORD"

    return data


def scrape_characters(query=""):
    """Scrape character data from the wiki."""
    data = {}
    
    # If the character is traveler, scrape for traveler data instead.
    if "traveler" in query.lower():
        resonance = query.split(" ")[1].replace("(", "").replace(")", "").title()
        return scrape_travelers(resonance)
    
    query = title_case(query).replace('"', '').replace(' ', '_')
    
    # Get HTML data from main page.
    mainRes = requests_session.get(f"https://genshin-impact.fandom.com/wiki/{query}")
    mainSoup = BeautifulSoup(mainRes.text, "lxml")
    # Get HTML data from lore page.
    loreRes = requests_session.get(f"https://genshin-impact.fandom.com/wiki/{query}/Lore")
    loreSoup = BeautifulSoup(loreRes.text, "lxml")
    # Get HTML data from outfits page.
    outfitsRes = requests_session.get(f"https://genshin-impact.fandom.com/wiki/{query}/Outfits")
    outfitsSoup = BeautifulSoup(outfitsRes.text, "lxml")
    
    char_info_div = mainSoup.find("aside", {"role": "region"})
    char_details_div = char_info_div.find("section", {"class": "wds-tabber"})
    talent_div = mainSoup.find("table", {"class": "talent-table"})
    constellation_div = mainSoup.find("table", {"class": "constellation-table"})
    
    # Get character data.
    data["name"] = char_info_div.find("h2", {"data-source": "name"}).text.strip()
    data["title"] = char_info_div.find("h2", {"data-item-name": "secondary_title"}).text.strip()
    data["vision"] = char_info_div.find("td", {"data-source": "element"}).text.strip()
    data["weapon"] = char_info_div.find("td", {"data-source": "weapon"}).text.strip()
    
    if search("Female", char_details_div.find("a", {"title": "Model Type"}).find_parent("h3").find_next_sibling("div").text.strip()):
        data["gender"] = "Female"
    else:
        data["gender"] = "Male"
    
    if query != "Aloy":
        nation_div = char_details_div.find("div", {"data-source": "region"}).find("h3").find_next_sibling()
        data["nation"] = parse_for_first_item_string(nation_div)
        data["nation"] = data["nation"].replace(" (in-game)", "")
    else:
        data["nation"] = "Outlander"
    
    affiliations_div = char_details_div.find("div", {"data-source": "affiliation"}).find("h3").find_next_sibling()
    data["affiliation"] = parse_for_first_item_string(affiliations_div)
    data["affiliation"] = data["affiliation"].replace(" (on profile)", "")
    
    data["specialDish"] = char_details_div.find("div", {"data-source": "dish"}).find("h3").find_next_sibling().text.strip()
    data["namecard"] = char_details_div.find("div", {"data-source": "namecard"}).find("h3").find_next_sibling().text.strip()
    data["rarity"] = get_int_from_string(char_info_div.find("td", {"data-source": "quality"}).find("img").get("alt"))
    data["constellation"] = char_details_div.find("div", {"data-source": "constellation"}).find("h3").find_next_sibling().text.strip().replace(" (Story Quest Chapter)", "")
    data["birthday"] = get_birthday_from_string(char_details_div.find("div", {"data-source": "birthday"}).find("h3").find_next_sibling().text.strip())
    data["description"] = loreSoup.find_all("p", {"class": "pull-quote__text"})[1].text.strip()
    
    # Get skill talents data.
    skill_talents = []
    def get_skill_talent(title):
        skill_div = talent_div.find("a", {"title": title}).find_parent("td").find_parent("tr")
        skill_name = skill_div.find_all("td")[1].find("a").text.strip()
        
        upgrades=[]
        upgrades_div = skill_div.find_next_sibling("tr").find("div", {"data-expandtext": "▼Attribute Scaling▼"}).find("table", {"class": "wikitable"}).find("tbody")
        for tr in upgrades_div.find_all("tr")[1:]:
            try:
                name = tr.find("th").text.strip()
                value = tr.find("td").text.strip()
                
                if "%" in name:
                    name = name.replace("(%)", "").strip()
                    value = convert_to_percentage_string(value)
                
                upgrades.append({
                    "name": name,
                    "value": value
                })
            except:
                pass
        
        # Combine "Low Plunge DMG" and "High Plunge DMG" into "Low / High Plunge DMG".
        for i in range(len(upgrades)):
            if upgrades[i]["name"] == "Low Plunge DMG":
                upgrades[i]["name"] = "Low / High Plunge DMG"
                upgrades[i]["value"] = f"{upgrades[i]['value']} / {upgrades[i+1]['value']}"
                upgrades.pop(i+1)
                break
        
        skill_desc = skill_div.find_next_sibling("tr").find("td")
        for br in skill_desc.find_all("br"):
            br.replace_with("\n")
        for div in skill_desc.find_all("div"):
            div.decompose()
        skill_desc = skill_desc.text.strip()
        
        skill_talents.append({
            "name": skill_name,
            "unlock": title,
            "description": skill_desc,
            "upgrades": upgrades,
            "type": title.upper().replace(" ", "_")
        })
    
    get_skill_talent(title="Normal Attack")
    get_skill_talent(title="Elemental Skill")
    get_skill_talent(title="Elemental Burst")
    
    data["skillTalents"] = skill_talents
    
    # Get passive talents data.
    passive_talents = []
    def get_passive_talent(title, level):
        ascension_div = talent_div.find("a", {"title": title}).find_parent("td").find_parent("tr")
        ascension_name = ascension_div.find_all("td")[1].find("a").text.strip()
        ascension_desc = ascension_div.find_next_sibling("tr").find("td")
        for br in ascension_desc.find_all("br"):
            br.replace_with("\n")
        for div in ascension_desc.find_all("div"):
            div.decompose()
        ascension_desc = ascension_desc.text.strip()
        passive_talents.append({
            "name": ascension_name,
            "unlock": f"Unlocked at Ascension {level}",
            "description": ascension_desc,
            "level": level
        })
    
    util_div = talent_div.find("a", {"title": "Utility Passive"}).find_parent("td").find_parent("tr")
    util_name = util_div.find_all("td")[1].find("a").text.strip()
    util_desc = util_div.find_next_sibling("tr").find("td")
    for br in util_desc.find_all("br"):
        br.replace_with("\n")
    for div in util_desc.find_all("div", {"class": "mw-collapsible"}):
        div.decompose()
    util_desc = util_desc.text.strip()
    
    get_passive_talent("1st Ascension Passive", 1)
    get_passive_talent("4th Ascension Passive", 4)
    passive_talents.append({
        "name": util_name,
        "unlock": "Unlocked Automatically",
        "description": util_desc
    })
    
    data["passiveTalents"] = passive_talents
    
    # Get constellations data.
    constellations = []
    def get_constellations(level):
        constellations_div = constellation_div.find("tbody")
        constellation_name = constellations_div.find_all("tr")[level * 2 - 1].find_all("td")[1].find("a").text.strip()
        constellation_desc = constellations_div.find_all("tr")[level * 2].find("td")
        for br in constellation_desc.find_all("br"):
            br.replace_with("\n")
        for div in constellation_desc.find_all("div"):
            div.decompose()
        constellation_desc = constellation_desc.text.strip()
        
        constellations.append({
            "name": constellation_name,
            "unlock": f"Constellation Lv. {level}",
            "description": constellation_desc,
            "level": level
        })
    
    for i in range(1, 7):
        get_constellations(i)
    
    data["constellations"] = constellations
    
    # Misc data.
    data["vision_key"] = data["vision"].upper()
    data["weapon_type"] = data["weapon"].upper()
    
    # Get outfits data.
    outfits_div = outfitsSoup.find("span", {"id": "List_of_Character_Outfits"}).find_parent("h2").find_next_sibling("p").find_next_sibling("table").find("tbody")
    
    outfits = []
    for tr in outfits_div.find_all("tr")[1:]:
        try:
            name = tr.find_all("td")[1].find("a").text.strip()
            rarity = get_int_from_string(tr.find_all("td")[2].find("img").get("title").strip())
            outfit_type = tr.find_all("td")[3].find("a").text.strip()
            
            outfitRes = requests_session.get(f"https://genshin-impact.fandom.com/wiki/{name.replace(' ', '_')}")
            outfitSoup = BeautifulSoup(outfitRes.text, "lxml")
            
            outfit_desc_div = outfitSoup.find("aside", {"role": "region"})
            outfit_desc = outfit_desc_div.find("div", {"data-source": "description"}).find("div").text.strip()
            
            if outfit_type == "Alternate":
                price = 0
            else:
                if rarity == 5:
                    price = 2480
                elif rarity == 4:
                    price = 1680
            
            outfit_image = f"outfit-{name.replace(' ', '-').lower()}"
            
            outfits.append({
                "type": outfit_type,
                "name": name,
                "description": outfit_desc,
                "rarity": rarity,
                "price": price,
                "image": outfit_image,
            })
        except:
            pass
        
    if outfits:
        data["outfits"] = outfits
    
    return data
