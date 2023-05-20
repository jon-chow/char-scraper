"""Used for automated testing purposes.

Author: jon-chow
Created: 2023-05-19
Last Modified: 2023-05-19
"""

import json
import os
import colorama
from colorama import Fore, Back, Style
from main import scrape

colorama.init(autoreset=True)

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def test_scrape(query="amber"):
  """Tests data scraping"""
  expected = json.load(open(f"tests/ex_{query}.json", "r"))
  actual = scrape(query=query)
  print(f"{Fore.CYAN}{json.dumps(actual, indent=2)}")
  try:
    assert (actual == expected)
  except AssertionError as e:
    print(f"{Fore.RED}Test scraping for {Fore.YELLOW}{query.capitalize()} {Fore.RED}failed!")

# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #
def test():
  # Read all names of files in tests folder.
  files = os.listdir("tests")
  for file in files:
    if file.startswith("ex_"):
      query = file[3:-5]
      test_scrape(query=query)

if __name__ == "__main__":
  test()
  print(f"{Fore.GREEN}All tests passed!")
