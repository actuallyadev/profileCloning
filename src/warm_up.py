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
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from captcha_finder import CaptchaFinder
from get_creepjs_output import get_creepjs_metrics
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
    'acept', 'permit',
    # French
    'accepte', 'autoris',
    # German
    'akzeptieren', 'einvers',
    # Portuguese
    'aceit',
    # Italian
    'accett', 'accett'
]

METRICS_DATAFRAME = Path("creepjs_metrics.csv")

def set_up_csv():
    """
        Create csv if not already created to store CreepJS
        metrics.
    """
    if not METRICS_DATAFRAME.exists():
        try:
            columns = [
                "warmup_duration",
                "websites_visited",
                "profile_number",
                "trust score_before",
                "trust score_after",
                "shadow_before",
                "shadow_after",
                "bot_before",
                "bot_after"
            ]
            pd.DataFrame(columns=columns).to_csv("creepjs_metrics.csv", index=False)
        except Exception as e:
            print("Could not setup csv: ", e)

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

def set_up_driver(i: int):
    """
        Setup the selenium driver, load the relevant
        profile by adding user_data_dir location and
        profile name to the chrome options
    """
    user_data_dir_path = Path.cwd() / "EnvironmentDirectory" / f"environment_{i}"
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={user_data_dir_path}')
    chrome_options.add_argument('--profile-directory=myprofile')
    # To avoid restore shit banner
    chrome_options.add_argument("--disable-session-crashed-bubble")
    # chrome_options.add_argument('--headless=new')
    print("Just loaded: ", user_data_dir_path, "+ myprofile")
    return uc.Chrome(options=chrome_options, version_main=136)

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
                # Scroll into view first
                driver.execute_script("window.scrollTo(0, 100)")
                # Case-insensitive version
                driver.find_element(By.XPATH, f'//*[contains(translate({attribute}, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{possibility}")]').click()
                print("FUCK YEAH GOT THEM SWEET COOKIES")
                return
            except NoSuchElementException:
                # scroll until end of page
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                # driver.find_element(By.XPATH, f'//*[contains(translate({attribute}, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{possibility}")]').click()
                continue
            except Exception:
                continue

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
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random.uniform(9, 16)))

def find_element(driver, random_letter):
    """
        Helper function to simplify act_like_a_human_logic
    """
    try:
        return driver.find_element(By.XPATH, f'//*[contains(text(), "{random_letter}")]')
    except Exception as e:
        print("Error: ", e)

def interact_with_element(element):
    """
        Interact with the element:
        Click it, if it is not clickable
        try to write something, if that fails
        try something else
    """
    if element.tag_name == "a" or element.tag_name == "button":
        try:
            element.click()
        except Exception as e:
            print("Exception at interact_with_element: ", e)
    elif element.tag_name == "input":
        try:
            element.send_keys(get_random_input())
        except Exception as e:
            print("Exception at interact_with_element: ", e)
    else:
        pass

def scroll_randomly(driver):
    """
        Scroll a random value
    """
    random_scroll_value = random.choice(range(0, 1080))
    driver.execute_script(f"window.scrollTo(0, {random_scroll_value})")

def get_random_element(driver):
    """
        Return a random button or...
    """
    possible_elements = ['button', 'input', 'a']
    for element in possible_elements:
        try:
            return driver.find_element(By.TAG_NAME, element)
        except NoSuchElementException:
            continue
        except Exception as e:
            print("Exception in get_random_element: ", e)


def interact_with_random_element(driver):
    """
       Search for a random element, every 5 seconds
       check for a captcha by creating a CaptchaFinder
       object
    """
    element = get_random_element(driver)
    interact_with_element(element)
    time.sleep(random.uniform(0.8, 2.3))

def act_like_a_human(driver, website, deadline):
    """
        Scroll, click a few buttons, read the text,
        think a bit, try to emulate real user behaviour
        just enough to get proper cookies and gain
        reputation.
    """
    possible_functions = [scroll_randomly, interact_with_random_element]
    try:
        # Without https:// it was not working
        driver.get(f"https://{website}")
        print("Just went to ", website)
        time.sleep(random.uniform(0.7, 1.3))
        accept_cookies(driver)
    except Exception as e:
        print("Importante: ", e)
    for i in range(0, random.choice(range(12, 18))):
        if time.time() > deadline:
            break
        random.choice(possible_functions)(driver)

def warm_up(driver, duration, starting_timestamp):
    """
        Warm up the environment and profile
    """
    try:
        visited_websites = []
        deadline = starting_timestamp + float(duration*60)
        while time.time() < deadline:
            random_websites = get_random_websites()
            for website in random_websites:
                if time.time() >= deadline:
                    break
                act_like_a_human(driver, website, deadline)
            visited_websites.extend(random_websites)
        return visited_websites
    except Exception as e:
        print("Exception at warm_up function:", e)

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

def record_difference(data_before, data_after, duration_of_warm_up, websites_visited, profile_number):
    """
        Store the difference in metrics along with
        the duration of the warm up and sites visited
        in a csv
    """
    KEYWORDS = ['trust_score', 'shadow', 'bot']
    try:
        dataframe = pd.DataFrame({
            "warmup_duration": [duration_of_warm_up],
            "websites_visited": [websites_visited],
            "profile_number": [profile_number]
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
    set_up_csv()
    number_of_profiles = how_many_profiles()
    duration_of_warm_up, current_timestamp = how_much_time(), time.time()
    for i in range(1, number_of_profiles+1):
        driver = set_up_driver(i)
        metrics_before = get_creepjs_metrics(driver)
        websites_visited = warm_up(driver, duration_of_warm_up, current_timestamp)
        metrics_after = get_creepjs_metrics(driver)
        record_difference(metrics_before, metrics_after, duration_of_warm_up, websites_visited, i)
        driver.quit()

if __name__ == '__main__':
    __main__()