import os

DEBUG = False

if DEBUG:
    MJTIMING_PATH = "./mjtiming"
else:
    # If you're running a standard installation of M&J Timing, this is the default path.
    MJTIMING_PATH = os.sep.join(["C:", "mjtiming"])

CONFIG_PATH = MJTIMING_PATH + os.sep + "config"
EVENTDATA_PATH = MJTIMING_PATH + os.sep + "eventdata"

PATHS = [MJTIMING_PATH, CONFIG_PATH, EVENTDATA_PATH]


