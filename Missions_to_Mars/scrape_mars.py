import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape_titlepara():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
        
    html = browser.html
    soup = bs(html, 'html.parser')
    title_para = soup.find('li', class_ = 'slide')

    news_title  = title_para.find('div', class_ = 'content_title').find('a').text.strip()
    news_p  = title_para.find('div', class_='article_teaser_body').text.strip()

    browser.quit()

    news_title_p = {
        'news_title':news_title,
        'news_p':news_p
    }

    return news_title_p


def scrape_image_url():
    browser = init_browser()

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    
    html = browser.html
    soup = bs(html, 'html.parser')    
    
    header = soup.find('div', class_ = 'header')
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + header.find('img', class_ = 'headerimage')['src']
    
    browser.quit()

    return featured_image_url


def scrape_marshemi():
    browser = init_browser()

    hemisphere_image_urls = []

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    results = soup.find('div', class_ ='result-list').find_all('div', class_ = 'item')

    for result in results:
        
        title_url = {}
        browser.click_link_by_partial_text('Enhanced')
        
        html = browser.html
        soup = bs(html, "html.parser")
        
        title_url['title'] = soup.find('section', class_ = 'block metadata').find('h2', class_ = 'title').text.strip()
        title_url['img_url'] = 'https://astrogeology.usgs.gov/' + soup.find('img', class_= 'wide-image')['src']
        hemisphere_image_urls.append(title_url)

    browser.quit()
    return hemisphere_image_urls


def scrape_table():

    tables = pd.read_html('https://space-facts.com/mars/')
    facts_df= tables[0]
    facts_df.columns = ['Description','Mars'] 
    facts_df = facts_df.set_index("Description")
    facts_df = facts_df.to_html()
    
    return facts_df