import re
import string_parser as spars

# filename extensions for video files
VIDEO_FN_EXTS = tuple('avi flv m4v mkv mov mp4 mpg vob wmv'.split())
DISALLOWED_CHARS = set('\/:*?"<>')


# boolean checks for file types

def is_video(fn):
    # return splitext(fn)[1:] in VIDEO_FN_EXTS
    return fn.endswith(VIDEO_FN_EXTS)

def is_episode(fn):
    return is_video(fn) and spars.contains_epdata(fn)










