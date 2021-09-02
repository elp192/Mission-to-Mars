#!/usr/bin/env python
# coding: utf-8
# # Scrape Mars Data : News
import pandas as pd
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Set your executable path 
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
# tag (div) and attribute (list_text)
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
# Assigned slide_elem as the variable to look for the <div /> tag
# Reference to the class list_text
slide_elem = news_soup.select_one('div.list_text')

# Look inside of slide_ele information to find this specific data
# The specific data is in a <div /> with a class of 'content_title'
slide_elem.find('div', class_='content_title')

# To get just a text
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# # Scrape Mars Data: Image
#Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
# Pulls the link to the image by get('src')

img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# https://galaxyfacts-mars.com/;

# Create DataFrame from HTML table, pull only the first table.
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df.to_html()

browser.quit()
