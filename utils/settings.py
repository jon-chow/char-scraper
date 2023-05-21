"""Settings for scraping.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-05-20
"""

from enum import Enum

class Functions(Enum):
    """Enum for functions."""
    CLEAN = "clean"
    CREATE = "create"

class Category(Enum):
    """Enum for category."""
    ARTIFACTS = "artifacts"
    CHARACTERS = "characters"
    WEAPONS = "weapons"

# ---------------------------------------------------------------------------- #
#                                  MODIFIABLES                                 #
# ---------------------------------------------------------------------------- #

# Default data generation category.
DEFAULT_CATEGORY = Category.CHARACTERS.value

# Files and directories.
DATA_SAVE_DIR = "assets/data/"
IMG_SAVE_DIR = "assets/images/"
LANG = "en"
