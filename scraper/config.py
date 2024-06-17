from fake_headers import Headers
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class Config:
    def do_config():
        header = Headers().generate()["User-Agent"]

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--user-agent={}".format(header))
        
        # For Hiding Browser
        chrome_options.add_argument("--headless")

        try:
            print("Iniciando ChromeDriver...")
            driver = webdriver.Chrome(
                options=chrome_options,
            )
            
            print("Configuração do WebDriver completa")
            return driver
        except WebDriverException:
            try:
                print("Baixando ChromeDriver...")
                chromedriver_path = ChromeDriverManager().install()
                chrome_service = ChromeService(executable_path=chromedriver_path)

                print("Iniciando ChromeDriver...")
                driver = webdriver.Chrome(
                    service=chrome_service,
                    options=chrome_options,
                )

                print("Configuração do WebDriver completa")
                return driver
            except Exception as e:
                return f"Erro ao configurar WebDriver: {e}"