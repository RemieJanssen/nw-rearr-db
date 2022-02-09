"""
Django production/staging settings for nw_rearr_db project.
"""

from pathlib import Path
from .basesettings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "136.144.254.62",
    "phylofun.remiejanssen.nl",
]
