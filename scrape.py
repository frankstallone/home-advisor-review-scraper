import time
import sys
import requests
import csv
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from chromedriver_py import binary_path # this will get you the path variable

# Home Advisor URL
# Example: "https://www.homeadvisor.com/rated.InspectorSeltzer.51920579.html"
URL = ""

# Amount of pages
# Example: 4
PAGES = 0

# Checking ot make sure variables exist
if URL:
    print('\n👍🏼 URL Variable exists\n')
else:
    print('\n🚨 URL Variable requied!\n')
    sys.exit()
if PAGES != 0:
    print('\n👍🏼 PAGES Variable exists\n')
else:
    print('\n🚨 PAGES Variable requied!\n')
    sys.exit()

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
        print("🚨 Unable to find buttons to click next")
    
print("🙌🏼 Reviews saved to reviews.csv\n")