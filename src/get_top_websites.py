import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

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
    except Exception as e:
        print("Important: ", e)

driver = uc.Chrome()
websites = get_top_websites(driver)
print(websites)