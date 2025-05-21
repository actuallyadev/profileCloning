"""
    This file is a rough draft of the profileCloning (name subject to change) CLI tool

    The objective is making a tool that takes as input one valid, used browser profile
    and cloning it, removing the name_id field and changing its template name

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