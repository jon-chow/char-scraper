"""Settings for scraping.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-05-20
"""


from enum import Enum


class Mode(Enum):
    """Enum for mode."""
    CHARACTERS = "characters"

# ---------------------------------------------------------------------------- #
#                                  MODIFIABLES                                 #
# ---------------------------------------------------------------------------- #

# Default data generation mode.
DEFAULT_MODE = Mode.CHARACTERS.value

# URL for scraping.
URL = "https://genshin-impact.fandom.com/wiki/"

# Files and directories.
DATA_SAVE_DIR = "assets/data/"
IMG_SAVE_DIR = "assets/images/"
FOLDERS = ["amber", "kaeya", "lisa"]
LANG = "en"
