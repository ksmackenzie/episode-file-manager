import os
from pytvdbapi import api

# local imports
import dirmanager as dman
import filemanager as fman
import interface as ui

# pytvdbapi key and instance
TVDBAPI_KEY = "4452E85C22F29289"
TVDB = api.TVDB(TVDBAPI_KEY)

# initialise user interface
cwd = os.getcwd()
ui.initialise(cwd)

# build dict mapping show folders to show objects
showdirs_dict = dman.dirs_to_shows(TVDB)

# loop through folders identified as tv series folders
for show_folder, show in showdirs_dict.items():

    # switch working directory to current tv show directory
    show_dir_path = os.path.abspath(show_folder)
    os.chdir(show_dir_path)

    # loop through each tv show folder
    for root, dirs, files in os.walk(show_dir_path):  # handle_show_dir(
        # show_dir)?
        # handle files
        ep_files_loose = [f for f in files if fman.is_episode(f)]

        # handle directories
        for directory in dirs:
            # if season_folder:
            #   handle_season_folder(dir, season_num)

            # if single_ep_dir(dir):
            #   handle_single_ep_dir(dir)
            #     walk, check for sgl ep dirs, and epfiles
            # handle single ep (dirs)
            pass

    # move back up to the root folder
    os.chdir('..')

