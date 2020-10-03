#!/usr/bin/env python
# coding: utf-8

# In[24]:


from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser


# In[27]:


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html



# In[30]:

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)



#URL To be scraped
def scrape():
    browser = init_browser()

    mars_news_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_news_url)
    mars_html = browser.html
    mars_news_soup = BeautifulSoup(mars_html, 'html.parser')
    news_title = mars_news_soup.find_all('div', class_='content_title')[1].text
    news_p = mars_news_soup.find_all('div', class_='article_teaser_body')[1].text

    
    
    #URL To be scraped
    jpls_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpls_url)
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')
    featured_image = jpl_soup.find_all('a', class_="button fancybox")
    pic_src = []
    for image in featured_image:
        pic_url = image['data-fancybox-href']
        pic_src.append(pic_url)
    featured_image_url = 'https://www.jpl.nasa.gov' + pic_url
    
    
    #URL To be scraped
    mars_facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(mars_facts_url)
    df = table[0]
    df.columns = ["Facts", "Value"]
    df.set_index(["Facts"])
    facts_h = df.to_html()
    facts_h = facts_h.replace('\n','')
    
    #hemisphere did not return anythign see the screenshot in file
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url":featured_image_url,
        "fact_table":facts_h
    }
    
    browser.quit()


    return mars_dict
