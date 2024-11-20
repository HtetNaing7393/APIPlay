from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

import json
import os
import execjs

import requests

# Global variables to store global data
api_links = []
endpoints = 0

# Setup webdriver and chrome optioins
options = webdriver.ChromeOptions()
options.add_argument("--headless")

# Start the chrome driver
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

actions = ActionChains(driver)

# Test opening js file
# js_file_path = os.path.join(os.path.dirname(__file__), "..", "js", "get_data.js")
js_file_path = 'C:\\Users\\htetk\\OneDrive\\Desktop\\Python\\APIPlay\\static\\js\\get_data.js'
with open(js_file_path, "r") as file:
    js_code = file.read()
context = execjs.compile(js_code)

def get_api_data(url):
    # The list that houses the api links
    # Navigate to the clickable links in the web-page
    url = f"{url}"
    driver.get(url)

    table = driver.find_element(By.TAG_NAME, "table")
    table_body = table.find_element(By.TAG_NAME, "tbody")
    table_row = table_body.find_elements(By.TAG_NAME, "tr")

    for r in table_row:
        link = r.find_element(By.TAG_NAME, "a")
        href = link.get_attribute("href")
        api_links.append(href)  # store the link in the api_endpoints array
        break
    driver.quit()


def scrape_page(link):
    driver.get(link)
    code = driver.find_element(By.TAG_NAME, "code")
    print(code.text)
    

# def scrape_page():
#     for link in api_links:
#         l = f"{link}"
#         # print(l)
#         result = context.call("get_api_endpoints", l)
#         print(type(result))


    

        
    
# get_api_data("https://developers.google.com/apis-explorer")
# scrape_page("https://developers.google.com/abusive-experience-report/v1/reference/rest")
