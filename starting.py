"""
    This file is a rough draft of the profileCloning (name subject to change) CLI tool

    The objective is making a tool that generates browser profile skeletons
    removing the name_id field and changing its template name, cloning it X times

    After that, the tool should take the newly generated profiles and warm them up to make
    them usable for scraping (optional for the user)

    We will start simple, using Chrome and Windows 11
"""

import time
import psutil
from decorators import do_not_redeem_it
import os, signal, platform
from pathlib import Path
from subprocess import Popen

def kill_chrome_processes():
    """
        Kill all chrome process leveraging the psutil library.
        Works on Windows, testing will be made on other systems
        to know for sure
    """
    for process in psutil.process_iter(['name', 'pid', 'username']):
        if 'chrome' in process.name():
            process.kill()

def create_profile_skeleton(directory: str, profile_directory_name: str, chrome_binary_path):
    """
        Create profile skeleton by executing chrome binary
        with no first run, no sync and no extensions flags
        set.
    """
    cmd = [
        chrome_binary_path,
        f"--user-data-dir={directory}",
        f"--profile-directory={profile_directory_name}",
        "--no-first-run",
        "--disable-sync",
        "--disable-sync-preferences",
        "--disable-extensions"
    ]

    Popen(cmd)

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
        Check if directory to store profiles has already been
        created and its contents. If not, create it.
        The name of the profile should
        be the next of the last one created -> Last created: Profile_1
        -> Next: Profile_2
    """
    # Create profile folder if it does not exist
    try:
        os.mkdir("ProfileFolder")
    except FileExistsError:
        pass
    profile_directory = os.path.join(os.getcwd(), "ProfileFolder")
    # Get contents of directory
    ls = os.listdir(profile_directory)
    if ls:
        # Check the contents of the directory and find the farthest profile
        next_folder_name = get_next_folder_name(profile_directory, ls)
        return profile_directory, next_folder_name
    else:
        print("CHECKK: ", profile_directory)
        return profile_directory, "profile_1"
    
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

def get_next_folder_name(full_path: str, ls: list):
    """
        Get the last folder name
    """
    last_folder_name = get_last_folder_name(full_path, ls)
    # We assume the last folder name will be something like profile_1056
    last_folder_name_letter = last_folder_name.split("_")[1]
    return "profile_" + str(int(last_folder_name_letter) + 1)

def get_last_folder_name(full_path: str, ls: list):
    """
        Sort the directory contents list and return 
        the subdirectory name of the highest profile,
        for example -> [profile_1, profile_2]:
        return profile_2
    """
    largest_ctime, newest_file = 0, ls[0]
    for file in ls:
        if 'profile_' in file:
            file_path = os.path.join(full_path, file)
            file_creation_time = float(os.path.getctime(file_path))
            if file_creation_time > largest_ctime:
                largest_ctime = file_creation_time
                newest_file = file
    return newest_file

def __main__():
    """
        Called when user executes the tool
    """
    for i in range(0,5):
        directory_path, directory_name = set_directory_path_and_name()
        print("DIRECTORY PATH: ", directory_path)
        print("DIRECTORY NAME: ", directory_name)
        chrome_binary_path = get_chrome_binary_path()
        print("Chrome binary path: ", chrome_binary_path)
        kill_chrome_processes()
        create_profile_skeleton(directory_path, directory_name, chrome_binary_path)
        time.sleep(2)
        try:
            kill_chrome_processes()
        except:
            pass

__main__()