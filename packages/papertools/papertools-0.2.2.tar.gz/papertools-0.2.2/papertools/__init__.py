"""
PaperTools
~~~~~~
A module which offers tons of usefull features for discord.py bots.

Copyright (c) 2023, aiokev

Licensed under GPL-3.0
"""

import discord as discordpy

if not discordpy.version_info.major >= 2:

    class DiscordPyOutdated(Exception):
        pass

    raise DiscordPyOutdated(
        "You must have discord.py (v2.0 or greater) to use this library. "
        "Uninstall your current version and install discord.py 2.0 "
        "using 'pip install discord.py'",
    )

__version__ = "0.2.2"
__title__ = "papertools"
__author__ = "aiokev"
__license__ = "GPL-3.0"
__copyright__ = "Copyright (c) 2023, aiokev"

from .num_methods import *
from .timetools import *
from .paginator import *
from .gittools import *
from .discord import *
