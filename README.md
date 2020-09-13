# Home Advisor Scraper
A quick script that will pull all Home Advisor reviews into a CSV file.

## Dependencies
- [Python3](https://www.python.org/downloads/)
- [chromedriver_py](https://pypi.org/project/chromedriver-py/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/#Download)
- [Selenium](https://selenium-python.readthedocs.io/#)
- [Requests](https://requests.readthedocs.io/en/master/)

# How to use
1. Clone repo
1. Install dependencies
1. Run command like `python3 scrape.py -u https://www.homeadvisor.com/rated.InspectorSeltzer.51920579.html -p 4` (See flags below)

## Flags
* `-u` - is the URL
* `-p` - number of pages in the pagination for the above URL