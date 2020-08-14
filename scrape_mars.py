# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
import time
from selenium import webdriver
import pandas as pd

def scrape_hemispheres(driver):
    #Navigate and Scrape web pages to get Title and IMG URLs of Mars Hemispheres
    url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    driver.maximize_window()
    driver.get(url)
    # time.sleep(1)
    # Retrieve page with the requests module
    content = driver.page_source.encode('utf-8').strip()
    soup = bs(content,"html.parser")
    hemispheres = soup.find_all("div", class_="description")
    hemisphere_urls=[]
    for link in hemispheres:
        b =link.a['href']
        hemisphere_urls.append(f"https://astrogeology.usgs.gov/{b}")
        hemisphere_urls

    hemisphere_image_urls = []
    hemisphere_titles= []
    for each in hemisphere_urls:
        driver.get(each)
        # time.sleep(1)
        content = driver.page_source.encode('utf-8').strip()
        soup = bs(content,"html.parser")
        hemisphere_title = soup.find('h2', class_='title').text
        hemisphere_image_url = soup.find('div', class_='downloads').ul.li.a['href']
        hemisphere_titles.append(hemisphere_title)       
        hemisphere_image_urls.append(hemisphere_image_url)
    
    return hemisphere_titles,hemisphere_image_urls


def scrape_info():

    # *****Scrape news about Mars from NASA. Retrieve title and summary*****
    driver = webdriver.Chrome()
    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"
    driver.maximize_window()
    driver.get(url)
    # time.sleep(1)
    # Retrieve page with the requests module
    content = driver.page_source.encode('utf-8').strip()
    soup = bs(content,"html.parser")
    results = soup.find('div', class_="image_and_description_container")
    # Error handling
    try:
        news_title = results.find('div', class_='content_title').a.text
        news_p = results.find('div', class_='article_teaser_body').text

    except AttributeError as e:
        news_title=None
        news_p = None

    print(news_title)
    print(news_p)

    #***** Scrape IMG URL of Mars*****
    # URL of page to be scraped
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    driver.maximize_window()
    driver.get(url)
    # time.sleep(1)
    # Retrieve page with the requests module
    content = driver.page_source.encode('utf-8').strip()
    soup = bs(content,"html.parser")
    img_url=soup.find('div', class_='carousel_items').article['style'].split("'")[1]
    img_url = f"https://www.jpl.nasa.gov{img_url}"
    print(img_url)

    #***** Scrape Mars Weather conditions from Twitter Feed*****
    # URL of page to be scraped
    url = "https://twitter.com/marswxreport?lang=en"
    driver.maximize_window()
    driver.get(url)
    time.sleep(1)
    # Retrieve page with the requests module
    content = driver.page_source.encode('utf-8').strip()
    soup = bs(content,"html.parser")
    mars_weather= soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').span.text.split('InSight ')[1]
    print(mars_weather)

    #***** Scrape information about Mars Planet Profile*****

    url = "https://space-facts.com/mars/"
    mars_info=pd.read_html(url)[0]
    mars_info = mars_info.to_html(classes="table")


    a,b = scrape_hemispheres(driver)

    #store in dicitonary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "img_url": img_url,
        "mars_weather": mars_weather,
        "mars_info": mars_info,
        "hemisphere_titles": a,
        "hemisphere_image_urls": b
    }

    return mars_data
