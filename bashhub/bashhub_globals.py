"""
This file should be used for declaring any global variables that need to be
pulled in from environment variables or are just used across multiple files.
"""

import os
import re
import time
import stat
import ConfigParser
from ConfigParser import NoSectionError, NoOptionError

# Current time in milleseconds to use across app.
current_milli_time = lambda: int(round(time.time() * 1000))

# Optional environment variable to configure for development
# export BH_URL='http://localhost:9000'
BH_URL = os.getenv('BH_URL', 'https://bashhub.com')

BH_HOME = '~/.bashhub' if 'HOME' not in os.environ.keys() \
        else os.environ['HOME'] + '/.bashhub'


def write_to_config_file(section, value):
    exists = os.path.exists(BH_HOME)
    file_path = BH_HOME + '/config'
    permissions = stat.S_IRUSR | stat.S_IWUSR
    if exists:
        config = ConfigParser.ConfigParser()
        config.read(BH_HOME + '/config')
        # Add our section if it doesn't exist
        if not config.has_section("bashhub"):
            config.add_section("bashhub")

        config.set("bashhub", section, value)
        with open(file_path, 'w') as config_file:
            config.write(config_file)
            os.chmod(file_path, permissions)
        return True
    else:
        print("Couldn't find bashhub home directory. Sorry.")
        return False


def get_from_config(key):
    try:
        config = ConfigParser.ConfigParser()
        config.read(BH_HOME + '/config')
        return config.get('bashhub', key)
    except (NoSectionError, NoOptionError) as error:
        return ""


def get_access_token():
    access_token = get_from_config("access_token")
    if not access_token:
        print("Missing access token from Bashhub Config")
    return ""


BH_SAVE_COMMANDS = os.getenv('BH_SAVE_COMMANDS', \
    get_from_config('save_commands')).lower() in ('true', 'yes', 't', 'on', '')

BH_SYSTEM_NAME = get_from_config("system_name")


# Get our token from the environment if one is present
# otherwise retrieve it from our config. Needs to
# be a function since we may change our token during setup
def BH_AUTH():
    return os.getenv('BH_ACCESS_TOKEN', get_from_config("access_token"))


def is_valid_regex(regex):
    try:
        re.compile(regex)
        return True
    except re.error:
        return False

BH_FILTER = os.getenv('BH_FILTER', '') if is_valid_regex(os.getenv('BH_FILTER', '')) \
        else '__invalid__'
