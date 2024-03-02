from time import sleep
import random

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc


class GVoiceChromeDriver:
    """GVoice page object model.
    """
    NAVIGATION_WAIT_TIMEOUT = 3

    def __init__(self):
        self._driver = None
        self._setup()

    def _setup(self):
        """Sets up the Selenium driver session.
        """
        options = uc.ChromeOptions()

        options.add_argument("--disable-extensions")
        options.add_argument('--disable-application-cache')
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")

        self._driver = uc.Chrome(
            options=options, driver_executable_path='/usr/local/bin/chromedriver')

    def load_cookies(self, cookies):
        """Loads the GVoice account cookies into the session.

        Args:
            cookies (List(dict)): the GVoice account cookies.
        """
        self._driver.get('https://voice.google.com/u/0/')

        for cookie in cookies:
            self._driver.add_cookie(cookie)

    def clear_cookies(self):
        """Clears all cookies.
        """
        self._driver.delete_all_cookies()

    def send_sms(self, phone_number, message):
        """Sends a new sms message to a given recipient. 

        Args:
            phone_number (str): phone number of the recipient.
            message (str): message contents to send.
        """
        self._driver.get('https://voice.google.com/u/0/messages')
        self.__send_new_message(phone_number, message)

    def __send_new_message(self, phone_number, message):
        """Sends a new message by navigating through message flow. 

        Args:
            phone_number (str): phone number of the recipient.
            message (str): message contents to send.
        """
        element_locator = (By.CSS_SELECTOR, '[gv-id="send-new-message"]')
        element = WebDriverWait(self._driver, self.NAVIGATION_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(element_locator)
        )
        element.click()

        actions = ActionChains(self._driver)
        actions.move_by_offset(0, 0).click().perform()
        element_locator = (
            By.CSS_SELECTOR, '[placeholder="Type a name or phone number"]')
        input_box = WebDriverWait(self._driver, self.NAVIGATION_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(element_locator)
        )
        input_box.send_keys(phone_number)

        element_locator = (
            By.XPATH, '//div[contains(text(), "Send to")]/following-sibling::div')
        div_element = WebDriverWait(self._driver, self.NAVIGATION_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(element_locator)
        )
        div_element.click()
        self._random_sleep()

        actions = ActionChains(self._driver)
        actions.move_by_offset(0, 0).click().perform()
        element_locator = (By.CSS_SELECTOR, '[placeholder="Type a message"]')
        input_box = WebDriverWait(self._driver, self.NAVIGATION_WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(element_locator)
        )
        input_box.send_keys(message)
        self._random_sleep()
        input_box.send_keys(Keys.ENTER)
        sleep(2)  # wait for the request to go through

    def _random_sleep(self):
        sleep(round(random.uniform(1, 1.5)))

    def close(self):
        self._driver.quit()
