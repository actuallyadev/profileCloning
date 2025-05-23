"""
    This file is a rough draft of the profileCloning (name subject to change) CLI tool

    The objective is making a tool that generates chrome enviroments which, as a subdirectory,
    each have one profile. We cannot have different profiles in the same chrome enviroment as they
    will get linked by Local State's 'client_id'.

    We need to clear the client_id field in Local State and set a profile in the enviroment

    After that, the tool should access each chrome enviroment, take the newly generated profile
    and warm it up to make it usable for scraping (optional for the user)

    We will start simple, using Chrome and Windows 11
"""

import time
import psutil
from decorators import do_not_redeem_it
import os, signal, platform
from pathlib import Path
from subprocess import Popen, PIPE

def kill_chrome_processes():
    """
        Kill all chrome process leveraging the psutil library.
        Works on Windows, testing will be made on other systems
        to know for sure
    """
    for process in psutil.process_iter(['name', 'pid', 'username']):
        if 'chrome' in process.name():
            process.kill()

def create_profile_skeleton(directory: str, environment_directory_name: str, chrome_binary_path):
    """
        Create chrome environment by executing chrome binary
        with no first run, no sync and no extensions flags
        set.
    """
    profile_directory_name = "profile_" + environment_directory_name.split("_")[1]
    cmd = [
        chrome_binary_path,
        f"--user-data-dir={directory + f'\{environment_directory_name}'}",
        f"--profile-directory={profile_directory_name}",
        "--no-first-run",
        "--disable-sync",
        "--disable-sync-preferences",
        "--disable-extensions"
    ]

    Popen(cmd, stderr=PIPE, stdout=PIPE)

def get_chrome_binary_path():
    """
        Find the chrome binary path by searching through
        common locations where chrome.exe is stored.
        If nothing is found the user will be asked to
        provide the path.
    """
    try:
        return search_for_chrome_binary()
    except Exception:
        return ask_user_for_chrome_binary()

def search_for_chrome_binary():
    """
        Search through common locations depending
        on the OS for the chrome binary path,
        if not found return None
    """
    current_os = platform.system() # Returns OS -> Windows, Linux, MacOs without version (Ubuntu, Windows 11, etc)
    print("CURRENT OS", current_os)
    potential_paths = []
    if current_os == 'Windows':
        # expandvars just replaces the enviroment variable names with the actual values
        potential_paths = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        ]
    
    elif current_os == 'Darwin':
        potential_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            os.path.expanduser("~/Applications/Chromium.app/Contents/MacOS/Chromium"),
        ]

    else:
        potential_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
            "/opt/google/chrome/google-chrome",
            "/snap/bin/chromium",
        ]

    for potential_path in potential_paths:
        if os.path.exists(potential_path):
            print("PATH FOUND: ", potential_path)
            return potential_path
    
    raise Exception("Could not automatically find the chrome binary")

def ask_user_for_chrome_binary():
    """
        Ask user for the path to the chrome binary.
        This function is used as a last resort, in 
        case of not finding the path of the binary 
        by searching in common locations.
    """
    try:
        binary_path = str(input("Could not find the binary path, specify it please\n"))
        if not os.path.exists(binary_path):
            raise Exception()
        return binary_path
    except Exception:
        raise SystemExit("Binary path is not valid, run the tool and enter a different one") # Same as calling sys.exit() but this is more stylish
        
def set_directory_path_and_name():
    """
        Check if directory to store chrome environments has
        already been created. If not, create it.
        The name of the profile should
        be the next of the last one created -> Last created: Environment_1
        -> Next: Environment_2
    """
    # Create profile folder if it does not exist
    try:
        os.mkdir("EnvironmentDirectory")
    except FileExistsError:
        pass
    environment_directory = os.path.join(os.getcwd(), "EnvironmentDirectory")
    # Get contents of directory
    ls = os.listdir(environment_directory)
    if ls:
        # Check the contents of the directory and find the farthest profile
        next_folder_name = get_next_folder_name(ls)
        return environment_directory, next_folder_name
    else:
        print("CHECKK: ", environment_directory)
        return environment_directory, "environment_1"
    
@do_not_redeem_it
def get_directory_path_and_name():
    """
        Ask the user for the directory path and name
        where the profile will be stored, not needed for now
    """
    directory_path, directory_name = "", ""
    try:
        directory_name = str(input("Select the folder name where the profile will be stored\n"))
    except Exception:
        pass
    try:
        directory_path = str(input("Select the directory path where the new folder will be created\n"))
    except Exception:
        pass
    return directory_path, directory_name

def get_next_folder_name(ls: list):
    """
        Get the last folder name
    """
    last_folder_name = get_last_folder_name(ls)
    # We assume the last folder name will be something like profile_1056
    last_folder_name_letter = last_folder_name.split("_")[1]
    return "environment_" + str(int(last_folder_name_letter) + 1)

def get_last_folder_name(ls: list):
    """
        Sort the directory contents list and return 
        the subdirectory name of the highest profile,
        for example -> [environment_1, environment_2]:
        return environment_2
    """
    largest_number, newest_file = 0, ls[0]
    for current_file in ls:
        current_number = int(current_file.split('_')[1])
        if current_number > largest_number:
            largest_number = current_number
            newest_file = current_file
    return newest_file

def get_user_input():
    """
        Helper function to sanitize input
        and handle edge cases better
    """
    try:
        return int(input("What is the number of profiles you want to generate?\n"))
    except:
        raise SystemExit("INVALID INPUT!?!?!?!?!")

def __main__():
    """
        Kill chrome processes, create profile skeleton
        and modify the json values of Local State's 
        client_id, then copy X times.
    """
    number_of_environments = get_user_input()
    chrome_binary_path = get_chrome_binary_path()
    for i in range(0, number_of_environments):
        try:
            kill_chrome_processes()
        except:
            pass
        directory_path, directory_name = set_directory_path_and_name()
        print(directory_name, directory_path)
        create_profile_skeleton(directory_path, directory_name, chrome_binary_path)
        time.sleep(2)
    try:
        kill_chrome_processes()
    except:
        pass

if __name__ == "__main__":
    __main__()