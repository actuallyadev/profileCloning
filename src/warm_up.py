"""
    This file focuses on warming up already created profiles, or (in the future)
    profiles that the user provides.

    Allowing the user to assign a specific proxy/IP to a browser profile or to
    each browser profile could be something valuable as well.

    We will be using undectected-chromedriver for this as it works much better
    and emulates a human much better than vanilla Selenium.

    This matters since we do not want the reputation stored in our profiles to be
    bot-like.

    A good idea could be showing how many captchas pop up in a website like
    Twitter without warm-up compared to with warm-up.

    Another good idea is showing the CreepJs metrics before warmup and after
    warmup
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from captcha_finder import CaptchaFinder
from get_creepjs_output import get_creepjs_metrics
from utils import set_up_driver, ExceptionCounter
import time
import string
import random
from pathlib import Path
import pandas as pd

TOP_WEBSITES = [
    'google.com', 'youtube.com', 'facebook.com', 'instagram.com', 'chatgpt.com',
    'x.com', 'whatsapp.com', 'reddit.com', 'yahoo.com', 'tiktok.com',
    'amazon.com', 'baidu.com', 'microsoftonline.com', 'linkedin.com', 'pornhub.com',
    'netflix.com', 'naver.com', 'live.com', 'office.com', 'bing.com',
    'temu.com', 'pinterest.com', 'bilibili.com', 'xvideos.com', 'microsoft.com',
    'xhamster.com', 'vk.com', 'sharepoint.com', 'fandom.com', 'globo.com',
    'canva.com', 'weather.com', 'samsung.com', 'duckduckgo.com', 'openai.com',
    'xnxx.com', 'nytimes.com', 'stripchat.com', 'aliexpress.com', 'roblox.com'
]

COOKIE_ACCEPT_TERMS = [
    # English
    'accept', 'allow', 'agree', 'ok', 'got', 'consent',
    # Spanish  
    'acept', 'permit', 'consen',
    # French
    'accepte', 'autoris',
    # German
    'akzeptieren', 'einvers',
    # Portuguese
    'aceit',
    # Italian
    'accett', 'accett'
]

LOG_IN_AND_REGISTER_STEMS = [
    # English
    "log", "sign", "reg", "join",

    # Spanish / Portuguese
    "inic",   # iniciar sesión / iniciar
    "acced",  # acceder
    "regis",  # registrarse / registrar
    "cuent",  # cuenta / conta

    # French
    "conn",   # connexion / se connecter
    "inscr",  # s’inscrire

    # German / Dutch
    "anmeld", "einlog",  # anmelden / einloggen
    "account", "registr", "konto",

    # Italian
    "acced", "registr", "crea",

    # Russian
    "войд", "лог", "зарег", "аккаун",

    # Chinese
    "登录", "注册", "帳戶", "账户",

    # Japanese
    "ログ", "サイン", "登録",

    # Korean
    "로그", "회원", "계정",
]

METRICS_DATAFRAME = Path("warm_metrics.csv")

def how_many_profiles():
    """
        Ask the user how many/which profiles he wants
        to warm-up.
    """
    try:
        return int(input("How many profiles do you want to warmup?\n"))
    except Exception as e:
        raise SystemExit("Not an integer, try again\n")
    
def how_much_time():
    """
        Ask the user how many/which profiles he wants
        to warm-up.
    """
    try:
        #TODO
        return int(input("Specify the time in minutes that each profile should warm-up\n"))
    except Exception as e:
        raise SystemExit("Not an integer, try again\n")

def how_many_actions():
    """
        Ask the user how many actions should
        be executed per site, that value will
        be used as the lower threshold, that
        value + 25 will be the upper threshold.
    """
    try:
        return int(input("Specify the lower threshold of actions executed per site\n"))
    except Exception as e:
        raise SystemExit("Not an integer, try again\n")

def how_much_sleep():
    """
        Ask the user how much time
        should be slept between actions,
        this value will be used as the
        lower threshold, that value + 0.5
        will be the upper threshold.
    """
    try:
        return float(input("Specify the lower threshold of sleep per action\n"))
    except Exception as e:
        raise SystemExit("Not an integer, try again\n")

def accept_cookies(driver):
    """
        Search for elements containing
        the term 'cookie' or 'accept' and
        accept them.
    """
    # Before anything
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    except Exception as e:
        print("Body is not found in 3 seconds:", e)
    attributes = ['text()', '@aria-label', '@alt']
    for possibility in COOKIE_ACCEPT_TERMS:
        for attribute in attributes:
            try:
                # Case-insensitive version
                driver.find_element(By.XPATH, f'//*[contains(translate({attribute}, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{possibility}")]').click()
                print("FUCK YEAH GOT THEM SWEET COOKIES")
                return
            except NoSuchElementException:
                try:
                    # Scroll into view first
                    driver.execute_script("window.scrollTo(0, 100)")
                    driver.find_element(By.XPATH, f'//*[contains(translate({attribute}, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{possibility}")]').click()
                except NoSuchElementException:
                    # Scroll until the bottom
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    driver.find_element(By.XPATH, f'//*[contains(translate({attribute}, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{possibility}")]').click()
            except Exception as e:
                print("Exception in accept_cookies:", e)

def get_random_websites():
    """
        Using the random module and the choices function
        we can easily get k random websites in one line
    """
    return random.choices(TOP_WEBSITES, k=7)

def get_random_input():
    """
        Return a random string
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(9, 16)))

def find_element(driver, random_letter):
    """
        Helper function to simplify act_like_a_human_logic
    """
    try:
        return driver.find_element(By.XPATH, f'//*[contains(text(), "{random_letter}")]')
    except Exception as e:
        print("Error: ", e)

def interact_with_element(element, counter, driver):
    """
        Interact with the element:
        Click it, if it is not clickable
        try to write something, if that fails
        try something else
    """
    if element.tag_name == "a" or element.tag_name == "button":
        try:
            element.click()
        except ElementNotInteractableException:
            try:
                driver.execute_script("arguments[0].click()", element)
            except ElementClickInterceptedException:
                counter.intercepted += 1        
        except ElementClickInterceptedException:
            try:
                driver.execute_script("arguments[0].click()", element)
            except ElementClickInterceptedException:
                counter.intercepted += 1
        except Exception as e:
            print("Exception at interact_with_element: ", e)
    elif element.tag_name == "input":
        try:
            element.send_keys(get_random_input())
            element.send_keys(Keys.ENTER)
        except Exception as e:
            print("Exception at interact_with_element: ", e)
    else:
        pass

def scroll_randomly(driver):
    """
        Scroll a random value
    """
    random_scroll_value = random.randint(100, 700) * random.choice((1, -1))
    for _ in range(random.randint(1, 4)):
        driver.execute_script(f"window.scrollBy(0, {random_scroll_value // 3})")
        time.sleep(random.uniform(0.2, 0.6))

def is_not_log_in_or_register_stem(element_text):
    """
        Check that the button text is not a
        log in or register stem
    """
    return element_text.lower() not in LOG_IN_AND_REGISTER_STEMS

def get_random_element(driver):
    """
        Return a random button or...
    """
    possible_tags = ['button', 'input', 'a']
    random.shuffle(possible_tags)
    for tag in possible_tags:
        elements = driver.find_elements(By.TAG_NAME, tag)
        visible_elements = [
            e for e in elements 
            if e.is_displayed()
            and (
                e.size['height'] > 5
                or e.size['width'] > 5
            ) and is_not_log_in_or_register_stem(e.text)
        ]
        try:
            return random.choice(visible_elements)
        except Exception as e:
            print("Exception at get_random_element: ", e)

def interact_with_random_element(driver, counter):
    """
       Search for a random element, every 5 seconds
       check for a captcha by creating a CaptchaFinder
       object
    """
    element = get_random_element(driver)
    if element:
        interact_with_element(element, counter, driver)

def act_like_a_human(driver, website, deadline, finder, actions_per_site, sleep, elements_over_scrolling=False):
    """
        Scroll, click a few buttons, read the text,
        think a bit, try to emulate real user behaviour
        just enough to get proper cookies and gain
        reputation.
    """
    counter = ExceptionCounter()
    possible_functions = []
    if elements_over_scrolling:
        possible_functions = [scroll_randomly] * 2 + [interact_with_random_element] * 3
    else:
        possible_functions = [scroll_randomly] * 4 + [interact_with_random_element]
    try:
        # Without https:// it was not working
        driver.get(f"https://{website}")
        print("Just went to ", website)
        time.sleep(random.uniform(0.7, 1.3))
        finder.check_for_captcha()
        time.sleep(random.uniform(0.7, 1.3))
        accept_cookies(driver)
    except Exception as e:
        print("Importante: ", e)
    for i in range(0, random.randint(actions_per_site, actions_per_site + 25)):
        if time.time() > deadline:
            break
        function = random.choice(possible_functions)
        if function.__name__ == "scroll_randomly":
            function(driver)
        else:
            function(driver, counter)
        if i % 20 == 0:
            finder.check_for_captcha()
        if i % 15 == 0:
            # User is thinking
            time.sleep(random.uniform(3.5, 6.5))
        # Between actions we need to wait a bit
        # Comment it out since we want 0 sleep for the test
        # time.sleep(random.uniform(sleep, sleep + 0.5))
    print(f"{website} STATS:")
    print("INTERCEPTED ELEMENTS: ", counter.intercepted)
    print("NOT INTERACTABLE ELEMENTS: ", counter.not_interactable)

def warm_up(driver, duration, finder, actions_per_site, sleep):
    """
        Warm up the environment and profile
    """
    elements_over_scrolling = input("Elements over scrolling? (y/n): ").lower().strip() == 'y'
    visited_websites = []
    deadline = time.time() + float(duration*60)
    while time.time() < deadline:
        random_websites = get_random_websites()
        try:
            for website in random_websites:
                if time.time() >= deadline:
                    break
                act_like_a_human(driver, website, deadline, finder, actions_per_site, sleep, elements_over_scrolling)
        except Exception as e:
            print("Exception at warm_up function:", e)
        visited_websites.extend(random_websites)
    return visited_websites

def add_to_df(row_df: pd.DataFrame, path: Path = METRICS_DATAFRAME):
    """
        Add a new line to the metrics dataframe, I was opening
        and rewriting the csv constantly, really inefficient
    """
    header_needed = not path.exists()
    try:
        row_df.to_csv(path, mode='a', header=header_needed, index=False)
    except:
        raise SystemExit("Come on bruh")

def record_difference(data_before, data_after, duration_of_warm_up, websites_visited, profile_number, finder):
    """
        Store the difference in metrics along with
        the duration of the warm up and sites visited
        in a csv
    """
    KEYWORDS = ['trust_score', 'shadow', 'bot']
    try:
        dataframe = pd.DataFrame({
            "captchas_triggered": [finder.counter],
            "warmup_duration": [duration_of_warm_up],
            "websites_visited": [websites_visited],
            "profile_number": [profile_number],
        })
        for key in KEYWORDS:
            dataframe[f"{key}_before"] = data_before[key]
            dataframe[f"{key}_after"] = data_after[key]
        add_to_df(dataframe)
    except Exception as e:
        raise SystemExit("Error in record_difference function:", e)

def __main__():
    """
        Warm up the profiles specified by the user, for
        the time specified by the user, and compare CreepJs
        metrics before and after
    """
    number_of_profiles = how_many_profiles()
    duration_of_warm_up = how_much_time()
    actions_per_site, sleep_per_action = how_many_actions(), how_much_sleep()
    for i in range(1, number_of_profiles+1):
        start = time.time()
        driver = set_up_driver(i)
        finder = CaptchaFinder(driver)
        metrics_before = get_creepjs_metrics(driver)
        websites_visited = warm_up(driver, duration_of_warm_up, finder, actions_per_site, sleep_per_action)
        print(f"Elapsed: {time.time() - start:.1f} s  (target: {duration_of_warm_up*60}s)")
        metrics_after = get_creepjs_metrics(driver)
        record_difference(metrics_before, metrics_after, duration_of_warm_up, websites_visited, i, finder)
        driver.quit()

if __name__ == '__main__':
    __main__()