from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd


def get_comments_youtube(link):
    chrome_options = Options()
    # chrome_options.add_argument('log-level=2')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--disable-infobars")
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    driver.get(link)
    comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
    # for everything to be loaded as necessary.
    driver.execute_script("arguments[0].scrollIntoView();", comment_section)
    time.sleep(7)

    # Scroll all the way down to the bottom in order to get all the
    # elements loaded (since Youtube dynamically loads them).
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Scroll down 'til "next load".
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load everything thus far.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # One last scroll just in case.
#     driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    username = driver.find_elements(By.XPATH, '//*[@id="author-text"]')
    comment_elems = driver.find_elements(By.XPATH, '//*[@id="content-text"]')
    comment_list, username_list = list(), list()
    for comment, user in zip(comment_elems, username):
        comment_list.append(comment.text)
        username_list.append(user.text)
        dict = {
            "Username": username_list,
            "Comment": comment_list
        }
        dt = pd.DataFrame(dict, columns=["Username","Comment"])
    dt.to_csv("comment_youtube.csv", index=False)
    driver.quit()
