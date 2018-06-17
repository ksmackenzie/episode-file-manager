from typing import Optional, List, Dict
from pytvdbapi.api import Show


def initialise(cwd: str) -> None:
    """
    Displays intro text and folder being scanned for shows

    :param cwd: current working directory (root folder for show folders)
    :return:  None
    """
    print("\n~*< KM Episode File Manager >*~\n")
    print("Scanning for tv show folders in:\n\t{}\n\n".format(cwd))


def select_tvshow_from_db_matches(folder: str, shows: List[Show]) -> Optional[Show]:
    """Handles cases where more than one match for the directory name was found
    in the tvdb
    precondition: len(shows) >= 2

    """

    # display possible matches for show
    # todo: make index number a variable instead of plus-one-ing it
    print(f"More than one match found for {folder}:")
    for i, show in enumerate(shows):
        display_index = i + 1
        print("\t{}) {}".format(display_index, show.SeriesName))

    # user selects number of show
    prompt = "Enter the number of the correct show as listed, or s to skip: "
    while True:  # loop until valid response from user
        response = input(prompt)
        skipping = response.lower().startswith('s')
        valid_response = skipping or int(response)
        if skipping:  # shows aren't relevant to user, move on
            print()
            return None
        try:  # check: user selected a valid response other than skip?
            user_selected_number = int(response) - 1
            valid_show_by_user = user_selected_number in range(len(shows))
            if valid_show_by_user:  # return valid show selected by user
                valid_show = shows[user_selected_number]
                print()
                return valid_show
            else:  # user selected a number, but not in appropriate range
                raise IndexError
        except (ValueError, IndexError, TypeError): # handle user fuck ups
            print(f"Error, invalid response: {response}")
            print("please try again\n")


def check_match(folder: str, show: Show) -> Show:
    """has user check imperfect match for show & folder"""

    text = "An imperfect match for the folder '{}' was found:\n\t{}" \
           "\nIs this the correct show for this folder? (y/n): "
    prompt = text.format(folder, show.SeriesName)
    response = input(prompt)
    print()
    return show if response[0].lower() == 'y' else None


def display_matches(dirs_shows: Dict[str, Show]) -> None:
    """displays list of unmatched folders, then list of matched folders
    :param dirs_shows: folders in root shows folder mapped to shows
    :return: None"""

    print("The following folders will be processed as tv show folders:")
    for folder, show in dirs_shows.items():
        print("\t{}:\n\t\t{}\n".format(folder, show))
    print()
