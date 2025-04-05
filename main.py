import requests
from bs4 import BeautifulSoup

GOOGLE_SHEET_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSdeaaFgov7Cr6afQlBBx05VkccHSAqBTpCu18fx8_zkwpVgVw/viewform?usp=header'
ZILLOW_CLONE_URL = 'https://appbrewery.github.io/Zillow-Clone/'

response = requests.get(ZILLOW_CLONE_URL)
webpage = response.text
soup = BeautifulSoup(webpage, features="html.parser")

addresses = [address.text.strip() for address in soup.find_all("address")]
prices = [price.text.split('/')[0].split("+")[0] for price in soup.find_all("span", class_="PropertyCardWrapper__StyledPriceLine")]
links = [a["href"] for a in soup.css.select("article div div div a")]
