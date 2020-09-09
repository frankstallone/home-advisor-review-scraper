#! /usr/local/bin/python3
import csv
import sys
import time
import argparse
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from chromedriver_py import binary_path # this will get you the path variable


class ErrorCodes(object):
    unable_to_identify_button = 10


def argument_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Given a HomeAdvisor URL, scrapes the page for associated reviews"
                    "\nExample: https://www.homeadvisor.com/rated.InspectorSeltzer.51920579.html"
    )
    parser.add_argument(
        '-u', '--url', dest='url', action='store', required=True,
        help="A target HomeAdvisor URL to scan for data"
    )
    parser.add_argument(
        '-p', '--pages', dest='pages', action='store', type=int, required=True,
        help='Number of pages of review to scan'
    )
    return parser.parse_args()

def main():

# webdriver options
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')

# initialize webdriver
    driver = webdriver.Chrome(executable_path=binary_path, options=options)
    driver.get(URL)

# initialize csv
    outfile = open('reviews.csv', 'w', newline='')
    writer = csv.writer(outfile)
    writer.writerow(["author", "rating", "date", "review"])

    for x in range(PAGES): 
        # Wait 4 seconds for the DOM to update
        time.sleep(4)
        # Grab new DOM
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Each user review
        reviews_selector = soup.find_all('div', class_='profile-user-review')
        for review_selector in reviews_selector:

            # Grab all data
            author = review_selector.find('span', attrs={'itemprop': 'author'}).get_text()
            rating = review_selector.find('span', attrs={'itemprop': 'reviewRating'}).get_text()
            date = review_selector.find('span', attrs={'itemprop': 'datePublished'}).get_text()
            review = review_selector.find('span', attrs={'itemprop': 'reviewBody'}).get_text()
            
            # Clean whitespace
            author = ''.join(content.strip() for content in author.split('/n'))
            rating = ''.join(content.strip() for content in rating.split('/n'))
            date = ''.join(content.strip() for content in date.split('/n'))
            review = BeautifulSoup(''.join(content.strip() for content in review.split('/n')), 'html.parser' )

            # Save all data
            writer.writerow([author, rating, date, review])
        print("✅ Page " + str(x+1) + "'s Page reviews saved\n")
        try:
            # Find next button on reviews
            nextButton = driver.find_element_by_class_name("next")
            # Click next button
            nextButton.click()
            print("🖱 Mouse click to next review page\n")
        except Exception as error:
            print(error)
            print("🚨 Unable to find buttons to click next")
            sys.exit(errorCodes.unable_to_identify_button)
        
    print("🙌🏼 Reviews saved to reviews.csv\n")


if __name__ == "__main__":
    args = argument_parser()
# Home Advisor URL
# Example: "https://www.homeadvisor.com/rated.InspectorSeltzer.51920579.html"
    URL = args.url

# Number of pages or reviews to parse
    PAGES = args.pages

    main()
