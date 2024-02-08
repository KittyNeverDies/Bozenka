from aiogram import Dispatcher

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


def register_all_features(features_list: list[BasicFeature], dispatcher: Dispatcher) -> None:
    """
    Registers all features / handlers avaible in bozenka
    :param features_list: List of features
    :return: None
    """
    pass
