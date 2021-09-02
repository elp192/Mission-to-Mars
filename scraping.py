#!/usr/bin/env python
# coding: utf-8
# # Scrape Mars Data : News
import pandas as pd
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

def scrape_all():
    # # Set executable path , Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True) # Run headless mode: scraping is accomplished, but behind the scenes.
    
    news_title, news_paragraph = mars_news(browser)

# Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
       # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    # Visit the mars nasa news site
    #url = 'https://redplanetscience.com'
    url ='https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    # tag (div) and attribute (list_text)
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    # Set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
    # Assigned slide_elem as the variable to look for the <div /> tag
    # Reference to the class list_text
        slide_elem = news_soup.select_one('div.list_text')

        # Look inside of slide_ele information to find this specific data
        # The specific data is in a <div /> with a class of 'content_title'
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        # To get just a text
        news_title = slide_elem.find('div', class_='content_title').get_text()
    
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p



def featured_image(browser):
      # # Scrape Mars Data: Image
    #Visit URL
    #url = 'https://spaceimages-mars.com'
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Find the relative image url
    # Pulls the link to the image by get('src')
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
         return None

    # Use the base URL to create an absolute URL
    #img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url


def mars_facts():
     # Add try/except for error handling
    try:
        # Create DataFrame from HTML table, pull only the first table.
        #df = pd.read_html('https://galaxyfacts-mars.com')[0]
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
      return None
      
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    return df.to_html(classes="table table-striped")
    
# Tell flask the script is complete and ready for action
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


 # type python app.py in terminal in environmnet 