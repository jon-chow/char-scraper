# CHAR SCRAPER
## Description
This is a scraper for characters from the game "Genshin Impact". Data is scraped from [Fandom](https://genshin-impact.fandom.com/wiki/Genshin_Impact_Wiki), processed, and stored in JSON files. My intent is to add this data to the [genshin.dev API](https://github.com/genshindev/api) project.

## Prerequisites
- [Python](https://www.python.org/downloads/) ^3.11.0
- [Make](https://www.gnu.org/software/make/) (optional)

## Dependencies
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [Requests](https://pypi.org/project/requests/)
- [Colorama](https://pypi.org/project/colorama/) (for coloured terminal output)

## Usage
```bash
$ python3 main.py create mode args[]
```

```bash
$ make create mode args[]
```
The `mode` argument specifies the category of items. They can be one of the following:
- `characters`
- `weapons`
- `artifacts`

Adding `args[]` is optional. If no `args[]` are provided, the program will scrape all items of the mode. If `args[]` are provided, the program will scrape only the items specified by the `args[]`. The `args[]` are the names of the items, separated by spaces.

Example use for scraping the characters `"Amber"` and `"Lisa"`, run the following command:

#### With Python:
```bash
$ python3 main.py create characters amber lisa
```

#### With Make:
```bash
$ make create characters amber lisa
```

For characters with multi-word names, wrap their name around quotations (Python) or use hyphens (Make). For example, to scrape `"Kaedehara Kazuha"` and `"Kamisato Ayaka"`, run the following command:

#### With Python:
```bash
$ python3 main.py create characters "kaedehara kazuha" "kamisato ayaka"
```

#### With Make:
```bash
$ make create characters kaedehara-kazuha kamisato-ayaka
```

## License
Licensed under Open Software License v3.0
