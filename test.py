import os
from dotenv import load_dotenv
from scraper.login import Login
from scraper.scraping import Scraping


# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument('--disable-dev-shm-usage') 
# driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://x.com/")
# driver.maximize_window()


#css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3
#css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3
#css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3

load_dotenv()

login = Login(
    username=os.getenv("TWITTER_USERNAME"),
    password=os.getenv("TWITTER_PASSWORD")
)
login.do_login()
scraping = Scraping()

scraping.scrape_tweets(
    max_tweets=10,
    scrape_username="Mimese_"
)
