import os
import re
import interface as ui


# folders in root folder not matched with shows
not_matched = []


def get_tvshow(f, tvdb):
    """
    checks the given directory name against tv shows in thetvdb,
    adds directory & tvdb show object to dirs_to_shows dict

    :param tvdb: tvdbapi instance <tvdbapi>
    :param f: name of directory containing episode files <str>
    :return: A tvdbapi.Show or None
    """
    show_matches = tvdb.search(f, 'en')
    shows = remove_bad_matches(f, show_matches)
    try:
        assert len(shows) is 1
        show = shows[0]
        return show if perfect_match(f, show) else ui.check_match(f, show)

    except AssertionError:
        return no_match(f) if len(shows) is 0 else ui.select_tvshow_from_db_matches(f, shows)


def folder_show_matcher(folders, shows):
    """
    generator for returning 2-tuples of directories with shows

    :param shows: a TVDB API instance
    :param folders: list of directories
    :return 2-tuples pairing directories to shows, where a valid show for the
    directory can be determined:
    """
    for f in folders:
        show = get_tvshow(f, shows)
        if f[0] not in ' _.' and show:
            yield f, show


def dirs_to_shows(tvdb):
    """
    :param: tvdb: a tvdbapi instance <tvdbapi.api>
    :return: a dictonary mapping directories identified as tvshow folders
    to their respective TVDB API show objects.
    """
    # get directories in current directory
    folders = [x for x in os.listdir(".") if os.path.isdir(x)]

    # build folder to show dict
    dirs_shows = {f: s for f, s in folder_show_matcher(folders, tvdb)}

    # print folders being skipped, then print show folders
    ui.display_matches(dirs_shows)

    return dirs_shows


def remove_bad_matches(folder, shows):
    """
    tvdbapi uses a fairly greedy matching algorithm, and as such returns some
     unreasonable matches. this function removes at least some of them.

    :param folder: <str>
    :param shows: list(<tvdbapi.Show>)
    :return: list(<tvdbapi.Show>)
    """
    valid = ('a ', 'the ', 'that ', folder)
    return [s for s in shows if s.SeriesName.lower().startswith(valid)]


def perfect_match(folder, show):
    """
    :param folder: <str>
    :param show: <tvdbapi.Show>
    :return: whether folder name matches show name 'perfectly' <bool>
    """
    delims = re.compile(r'[.-_\s]\s*')
    folder_split = [s for s in re.split(delims, folder.lower())]
    show_split = [s for s in re.split(delims, show.SeriesName.lower())]
    return folder_split == show_split


def no_match(folder):
    """
    adds folder to list of unmatched folders

    :param folder: folder not matched with any show <str>
    :return: None
    """
    not_matched.append(folder)
    return None


#  todo: handle folders in each show folder   ---   ######
def is_season(folder, show_name):
    """
    returns whether the folder passed in is a season folder.
    should only be used at top level of a show folder

    :param show_name: name of tv shows <str>.lower()
    :param folder: folder inside a show folder <str>.lower()
    :return: whether the folder is a season folder <bool>
    """
    if 'season' in folder and 'episode' not in folder:
        return True

    delim = re.compile(r'[\s\-_.]?')

    show_normd = re.sub(delim, ' ', show_name)

    show_split = ' '.split(show_name)
    folder_split = re.split(delim, folder)

    # valid_starts = ('s', 'season')


    valid_starts = re.compile(r'(?i)(s|seas|season)?[\s\-._]?\d{1,3}')
    invalid_contents = re.compile(r'E\d{1,2}',re.I)  # ignore ep folders
    seas_text = re.compile(r'(?i)s?e?a?s?o?n?')
    normd_folder = folder.lower()
    return normd_folder.startswith(valid_starts)


def is_single_episode(folder):
    """
    returns whether the folder is a single episode folder.
    should be used at top level of show folders, and of season folders

    :param folder: folder insode a show folder <str>
    :return: whether the folder is a single episode folder <bool>
    """
