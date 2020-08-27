import time
import requests
import csv
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from chromedriver_py import binary_path # this will get you the path variable

# webdriver options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
# instantiate webdriver
driver = webdriver.Chrome(executable_path=binary_path, options=options)
driver.get("https://www.homeadvisor.com/rated.InspectorSeltzer.51920579.html")
# instantiate csv
outfile = open('reviews.csv', 'w', newline='')
writer = csv.writer(outfile)
writer.writerow(["author", "rating", "date", "review"])

# Empty array for reviews
reviews = []

for x in range(4): 
    # Wait 4 seconds for the DOM to update
    time.sleep(4)
    # Grab new DOM
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Each user review
    reviews_selector = soup.find_all('div', class_='profile-user-review')
    for review_selector in reviews_selector:

        # Grab all data
        test = review_selector.find('div', class_='profile-user-review-body').find('div', class_='t-heavy').get_text()
        # for string in test.strings:
        #     print(repr(string))
        test2 = test.replace("\n", "")
        test3 = ''.join(content.strip() for content in test2.split('/n'))
        print(test3)
        # author = review_selector.find('span', attrs={'itemprop': 'author'}).get_text()
        # rating = review_selector.find('span', attrs={'itemprop': 'reviewRating'}).get_text()
        # date = review_selector.find('span', attrs={'itemprop': 'datePublished'}).get_text()
        # review = review_selector.find('span', attrs={'itemprop': 'reviewBody'}).get_text()
        
        # # Clean whitespace
        # author = ''.join(content.strip() for content in author.split('/n'))
        # rating = ''.join(content.strip() for content in rating.split('/n'))
        # date = ''.join(content.strip() for content in date.split('/n'))
        # review = ''.join(content.strip() for content in review.split('/n'))

        # # Save all data
        # reviews.append(author)
        # reviews.append(rating)
        # print(author)
    print("For completed")
    try:
        # This only grabs the first pages profiles
        # reviews_selector = soup.find_all('span', class_='reviewBody')
        # print(reviews_selector)
        nextButton = driver.find_element_by_class_name("next")
        nextButton.click()
        print("Completed click")
    except Exception: break
    
# print(reviews)