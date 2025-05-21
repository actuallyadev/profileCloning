"""
    This file is a rough draft of the profileCloning (name subject to change) CLI tool

    The objective is making a tool that generates browser profile skeletons
    removing the name_id field and changing its template name, cloning it X times

    After that, the tool should take the newly generated profiles and warm them up to make
    them usable for scraping (optional for the user)

    We will start simple, using Chrome and Windows 11
"""

import psutil
import os, signal

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

def get_chrome_binary_path():
    """
        Find the chrome binary path by searching through
        common locations where chrome.exe is stored.
        If nothing is found the user will be asked to
        provide the path.
    """
    try:
        chrome_binary = search_for_chrome_binary()
    except Exception:
        chrome_binary = ask_user_for_chrome_binary()

def search_for_chrome_binary():
    """
        Search through common locations depending
        on the OS for the chrome binary path,
        if not found throw exception
    """


def ask_user_for_chrome_binary():
    """
        Ask user for the path to the chrome binary.
        This function is used as a last resort, in 
        case of not finding the path of the binary 
        by searching in common locations.
    """
    try:
        binary_path = str(input("Could not find the binary path, specify it please"))
        return binary_path
    except Exception:
        pass

def get_directory_path_and_name():
    """
        Ask the user for the directory path and name
        where the profile will be stored
    """
    directory_path, directory_name = "", ""
    try:
        directory_path = str(input("Could not find the binary path, specify it please"))
    except Exception:
        pass
    try:
        directory_name = str(input("Could not find the binary path, specify it please"))
    except Exception:
        pass
    return directory_path, directory_name

def __main__():
    """
        Called when user executes the tool
    """
    directory_path, directory_name = get_directory_path_and_name()
    chrome_binary_path = get_chrome_binary_path()
    kill_chrome_processes()
    create_profile_skeleton(directory_path, directory_name, chrome_binary_path)