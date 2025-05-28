from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

KEYWORDS = ['bot', 'lies', 'errors', 'trust score', 'shadow']

def get_creepjs_metrics(driver):
    """
    bot: score

        Main indicator of detectability.

        Shows your overall bot probability.

        Example: bot: 0.13:stranger:csl:00000001

        Goal: Keep this as low as possible (under 0.2 is decent).

    lies: count

        Number of detected inconsistencies (lies) in fingerprint data.

        Includes things like mismatched screen dimensions, fake UA, or WebDriver flags.

        Goal: lies (0): none — zero lies.

    errors: count

        JavaScript execution errors often caused by headless or missing APIs.

        Goal: errors (0): none

    trust score:

        General trustworthiness rating of the browser fingerprint.

        Expressed as a percentage + letter grade (e.g., 69% D+).

        Goal: 80%+ and at least a B or better.

    shadow: score

        Number of known stealth modifications detected.

        Modifications like changing navigator.webdriver may trigger this.

        Goal: Keep shadow as low as possible (0 ideally).
    """
    metrics = {}
    driver.get('https://abrahamjuliot.github.io/creepjs/')
    try:
        first_col = WebDriverWait(driver, timeout=15).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//span[contains(@class, "unblurred")]'))
        )
        metrics["trust_score"] = first_col[2].text
        metrics["shadow"] = first_col[6].text
        metrics["bot"] = driver.find_element(By.XPATH, '//div[contains(@class, "unblurred")]').text.split(":")[1]
        return metrics
    except Exception as e:
        print("Could not get CreepJS metrics: ", e)

def find_lies(driver):
    """
        Get lies metric
    """
    try:
        lies = driver.find_element(By.XPATH, '//div[@class = " lies"]').text
        return process_lies(lies)
    except Exception as e:
        print("Exception while getting lies: ", e)

def process_lies(lies):
    """
        Process and clean lies text
    """
    pass            