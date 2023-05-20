"""Used for automated testing purposes.

Author: jon-chow
Created: 2023-05-19
Last Modified: 2023-05-19
"""

import json
from main import scrape, create_json, clean_up

TEST_DATA = json.load(open("test_data.json", "r"))

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def test_scrape():
  """Tests data scraping"""
  expected = TEST_DATA
  actual = scrape()
  assert (actual == expected), "Scraping failed."



# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #
def test():
  test_scrape()

if __name__ == "__main__":
  test()
  print("Everything passed")
