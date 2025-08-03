import os
import shutil

def clear_downloads():
    folder = "downloads"
    for f in os.listdir(folder):
        os.remove(os.path.join(folder, f))

def get_downloads():
    folder = "downloads"
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    return files
