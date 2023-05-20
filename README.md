# CHAR SCRAPER
## Description
This is a scraper for characters from the game "Genshin Impact". Data is scraped from [Fandom](https://genshin-impact.fandom.com/wiki/Genshin_Impact_Wiki), processed, and stored in JSON files. My intent is to add this data to the [genshin.dev API](https://github.com/genshindev/api) project.

## Prerequisites
- [Python](https://www.python.org/downloads/) ^3.11.0

## Dependencies
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [Requests](https://pypi.org/project/requests/)
- [Colorama](https://pypi.org/project/colorama/) (for coloured terminal output)

## Usage
```bash
$ python3 main.py args[]
```
The arguments are optional. If no arguments are provided, the program will scrape all characters specified in the constant FOLDERS. If arguments are provided, the program will scrape only the characters specified by the arguments. The arguments are the names of the characters, separated by spaces.

For example, to scrape only the characters `"Amber"` and `"Lisa"`, run the following command:
```bash
$ python3 main.py amber lisa
```

For characters with multi-word names, wrap their name around quotations.<br />
For example, to scrape `"Kaedehara Kazuha"` and `"Kamisato Ayaka"`, run the following command:
```bash
$ python3 main.py "kaedehara kazuha" "kamisato ayaka"
```

## License
Licensed under Open Software License v3.0
