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
import time
import string
import random
from pathlib import Path

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
    print("Just loaded: ", user_data_dir_path, "+ myprofile")
    return uc.Chrome(options=chrome_options)

def get_random_websites():
    """
        Using the random module and the choices function
        we can easily get k random websites in one line
    """
    return random.choices(TOP_WEBSITES, k=7)

def get_random_letter():
    """
        Return a random letter
    """
    return random.choice(string.ascii_letters)

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
    pass

def act_like_a_human(driver, website):
    """
        Scroll, click a few buttons, read the text,
        think a bit, try to emulate real user behaviour
        just enough to get proper cookies and gain
        reputation.
    """
    try:
        # Without https:// it was not working
        driver.get(f"https://{website}")
    except Exception as e:
        print("Importante: ", e)
    random_scroll_value = random.choice(range(0, 1080))
    driver.execute_script(f"window.scrollTo(0, {random_scroll_value})")
    for i in range(0, random.choice(range(1, 15))):
        random_letter = get_random_letter()
        element = find_element(driver, random_letter)
        interact_with_element(element)
        time.sleep(1.5)

def warm_up(driver, duration: int, starting_timestamp):
    """
        Warm up the environment and profile
    """
    try:
        # Could store in a variable but I like being a G
        while abs(time.time() - (starting_timestamp + float(duration*60))) > 0.1:
            random_websites = get_random_websites()
            for website in random_websites:
                act_like_a_human(driver, website)
    except Exception as e:
        print("Important: ", e)

def get_data(i: int):
    """
        Get length of relevant files
    """
    pass

def check_difference(data_before, data_after):
    """
        Check difference before
    """
    pass

def __main__():
    """
        Get the user's input on how many profiles
        and how much time in minutes to warm-up
    """
    number_of_profiles = how_many_profiles()
    duration_of_warm_up, current_timestamp = how_much_time(), time.time()
    for i in range(1, number_of_profiles+1):
        data_before = get_data(i)
        driver = set_up_driver(i)
        warm_up(driver, duration_of_warm_up, current_timestamp)
        data_after = get_data(i)
        check_difference(data_before, data_after)
        driver.quit()

if __name__ == '__main__':
    __main__()