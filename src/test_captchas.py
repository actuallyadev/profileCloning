"""
    Compare first warmed up environment (environment_1):
        warm_up(environment_1, 10 minutes, 35 actions, 0.6 sleep, clicks>scrolling)
    with a fresh environment (environment_2):
        warm_up(environment_1, X minutes, 15 actions, 0.3, clicks>scrolling)
        warm_up(environment_2, X minutes, 15 actions, 0.3, clicks>scrolling)
    by calling act_like_a_human with a couple captcha heavy websites
"""

import time
import warm_up
from captcha_finder import CaptchaFinder
from get_creepjs_output import get_creepjs_metrics

CAPTCHA_HEAVY_SITES = [
    "www.tiktok.com/foryou?lang=en",
    "reddit.com/r/worldnews/",
    "nytimes.com/section/technology",
    "aliexpress.com",
    "www.walmart.com/",
    "booking.com/city/gb/london.en-gb.html",
    "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html",
    "duckduckgo.com/?q=python+web+scraping",
    "accuweather.com/en/us/new-york/10007/weather-forecast/349727"
]

def get_captcha_heavy_websites():
    """
        Return captcha heavy websites
    """
    return CAPTCHA_HEAVY_SITES

warm_up.get_random_websites = get_captcha_heavy_websites

DURATION_OF_WARM_UP = 4 # minutes for test
NUMBER_OF_INTERACTIONS = 500
SLEEP_BETWEEN_ACTIONS = 0

def run_loop(driver, finder, i):
    """
        Run loop
    """
    start = time.time()
    metrics_before = get_creepjs_metrics(driver)
    websites_visited = warm_up.warm_up(driver, DURATION_OF_WARM_UP, finder, NUMBER_OF_INTERACTIONS, SLEEP_BETWEEN_ACTIONS)
    print(f"Elapsed: {time.time() - start:.1f} s  (target: {DURATION_OF_WARM_UP*60}s)")
    metrics_after = get_creepjs_metrics(driver)
    warm_up.record_difference(metrics_before, metrics_after, DURATION_OF_WARM_UP, websites_visited, i, finder)
    driver.quit()

def run_that_shit():
    """
        Compare non warmed VS warmed up environments.
    """
    # Run loop with warm driver
    warm_driver = warm_up.set_up_driver(1)
    warm_finder = CaptchaFinder(warm_driver)
    run_loop(warm_driver, warm_finder, 1)
    # Run loop with non-warm driver
    not_warm_driver = warm_up.set_up_driver(2)
    not_warm_finder = CaptchaFinder(not_warm_driver)
    run_loop(not_warm_driver, not_warm_finder, 2)

if __name__ == "__main__":
    run_that_shit()