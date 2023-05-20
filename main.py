"""Script for generating JSON character data from web scraping.

Author: jon-chow
Created: 2023-05-19
Last Modified: 2023-05-20
"""

import json
import os
import re
import requests
import sys
from bs4 import BeautifulSoup
from settings import *

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def get_int_from_string(string):
    """Extracts number from string."""
    return int("".join(filter(str.isdigit, string)))


def convert_month_to_num(month):
    """Converts month to number."""
    return {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }[month]
    

def convert_to_percentage_string(string):
    """Converts numbers to percentage string."""
    if "+" in string:
        return f"{round(float(string.split('+')[0]), 1)}% + {round(float(string.split('+')[1]), 1)}%"
    else:
        return f"{round(float(string), 1)}%"


def get_birthday_from_string(string):
    """Extracts birthday from string."""
    month = convert_month_to_num(string.split(" ")[0])
    day = string.split(" ")[1][:-2]
    # Add leading zero if day is single digit.
    if len(day) == 1:
        day = f"0{day}"
    return f"0000-{month}-{day}"


def scrape(url=URL, query=""):
    """Scrapes HTML data from given URL."""
    data = {}
    try:
        # Get HTML data from main page.
        response = requests.get(f"{URL}{query}")
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Get HTML data from lore page.
        response2 = requests.get(f"{URL}{query}/Lore")
        soup2 = BeautifulSoup(response2.content, "html.parser")
        
        char_info_div = soup.find("aside", {"role": "region"})
        char_details_div = char_info_div.find("section", {"class": "wds-tabber"})
        talent_div = soup.find("div", {"class": "talent-table-container"})
        constellation_div = soup.find("span", {"id": "Constellation"}).find_parent("h3").find_next_sibling("table", {"class": ["wikitable", 'talent-table']})
        
        # Get character data.
        data["name"] = char_info_div.find("h2", {"data-source": "name"}).text.strip()
        data["title"] = char_info_div.find("h2", {"data-item-name": "secondary_title"}).text.strip()
        data["vision"] = char_info_div.find("td", {"data-source": "element"}).text.strip()
        data["weapon"] = char_info_div.find("td", {"data-source": "weapon"}).text.strip()
        if re.search("Female", char_details_div.find("a", {"title": "Model Type"}).find_parent("h3").find_next_sibling("div").text.strip()):
            data["gender"] = "Female"
        else:
            data["gender"] = "Male"
        data["nation"] = char_details_div.find("div", {"data-source": "region"}).find("a").text.strip()
        data["affiliation"] = char_details_div.find("div", {"data-source": "affiliation"}).find("a").text.strip()
        data["specialDish"] = char_details_div.find("div", {"data-source": "dish"}).find("span", {"class": "item_text"}).text.strip()
        data["rarity"] = get_int_from_string(char_info_div.find("td", {"data-source": "quality"}).find("img").get("alt"))
        data["constellation"] = char_details_div.find("div", {"data-source": "constellation"}).find("div").find("a").text.strip()
        data["birthday"] = get_birthday_from_string(char_details_div.find("div", {"data-source": "birthday"}).find("div").find("a").text.strip())
        data["description"] = soup2.find_all("p", {"class": "pull-quote__text"})[1].text.strip().replace("\u2014", "-")
        
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
    except:
        print(f"Error: Could not scrape {URL}{query}.")
    return data


def create_json(folders=FOLDERS, file_name=LANG):
    """Generates JSON files for each folder."""
    for (folder) in folders:
        folder_dir = f"{DATA_SAVE_DIR}{folder.lower().replace(' ', '-')}"
        # Create directory if it doesn't exist.
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)
        
        # Create and store JSON data.
        with open(f"{folder_dir}/{file_name}.json", "w") as f:
            data = scrape(query=folder.title().replace(' ', '_'))
            json.dump(data, f, indent=2)


def clean_up(folders=FOLDERS):
    """Removes specified folders and its files."""
    for (folder) in folders:
        folder_dir = f"{DATA_SAVE_DIR}{folder}"
        # Remove files and directory if it exists.
        if os.path.exists(folder_dir):
            for file in os.listdir(folder_dir):
                os.remove(f"{folder_dir}/{file}")
            os.rmdir(folder_dir)

# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #
def main():
    """Main function."""
    # Get folders from command line arguments if they exist.
    if len(sys.argv) > 1:
        folders = sys.argv[1:]
        create_json(folders)
    # Otherwise, use default.
    else:
        create_json()
    
if __name__ == "__main__":
    main()
