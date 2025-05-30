"""
    This file will contain the source code with
    the functionality of finding how many total
    captchas are triggered during the driver's lifetime.
"""

from utils import set_up_driver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

CAPTCHA_SELECTORS = [
    # Common CAPTCHA selectors
    'iframe[src*="recaptcha"]',
    'div[class*="recaptcha"]',
    'div[id*="recaptcha"]',
    'iframe[src*="hcaptcha"]',
    'div[class*="hcaptcha"]',
    'div[id*="hcaptcha"]',
    'div[class*="captcha"]',
    'div[id*="captcha"]',
    'img[alt*="captcha"]',
    'img[src*="captcha"]',
    # Cloudflare challenge
    'div[class*="cf-challenge"]',
    'div[id*="cf-challenge"]',
]

class CaptchaFinder:
    def __init__(self, driver):
        """
            CaptchaFinder constructor
        """
        self.driver = driver
        self.counter = 0
        self.seen_captchas = set()
        self.check_for_captcha()

    def check_for_captcha(self):
        """
            Test different captcha selectors, if
            one is found add one to the counter
        """
        for selector in CAPTCHA_SELECTORS:
            page_key = f"{self.driver.current_url}_{selector}"
            if page_key not in self.seen_captchas:
                try:
                    self.driver.find_element(By.CSS_SELECTOR, selector)
                    self.counter = self.counter + 1
                    self.seen_captchas.add(page_key)
                    break
                except NoSuchElementException:
                    continue
                except Exception as e:
                    print("Exception when checking for captcha: ", e)