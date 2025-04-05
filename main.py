import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

ZILLOW_CLONE_URL = 'https://appbrewery.github.io/Zillow-Clone/'
GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSdeaaFgov7Cr6afQlBBx05VkccHSAqBTpCu18fx8_zkwpVgVw/viewform?usp=header'
GOOGLE_SHEET_URL = 'https://docs.google.com/spreadsheets/d/1r8uKQmzjAqTDYodYefOiKWX_PMWgwvYQ7YaVpUAXcNo/edit?usp=sharing'

# Using bs4, scrape website for info from the listings
response = requests.get(ZILLOW_CLONE_URL)
webpage = response.text
soup = BeautifulSoup(webpage, features="html.parser")

addresses = [address.text.strip() for address in soup.find_all("address")]
prices = [price.text.split('/')[0].split("+")[0] for price in soup.find_all("span", class_="PropertyCardWrapper__StyledPriceLine")]
links = [a["href"] for a in soup.css.select("article div div div a")]


# Using Selenium, input the entries into the Google Form.
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get(GOOGLE_FORM_URL)

for i in range(len(addresses)):
    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    sleep(1)
    address_input.send_keys(addresses[i])
    price_input.send_keys(prices[i])
    link_input.send_keys(links[i])

    sleep(1)
    submit_button.click()

    if i != len(addresses):
        sleep(1)
        submit_again_link = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        submit_again_link.click()

driver.switch_to.new_window('tab')
driver.get(GOOGLE_SHEET_URL)
