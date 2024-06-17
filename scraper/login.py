import os
import sys
from scraper.config import Config

from time import sleep

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from dotenv import load_dotenv

class Login:
    load_dotenv()    
    
    def __init__(
        self,
        username,
        password
    ):
        self.username = username
        self.password = password
        self.driver = Config.do_config()
        
    def do_login(self):
        print()
        print("Logando no Twitter...")

        try:
            self.driver.maximize_window()
            self.driver.get(os.getenv("TWITTER_LOGIN_URL"))
            sleep(3)

            self._input_username()
            self._input_unusual_activity()
            self._input_password()

            cookies = self.driver.get_cookies()

            auth_token = None

            for cookie in cookies:
                if cookie["name"] == "auth_token":
                    auth_token = cookie["value"]
                    break

            if auth_token is None:
                return ValueError("""Pode ser devido à conexão, nome de usuário ou senha incorretos""")

            print()
            print("Login feito com sucesso")
            print()
        except Exception as e:
            print()
            print(f"Login sem êxito: {e}")
            sys.exit(1)

        pass
    
    def _input_username(self):
        input_attempt = 0

        while True:
            try:
                username = self.driver.find_element(
                    By.XPATH, "//input[@autocomplete='username']"
                )

                username.send_keys(self.username)
                username.send_keys(Keys.RETURN)
                sleep(3)
                break
            except NoSuchElementException:
                input_attempt += 1
                if input_attempt >= 3:
                    print()
                    return f"Houve um erro ao tentar se conectar que pode estar relacionado ao nome de usuário incorreto, conexão instável ou ação suspeita"
                else:
                    print("Tentando inserir usuário novamente...")
                    sleep(2)

    def _input_unusual_activity(self):
        input_attempt = 0

        while True:
            try:
                unusual_activity = self.driver.find_element(
                    By.XPATH, "//input[@data-testid='ocfEnterTextTextInput']"
                )
                unusual_activity.send_keys(self.username)
                unusual_activity.send_keys(Keys.RETURN)
                sleep(3)
                break
            except NoSuchElementException:
                input_attempt += 1
                if input_attempt >= 3:
                    break

    def _input_password(self):
        input_attempt = 0

        while True:
            try:
                password = self.driver.find_element(
                    By.XPATH, "//input[@autocomplete='current-password']"
                )

                password.send_keys(self.password)
                password.send_keys(Keys.RETURN)
                sleep(3)
                break
            except NoSuchElementException:
                input_attempt += 1
                if input_attempt >= 3:
                    print()
                    return f"Houve um erro ao tentar se conectar que pode estar relacionado à senha incorreta, conexão instável ou ação suspeita"
                else:
                    print("Tentando inserir a senha novamente...")
                    sleep(2)