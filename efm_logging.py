import time

def timestamp():
    """
    timestamp for log files

    :return: current date and time in the form YYYYMMDD_HHMM
    """
    return time.strftime('%Y%m%d_%H%M')

