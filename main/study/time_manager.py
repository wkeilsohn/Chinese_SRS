# William Keilsohn
# September 25 2025

# Import Packages
# import time
# import numpy
from datetime import datetime
from django.utils import timezone 

# Define Variables

time_dict = {
    "PP": 0,
    "P0": 2,
    "P1": 4,
    "P2": 8,
    "P3": 24,
    "P4": 48,
    "P5": 168,
    "P6": 336,
    "P7": 732,
    "P8": 2928,
}
format_string = "%Y-%m-%d %H:%M:%S.%f"


# Define Functions
def calculate_time_since_last_study(last_review_time):
    ctime = timezone.now()
    # last_review_time = timezone.datetime(last_review_time, tzinfo=timezone.get_current_timezone()) # Should be pre-formated
    time_diff = ctime - last_review_time
    time_diff = time_diff.total_seconds()
    return time_diff / 3600


def check_if_study(p_val, review_time):
    global time_dict
    rep_time = time_dict[p_val]
    if review_time >= rep_time:
        return True
    else:
        return False


# # Test Application
# if __name__ == "__main__":
#     rev_time = calculate_time_since_last_study(datetime(2025, 9, 26, 8, 0, 0))
#     print(check_if_study("P0", rev_time))
