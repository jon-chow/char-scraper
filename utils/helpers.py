"""Module for helper functions.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-05-20
"""

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


def parse_for_first_item_string(element):
    """Parses an element to get the first string."""
    if element.find("ul"):
        return element.find_all("li")[0].text.strip()
    elif element.find("a"):
        return element.text.strip()
    else:
        return element.text.strip()
