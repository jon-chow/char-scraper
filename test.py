"""Used for automated testing purposes.

Author: jon-chow
Created: 2023-05-19
Last Modified: 2023-05-19
"""

import json
import colorama
from colorama import Fore, Back, Style
from main import scrape

colorama.init(autoreset=True)

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def test_scrape():
  """Tests data scraping"""
  query = "potato"
  expected = json.load(open("test_data.json", "r"))
  actual = scrape(query=query)
  assert (actual == expected), f"{Fore.RED}Test scraping for '{query}' failed!"

# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #
def test():
  test_scrape()

if __name__ == "__main__":
  test()
  print(f"{Fore.GREEN}All tests passed!")
