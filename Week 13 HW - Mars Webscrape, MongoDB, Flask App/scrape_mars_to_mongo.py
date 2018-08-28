import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import pymongo
from pymongo import MongoClient
import datetime


#overall function to perform all scraping and return one dictionary with all scraped data
def scrape():
    # ### NASA Mars News
    # 
    # * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    # 
    # ```python
    # # Example:
    # news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
    # 
    # news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."
    # ```

    # ##### Get Mars News  Data by Using Selenium (so can extract all information processed by Javascript)

    def instantiate_selenium_driver():
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(r'C:\Users\micha\Google Drive\Data Science\chromedriver.exe', 
            chrome_options=chrome_options)
        return driver

    def get_soup_selenium(web_url):
        driver = instantiate_selenium_driver()

        driver.get(web_url)
        data_page = driver.page_source
        
        soup = BeautifulSoup(data_page, 'html.parser')
        driver.quit()
        return soup


    mars_news_soup2 = get_soup_selenium('https://mars.nasa.gov/news/')

    #find just latest article title and teaser text - so use find to get first item
    mars_news_title2 = mars_news_soup2.find('div', {'class': 'content_title'}).text
    print('Most Recent News Title: ', mars_news_title2)
    mars_news_descriptor2 = mars_news_soup2.find('div', {'class': 'article_teaser_body'}).text
    print('Most Recent News Descriptor: ',mars_news_descriptor2)


    # ### JPL Mars Space Images - Featured Image
    # 
    # * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    # 
    # * Make sure to find the image url to the full size `.jpg` image.
    # 
    # * Make sure to save a complete url string for this image.
    # 
    # ```python
    # # Example:
    # featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
    # ```
    # 

    driver = instantiate_selenium_driver()
    driver.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    #find and click on the full_image link of the header
    full_image_button = driver.find_element_by_id('full_image')
    full_image_button.click()

    #the picture that shows up is in a carousel of previous feature images
    #this picture is still a medium size (or large size depending on your browser,
    #but not full size).  go to 'more info' button to find details of the image
    time.sleep(1) #takes a little bit for this page to load, button won't show up if script runs instantly
    more_info_button = driver.find_element_by_link_text('more info')
    # more_info_button = driver.find_element_by_partial_link_text('info')
    more_info_button.click()

    #get soup of current more info page
    more_info_page = driver.page_source
    image_more_info_soup = BeautifulSoup(more_info_page, 'html.parser')
    driver.quit()

    #jpeg link is the second li in download_tiff class (first is download tiff if want that one)
    full_res_jpg_url = image_more_info_soup.find_all('div', {'class':'download_tiff'})                                                [1].a.attrs['href']
    full_res_jpg_url = 'https:' + full_res_jpg_url
    print('The full resolution jpg image is at: ', full_res_jpg_url)


    # ### Mars Weather
    # 
    # * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
    # 
    # ```python
    # # Example:
    # mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
    # ```
    # 

    twitter_feed_soup = get_soup_selenium('https://twitter.com/marswxreport?lang=en')

    #get all the tweet texts from the page
    #find the first one in the list that has weather info (since they post some 
    #tweets that are not a normal weather report) by selecting a text that includes
    #high, low, pressure, and daylight
    tweets_text = [tweet_paragraph.text for tweet_paragraph in
                twitter_feed_soup.find_all('p', {'class':'tweet-text'})]
    for tweet_text in tweets_text:
        if all(word in tweet_text for word in ['high', 'low', 'pressure', 'daylight']):
            latest_mars_weather = tweet_text
            break
    print('The latest weather on Mars is: ', latest_mars_weather)


    # ### Mars Facts
    # 
    # * Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # 
    # * Use Pandas to convert the data to a HTML table string.

    #mars facts page doesn't load with javascript so can directly read tables into pandas 
    #without using selenium, and only one table on the page
    df_mars_facts = pd.read_html('http://space-facts.com/mars/')[0]
    print(df_mars_facts)

    mars_facts_html_table = df_mars_facts.to_html(header=False, index=False)
    print('Html Code for Table: \n\n', mars_facts_html_table)


    # ### Mars Hemispheres
    # 
    # * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    # 
    # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # 
    # * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    # 
    # * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    # 
    # ```python
    # # Example:
    # hemisphere_image_urls = [
    #     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #     {"title": "Cerberus Hemisphere", "img_url": "..."},
    #     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    # ]
    # ```

    # ##### The USGS page doesn't load with javascript, so can just use response and beautiful soup to find href links and go to each one instead of using selenium.

    #get the soup from the main mars hemispheres page
    USGS_response = requests.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    USGS_soup = BeautifulSoup(USGS_response.text, 'html.parser')

    #find all of the relative links from the hemispheres - under a tags of class: product-item
    #and add on main url to front of https://astrogeology.usgs.gov
    USGS_hem_links = ['https://astrogeology.usgs.gov' + a['href'] for a
                        in USGS_soup.find_all('a', {'class': 'product-item'})]


    #run a for loop to go through each link from the main page to visit each hemisphere page
    #and extract required data and store in list as dictionary for each hemisphere
    hemisphere_image_urls = []
    for hem_link in USGS_hem_links:
        #get soup from hemisphere page
        hem_soup = BeautifulSoup(requests.get(hem_link).text, 'html.parser')

        #get name of hemisphere - note: all the hemisphere titles have extra string of Enhanced
        #at the end, so remove that for true title
        hem_title = hem_soup.find('h2', {'class':'title'}).text.replace(' Enhanced', '')

        #for imageurl: go to downloads div, and within that find the href that has text of Sample
        #(Original will only give a link that downloads, but we will want to show the img on our webpage)
        hem_img_url = hem_soup.find('div', {'class': 'downloads'}).find('a', text='Sample')['href']

        #append dictionary to list
        hemisphere_image_urls.append(dict([('title', hem_title), ('img_url', hem_img_url)]))

    print(hemisphere_image_urls)



    # ## Step 2a - Create Dictionary
    # 
    # - convert everything to dictionary
    # - that can be stored into MongoDB

    #collect all mars scraped data - include an _id for mongo that is the timestamp
    #of when collected all the info
    mars_scraped_data = {
        '_id': str(datetime.datetime.now()).split('.')[0],
        'mars_news': {'mars_news_title': mars_news_title2,
                    'mars_news_descripter': mars_news_descriptor2},
        'mars_img_url': full_res_jpg_url,
        'mars_weather': latest_mars_weather,
        'mars_facts_html_table': mars_facts_html_table,
        'mars_hemisphere_image_urls': hemisphere_image_urls
    }
    return mars_scraped_data


#Step 2b - overall function to send dictionary to MongoDB
def to_mongo(mars_scraped_dict):
    #setup Mongo Client for mars database and a collection called mars_data
    client = MongoClient('localhost', 27017) #local mongo client
    db = client.mars
    collection = db.mars_data

    #insert the mars news data dictionary
    collection.insert_one(mars_scraped_dict)
    print('scraped data saved to MongoDB localhost db: mars, collections: mars_data')


#what runs when run this script (won't run if just import functions)
if __name__ == '__main__':
    to_mongo(scrape())