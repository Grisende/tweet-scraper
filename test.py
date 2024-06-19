import os
from dotenv import load_dotenv
from scraper.login import Login
from scraper.scraping import Scraping

load_dotenv()

login = Login(
    username=os.getenv("TWITTER_USERNAME"),
    password=os.getenv("TWITTER_PASSWORD")
)
login.do_login()
scraping = Scraping()

scraping.scrape_tweets(
    max_tweets=10,
    scrape_username="pobredasofertas"
)
