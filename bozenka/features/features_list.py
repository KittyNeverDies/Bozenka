from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand

from bozenka.features import BasicFeature
from bozenka.features.admin import *
from bozenka.features.user import *
from bozenka.features.basic import *

features_list = [
    # Admin related category
    Moderation,
    Invite,
    Pins,
    Threads,
    # User related category
    ImageGeneratrion,
    TextGeneratrion,
    Welcome,
    # Basic Functions
    Setup,
    Start
]



