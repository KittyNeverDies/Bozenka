from bozenka.features import *

features_list = [
    # Admin related category
    Moderation,
    Invite,
    Pins,
    Threads,
    ChatInformation,
    # User related category
    ImageGeneratrion,
    TextGeneratrion,
    Welcome,
    # Basic Functions
    Setup,
    Start
]

customizable_features = {}

for feature in features_list:
    if feature.telegram_setting_in_list:
        if feature.telegram_category in customizable_features.keys():
            customizable_features[feature.telegram_category].append(feature)
        else:
            customizable_features[feature.telegram_category] = [feature]
