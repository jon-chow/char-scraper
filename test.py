"""Used for automated testing purposes.

Author: jon-chow
Created: 2023-05-19
Last Modified: 2023-05-19
"""

import json
import os
import colorama
from colorama import Fore, Back, Style

from utils.scraper import scrape

from utils.scrapers.names.characters import get_all_character_names


colorama.init(autoreset=True)

TESTS_DIR = "tests"

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def test_get_all_character_names():
  """Tests retrieving all character names (checks for only the first and last characters)."""
  expected = ["albedo", "zhongli"]
  actual = get_all_character_names()
  actual = actual[:1] + actual[-1:]
  try:
    assert (actual == expected)
    print(f"{Fore.GREEN}Test get_all_character_names() passed!")
    return True
  except AssertionError as e:
    print(f"{Fore.RED}Test get_all_character_names() failed!")
    return False


def test_scrape(query="amber"):
  """Tests data scraping."""
  expected = json.load(open(f"{TESTS_DIR}/ex_{query}.json", "r"))
  actual = scrape(query=query)
  try:
    assert (actual == expected)
    print(f"{Fore.GREEN}Test scraping for {Fore.YELLOW}{query.capitalize()} {Fore.GREEN}passed!")
    return True
  except AssertionError as e:
    # print(f"{Fore.CYAN}{json.dumps(actual, indent=2)}")
    print(f"{Fore.RED}Test scraping for {Fore.YELLOW}{query.capitalize()} {Fore.RED}failed!")
    return False

# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #
def test():
  """Main function for testing."""
  progress = { "passes": 0, "fails": 0 }
  
  def passed():
    """Increments the number of passed tests."""
    progress['passes'] += 1

  def failed():
    """Increments the number of failed tests."""
    progress['fails'] += 1
  
  # Testing: test_get_all_character_names().
  print(f"{Fore.CYAN}\nTesting get_all_character_names()...")
  if test_get_all_character_names():
    passed()
  else:
    failed()
  
  # Testing: test_scrape().
  print(f"{Fore.CYAN}\nTesting test_scrape()...")
  files = os.listdir(TESTS_DIR)
  for file in files:
    if file.startswith("ex_"):
      query = file[3:-5]
      if test_scrape(query=query):
        passed()
      else:
        failed()
  
  return progress

if __name__ == "__main__":
  results = test()
  if results['fails'] == 0:
    print(f"{Fore.CYAN}\nSUMMARY: All tests passed!")
  else:
    print(f"{Fore.CYAN}\nSUMMARY: {results['passes']} / {results['passes'] + results['fails']} tests passed!")
