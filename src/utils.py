from pathlib import Path
import undetected_chromedriver as uc

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

class ExceptionCounter:
    def __init__(self):
        self.intercepted = 0
        self.not_interactable = 0
        self.elements_clicked = 0