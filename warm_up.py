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
from pathlib import Path

def how_many_profiles():
    """
        Ask the user how many/which profiles he wants
        to warm-up.
    """
    try:
        return int(input("How many profiles do you want to warmup?\n"))
    except:
        raise SystemExit("Not an integer, try again\n")
    
def how_much_time():
    """
        Ask the user how many/which profiles he wants
        to warm-up.
    """
    try:
        return int(input("Specify the time in minutes that each profile should warm-up\n"))
    except:
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
    chrome_options.add_argument('--headless=new')
    print("Just loaded: ", user_data_dir_path, "+ myprofile")
    return uc.Chrome(options=chrome_options)

def get_top_websites(driver):
    """
        Get the top 40 websites from wikipedia
    """
    try:
        driver.get('https://en.wikipedia.org/wiki/List_of_most-visited_websites')
        top_websites_elements = driver.find_elements(By.XPATH, f'//*[contains(text(), ".com")]')
        print("Important", top_websites_elements)
        for website in top_websites_elements:
            print(website.text)
        return [website.text for website in top_websites_elements]
    except:
        print("Important")

def get_random_websites(websites):
    """
        Using the random module and the choices function
        we can easily get k random websites in one line
    """
    import random

    return random.choices(websites, k=7)

def act_like_a_human(driver, website):
    """
        Scroll, click a few buttons, read the text,
        think a bit, try to emulate real user behaviour
        just enough to get proper cookies and gain
        reputation.
    """
    pass

def warm_up(driver, duration: int):
    """
        Warm up the environment and profile
    """
    try:
        while duration:
            websites = get_top_websites(driver)
            random_websites = get_random_websites(websites)
            for website in random_websites:
                act_like_a_human(driver, website)
    except:
        print("Important")

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
    duration_of_warm_up = how_much_time()
    for i in range(1, number_of_profiles+1):
        data_before = get_data(i)
        driver = set_up_driver(i)
        warm_up(driver, duration_of_warm_up)
        data_after = get_data(i)
        check_difference(data_before, data_after)

if __name__ == '__main__':
    __main__()