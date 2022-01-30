"""
Django development settings for nw_rearr_db project.
"""

from pathlib import Path
from .basesettings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]
