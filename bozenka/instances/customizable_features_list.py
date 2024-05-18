import bozenka.features.admin
from bozenka.features import *
from bozenka.features.admin import *

customizable_features = [
    # Admin related category
    Moderation,
    Invite,
    Pins,
    Threads,
    ChatInformation,
    # User related category
    Welcome,
    AiFeature
]

text_transcription = {
    "user": "Пользователи 👤",
    "admin": "Администраторы 👮‍♂"
}

categorized_customizable_features = {}

for feature in customizable_features:
    if feature.telegram_setting_in_list:
        if feature.telegram_category in categorized_customizable_features.keys():
            categorized_customizable_features[feature.telegram_category].append(feature)
        else:
            categorized_customizable_features[feature.telegram_category] = [feature]
