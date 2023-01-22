import os

DEBUG = False
APP_PREFIX = "MJAPI_"

# If you're running a standard installation of M&J Timing, this is the default path.
MJTIMING_PATH = os.environ.get(APP_PREFIX + "MJTIMING_PATH", os.sep.join(["C:", "mjtiming"]))

CONFIG_PATH = os.environ.get(APP_PREFIX + "CONFIG_PATH", MJTIMING_PATH + os.sep + "config")
EVENTDATA_PATH = os.environ.get(APP_PREFIX + "EVENTDATA_PATH", MJTIMING_PATH + os.sep + "eventdata")

PATHS = [MJTIMING_PATH, CONFIG_PATH, EVENTDATA_PATH]


