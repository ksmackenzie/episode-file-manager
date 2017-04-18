import re
import os

# regex patterns for matching season episode identifiers in filenames
EP_PATTERNS = (
    re.compile(r's\d{1,2}.*e\d{1,2}', re.I),  # SDDEDD
    re.compile(r'\d{1,2}[x|-]\d{1,2}', re.I),  # DXD, D-D
    re.compile(r'\d{3,4}'),  # DDD, DDDD
    re.compile(r'season[\s|.]\d{1,2}[\s|.]episode[\s|.]\d{1,2}', re.I)  # LONG
)

# season episode patterns that may be in filenames in single ep dirs
SGL_DIR_EP_PATTERNS = (
    re.compile(r'\d{1,3}')
)


def remove_show_name(fn, showname):
    """
    Removes the show name from an epfile.

    Primarily for use renaming epfiles in season folders. Such files will
    often not have season identifiers in them, and as such episode numbers
    may be confused with show titles if the show title contains a digits,
    eg '30 Rock E04.mp4' could be identified as season 30.

    :param fn: file to be renamed <str>
    :param showname: title of show <str>
    :return: the filename with the show name removed <str>
    """

    # replace whitespace in showname with a regex set of delimiters
    show_pattern = showname.replace(' ', '[ _.\-]')

    # remove the showname pattern from the filename, ignoring case
    return re.sub(show_pattern, '', fn, flags=re.I)


# todo: refactor to return match? Or seas/ep tuple?
def contains_epdata(fn, season=None):
    # TODO: something
    """
    Checks for substrings identifying fn as an episode.

    :param fn: filename <str>
    :param season:
        If the file is in a season folder, season number may not
    be embedded in the filename. In such cases the season number is passed in.
    :return:
        Whether episode data was detected in the filename
    """
    for pattern in EP_PATTERNS:
        if pattern.search(fn):
            # season-ep id found in filename
            return True

    if season:
        # todo: fix this nonsense
        # whether the first substring in the string split around '.' contains a
        # digit? seems a bit stupid...
        return any(c.isdigit() for c in fn.split('.')[0])
    return False

def remove_filename_ext(fn):
    return os.path.splitext(fn)[0]

def get_seasep_numbers(f, showname):
    """
    parses f to determine the which season and episode it belongs to

    :param f: <str>
        file or directory of tv show video file
    :param showname: <str>
        name of show being considered. This is only necessary to help avoid
        confusion when parsing chars in fn, eg hyphens and digits that are in
        the show name. remove_show_name is used to this end.
    :return: tuple(<str>)
        a tuple representing the season and episode numbers
    """
    #todo: handle qualifiers in showname that may not appear in filename,
    # eg '2015', '(US)'

    showname_removed = remove_show_name(f, showname)
    ext_and_showname_removed = remove_filename_ext(showname_removed)

    # replace non-digits with whitespace, remove leading/trailing whitespace
    digits_str = re.sub(r'\D+', ' ', ext_and_showname_removed).strip()

    digits_list = [ds.zfill(2) for ds in digits_str.split()]
    if len(digits_list) == 2:
        return digits_list[0], digits_list[1]


# testing
f = '30.rock.s02e23.blahblah.mp4'
showname = '30 rock'
print(get_seasep_numbers(f, showname))