"""Used for automated testing purposes.

Author: jon-chow
Created: 2023-05-19
Last Modified: 2023-06-04
"""

import pytest
import colorama
from json import load
from os import listdir, path
from colorama import Fore, Back, Style

from utils.scrapers import scrape, get_all_names


colorama.init(autoreset=True)

TESTS_DIR = "tests/data"

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def get_scrape_test_data():
    """Gathers all testing data, and returns a list of tuples of the form (category, query)."""
    tuples = []
    folders = listdir(TESTS_DIR)
    for category in folders:
        for file in listdir(path.join(TESTS_DIR, category)):
            if file.startswith("ex_"):
                query = file[3:-5]
                tuples.append((category, query))
    return tuples


# ---------------------------------------------------------------------------- #
#                                     TESTS                                    #
# ---------------------------------------------------------------------------- #
@pytest.mark.parametrize("category, expected", [
	("artifacts", ["Adventurer", "Vourukasha's Glow"]),
	("characters", ["Albedo", "Zhongli"]),
	("weapons", ["A Thousand Floating Dreams", "Waster Greatsword"]),
])
def test_get_all_names(category, expected):
	"""Tests retrieving all names for a given category."""
	print(f"{Fore.CYAN}\nTesting getting all {category} names...")
	actual = get_all_names(category)
	actual = actual[:1] + actual[-1:]
	assert actual == expected, f"{Fore.RED}Test get_all_{category}_names() failed!"


@pytest.mark.parametrize("category, query", get_scrape_test_data())
def test_scrape(category, query):
	"""Tests scraping data from category."""
	print(f"{Fore.CYAN}\nTesting {category} scraper...")
	expected = load(open(f"{TESTS_DIR}/{category}/ex_{query}.json", "r", encoding="utf-8"))
	query = query.replace("-", " ").title()
	actual = scrape(category, query)
	assert actual == expected, f"{Fore.RED}Test scrape() for {Fore.YELLOW}{query.capitalize()} {Fore.RED}failed!"
