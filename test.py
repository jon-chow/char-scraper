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

colorama.init(autoreset=True)

TESTS_DIR = "tests"

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
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
  files = os.listdir(TESTS_DIR)
  for file in files:
    if file.startswith("ex_"):
      query = file[3:-5]
      if test_scrape(query=query):
        progress['passes'] += 1
      else:
        progress['fails'] += 1
  return progress

if __name__ == "__main__":
  results = test()
  if results['fails'] == 0:
    print(f"{Fore.CYAN}SUMMARY: All tests passed!")
  else:
    print(f"{Fore.CYAN}SUMMARY: {results['passes']} / {results['passes'] + results['fails']} tests passed!")
