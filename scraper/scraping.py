from scraper.progress_bar import Progress_Bar
from scraper.config import Config
from scraper.scroll import Scroll
from scraper.tweet import Tweet

from time import sleep

from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)

import json

class Scraping():
    def __init__(
            self,
            max_tweets=50,
            scrape_username=None,
            scrape_poster_details=False
        ):
        
        print("Iniciando Scraper...")
        
        self.interrupted = False
        self.tweet_ids = set()
        self.data = []
        self.tweet_cards = []
        self.scraper_details = {
            "type": None,
            "username": None,
            "tab": None,
            "poster_details": False,
        }
        self.max_tweets = max_tweets
        self.progress = Progress_Bar(0, max_tweets)
        self.driver = Config.do_config()
        self.actions = ActionChains(self.driver)
        self.scroller = Scroll(self.driver)
        self._config_scraper(
            max_tweets,
            scrape_username,
            scrape_poster_details,
        )
    
    def _config_scraper(
        self,
        max_tweets=50,
        scrape_username=None,
        scrape_poster_details=False,
    ):
        self.tweet_ids = set()
        self.data = []
        self.tweet_cards = []
        self.max_tweets = max_tweets
        self.progress = Progress_Bar(0, max_tweets)
        self.scraper_details = {
            "type": None,
            "username": scrape_username,
            "tab": "Latest",
            "poster_details": scrape_poster_details,
        }
        
        self.scroller = Scroll(self.driver)
        
        self.scraper_details["type"] = "Username"
        
    def scrape_tweets(
        self,
        max_tweets=50,
        no_tweets_limit=False,
        scrape_username=None,
        scrape_poster_details=False
    ):
        self._config_scraper(
            max_tweets,
            scrape_username,
            scrape_poster_details,
        )

        self.driver.get(f"https://twitter.com/{self.scraper_details['username']}")

        print("Scraping Tweets from @{}...".format(self.scraper_details["username"]))
        
        # Aceita os cookies pro card sumir
        try:
            accept_cookies_btn = self.driver.find_element(
            "xpath", "//span[text()='Refuse non-essential cookies']/../../..")
            accept_cookies_btn.click()
        except NoSuchElementException:
            pass

        self.progress.print_progress(0, False, 0, no_tweets_limit)

        refresh_count = 0
        added_tweets = 0
        empty_count = 0
        retry_cnt = 0

        while self.scroller.scrolling:
            try:
                self._get_tweet_cards()
                added_tweets = 0

                for card in self.tweet_cards[-15:]:
                    try:
                        tweet_id = str(card)

                        if tweet_id not in self.tweet_ids:
                            self.tweet_ids.add(tweet_id)

                            if not self.scraper_details["poster_details"]:
                                self.driver.execute_script(
                                    "arguments[0].scrollIntoView();", card
                                )

                            tweet = Tweet(
                                card=card,
                                driver=self.driver,
                                actions=self.actions,
                                scrape_poster_details=self.scraper_details[
                                    "poster_details"
                                ],
                            )

                            if tweet:
                                if not tweet.error and tweet.tweet is not None:
                                    if not tweet.is_ad:
                                        self.data.append(tweet.tweet)
                                        added_tweets += 1
                                        self.progress.print_progress(len(self.data), False, 0, no_tweets_limit)

                                        if len(self.data) >= self.max_tweets and not no_tweets_limit:
                                            self.scroller.scrolling = False
                                            break
                                    else:
                                        continue
                                else:
                                    continue
                            else:
                                continue
                        else:
                            continue
                    except NoSuchElementException:
                        continue

                if len(self.data) >= self.max_tweets and not no_tweets_limit:
                    break

                if added_tweets == 0:
                    # Verifica se existe um botão "Retry" e clica nele uma certa quantidade de tentativas
                    try:
                        while retry_cnt < 15:
                            retry_button = self.driver.find_element(
                            "xpath", "//span[text()='Retry']/../../..")
                            self.progress.print_progress(len(self.data), True, retry_cnt, no_tweets_limit)
                            sleep(58)
                            retry_button.click()
                            retry_cnt += 1
                            sleep(2)
                    # There is no Retry button so the counter is reseted
                    # Não tem botão reset então o contador é resetado
                    except NoSuchElementException:
                        retry_cnt = 0
                        self.progress.print_progress(len(self.data), False, 0, no_tweets_limit)

                    if empty_count >= 5:
                        if refresh_count >= 3:
                            print()
                            print("Sem tweets recentes")
                            break
                        refresh_count += 1
                    empty_count += 1
                    sleep(1)
                else:
                    empty_count = 0
                    refresh_count = 0
            except StaleElementReferenceException:
                sleep(2)
                continue
            except KeyboardInterrupt:
                print("\n")
                print("Busca interrompida por teclado")
                self.interrupted = True
                break
            except Exception as e:
                print("\n")
                print(f"Error scraping tweets: {e}")
                break

        print("")

        if len(self.data) >= self.max_tweets or no_tweets_limit:
            print("Scraping Finalizado")
            data = {
            "Name": [tweet[0] for tweet in self.data],
            "Handle": [tweet[1] for tweet in self.data],
            "Timestamp": [tweet[2] for tweet in self.data],
            "Verified": [tweet[3] for tweet in self.data],
            "Content": [tweet[4] for tweet in self.data],
            "Comments": [tweet[5] for tweet in self.data],
            "Retweets": [tweet[6] for tweet in self.data],
            "Likes": [tweet[7] for tweet in self.data],
            "Analytics": [tweet[8] for tweet in self.data],
            "Tags": [tweet[9] for tweet in self.data],
            "Mentions": [tweet[10] for tweet in self.data],
            "Emojis": [tweet[11] for tweet in self.data],
            "Profile Image": [tweet[12] for tweet in self.data],
            "Tweet Link": [tweet[13] for tweet in self.data],
            "Tweet ID": [f"tweet_id:{tweet[14]}" for tweet in self.data],
        }
            print(json.dumps(data, indent=4))
        else:
            print("Scraping Incompleto")

        if not no_tweets_limit:
            print("Tweets: {} de {}\n".format(len(self.data), self.max_tweets))

        pass
    
    def _get_tweet_cards(self):
        self.tweet_cards = self.driver.find_elements(
            "xpath", '//article[@data-testid="tweet" and not(@disabled)]'
        )
        pass