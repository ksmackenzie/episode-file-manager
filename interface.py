

def initialise(cwd):
    """
    Displays intro text and folder being scanned for shows

    :param cwd: current working directory (root folder for shows)
    :return:  None
    """
    print("\n~*< KM Episode File Manager >*~\n")
    print("Scanning for tv show folders in:\n\t{}\n\n".format(cwd))


def select_tvshow(folder, shows):
    """
    Handles cases where more than one match for the directory name was found
    in the tvdb

    :param folder: possible show folder <str>
    :param shows: list of show objects <list(<tvdb.Show>)>
    :return: show selected by user, else None if user opts to skip this dir
    """

    # display possible matches for show
    print("More than one match found for {}:".format(folder))
    for i, show in enumerate(shows):
        print("\t{}) {}".format(i + 1, show.SeriesName))

    prompt = "Enter the number of the correct show as listed, or s to skip: "

    # loop until valid selection is entered
    while True:
        response = input(prompt)
        skipping = response.lower().startswith('s')
        if skipping:
            print()
            return None

        try:
            in_range = int(response)-1 in range(len(shows))
            if in_range:
                print()
                return shows[int(response) - 1]

            raise IndexError

        except (ValueError, IndexError, TypeError):
            print("Error, invalid response:", response)


def check_match(folder, show):
    """
    has user check imperfect match for show & folder

    :param show: tvdbapi show object <tvdbapi.Show>
    :param folder: name of show folder <str>
    :return: the confirmed correct show, or None
    """
    text = "An imperfect match for the folder '{}' was found:\n\t{}" \
           "\nIs this the correct show for this folder? (y/n): "
    prompt = text.format(folder, show.SeriesName)
    response = input(prompt)
    print()
    return show if response[0].lower() == 'y' else None


def display_matches(dirs_shows):
    """
    displays list of unmatched folders, then list of matched folders

    :param dirs_shows: folders in root shows folder mapped to shows
    :return: None
    """
    print("The following folders will be processed as tv show folders:")
    for folder, show in dirs_shows.items():
        print("\t{}:\n\t\t{}\n".format(folder, show))
    print()

