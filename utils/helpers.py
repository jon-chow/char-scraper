"""Module for helper functions.

Author: jon-chow
Created: 2023-05-20
Last Modified: 2023-06-05
"""

import colorama
from colorama import Fore, Back, Style
from math import ceil, floor, log10
from pynput.keyboard import Key, KeyCode, Listener


colorama.init(autoreset=True)

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def get_int_from_string(string):
    """Extracts number from string."""
    return int("".join(filter(str.isdigit, string)))


def title_case(string):
    """
    Converts string to title case, ignoring prepositions.
    Capitalizes hyphenated words i.e. "freedom-sworn" -> "Freedom-Sworn".
    Capitalizes words in parentheses i.e. "prized isshin blade (awakened)" -> "Prized Isshin Blade (Awakened)".
    Ignores capitalization of prepositions.
    """
    prepositions = {"a", "an", "the", "at", "by", "for", "in", "of", "on", "to", "up", "and", "as", "but", "it", "or", "nor"}
    words = string.split(" ")
    capitalized_words = []

    for word in words:
        if "-" in word:
            word = "-".join([w.capitalize() for w in word.split("-")])
        elif "(" in word:
            word = "(".join([w.capitalize() for w in word.split("(")])
        elif word not in prepositions:
            word = word.capitalize()
        capitalized_words.append(word)
    return " ".join(capitalized_words)


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
    return f"{round(float(string.split('+')[0]), 1)}% + {round(float(string.split('+')[1]), 1)}%" if "+" in string else f"{round(float(string), 1)}%"


def get_birthday_from_string(string):
    """Extracts birthday from string."""
    month = convert_month_to_num(string.split(" ")[0])
    day = string.split(" ")[1][:-2]
    return f"0000-{month}-0{day}" if len(day) == 1 else f"0000-{month}-{day}"


def parse_for_first_item_string(element):
    """Parses an element to get the first string."""
    return element.find_all("li")[0].text.strip() if element.find("ul") else element.text.strip()


def paginate_output(lines, max_items):
    """Paginates outputs to the terminal."""
    total_lines = len(lines)
    total_pages = ceil(total_lines / max_items)
    current_page = 1
    
    def print_items():
        """Prints items."""
        nonlocal current_page, total_pages, total_lines
        start = (current_page - 1) * max_items
        end = start + max_items
        page_lines = lines[start:end]
        LEADING_ZEROS = floor(log10(total_lines)) + 1
        
        # Clear and print page.
        print("\033c", end="")
        print(f"{Fore.YELLOW}Page {current_page} / {total_pages} ({total_lines} total items)")
        for line in page_lines:
            print(f"{Fore.CYAN}{str(lines.index(line) + 1).zfill(LEADING_ZEROS)}. {line}")
            
        # Add padding if there are less than max_items.
        if len(page_lines) < max_items:
            for i in range(max_items - len(page_lines)):
                print()
        
        # Add instructions.
        print(f"{Fore.YELLOW}Next: {Fore.GREEN}RIGHT, 'd'{Fore.YELLOW} | Prev: {Fore.GREEN}LEFT, 'a'{Fore.YELLOW} | Quit: {Fore.GREEN}ESC, 'q'{Fore.YELLOW}")

    def on_press(key):
        """Handles key presses."""
        nonlocal current_page, total_pages
        if key == Key.esc or key == KeyCode.from_char("q") or key == Key.enter:
            print("\033c", end="")
            return False
        elif (key == Key.right or key == KeyCode.from_char("d")) and current_page < total_pages:
            current_page += 1
            print_items()
        elif (key == Key.left or key == KeyCode.from_char("a")) and current_page > 1:
            current_page -= 1
            print_items()

    # Print the first page and start listening for key presses.
    print_items()
    with Listener(on_press=on_press, suppress=True) as listener:
        listener.join()

