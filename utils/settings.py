"""Settings for scraping.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-05-28
"""

from enum import Enum

# ---------------------------------------------------------------------------- #
#                                     ENUMS                                    #
# ---------------------------------------------------------------------------- #
class Functions(Enum):
    """Enum for functions."""
    CLEAR = "clear"
    CREATE = "create"
    LIST = "list"

class Category(Enum):
    """Enum for category."""
    ARTIFACTS = "artifacts"
    # BOSSES = "bosses"
    CHARACTERS = "characters"
    # CONSUMABLES = "consumables"
    # DOMAINS = "domains"
    ELEMENTS = "elements"
    # ENEMIES = "enemies"
    # MATERIALS = "materials"
    NATIONS = "nations"
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
