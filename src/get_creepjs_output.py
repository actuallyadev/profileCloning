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
    try:
        ds = WebDriverWait(driver, timeout=15).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class, 'col-six')]"))
        )
        strings = [ds[0].text, ds[1].text]
        metrics = []
        for string in strings:
            splitted_string = string.split("\n")
            for line in splitted_string:
                if any(keyword in line.lower() for keyword in KEYWORDS):
                    metrics.append(line)  # Append as a single-element list for consistency
        return dict(zip(KEYWORDS,metrics))
    except Exception as e:
        print("Could not get CreepJS metrics: ", e)