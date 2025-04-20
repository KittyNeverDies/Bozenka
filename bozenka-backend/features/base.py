class BasicFeature:
    """
    A basic class for all features of bozenka platform.
    There is described the structure of information, stored in classes of features.
    Don't touch it unless you know what you're doing.
    """


    settings_name = "Example name of setting"
    settings_description = "Example description of setting"

    settings_options = [
        # How does this work?
        # 'name' - Name of settings, used in API
        # 'displayName' - Name, which will be displayed at user's dashboard
        # 'type' - What value does it store (Can be text, choice or bool)
        # 'description' - Description of setting, displayed on dashboard
        # 'default' - Default value, what will be used for setting
        {
            "name": "1234",
            "displayName": "How it works?",
            "type": "bool", # Choice, text, or bool
            "description": "Example",
            "default": False,
            "choices": [True, False],
        }
    ]

    platforms_available: dict[str: list | str | dict] = {
        "telegram": {
            'commands_hints': {
                # There stored all command hints of telegram version
                # Format is  "CommandNameHere": "Command description is here"
                "example": "Its an example"
            },
            'handlers': {
                #  Format is [Handler, [Filters]]
                'callback_query': [],  # Handlers for callback queries
                'message': [],         # Handlers for messages
                'channel_post': [],    # Handlers for channel posts
                'edited_channel_post': [], # Handlers for edited channel posts
                'poll': [],           # Handlers for polls
                'chat_join_request': [],      # Handlers for chat joins request
                'chat_boost': [],     # Handlers for chat boosts
            }
        },
        "discord": {
            'handlers': {
                #  Format is [Handler, {'name': 'example', 'description': 'It is an example'}]
            }
        },
        "vkontakte": {
            # In development right now
            'handlers': {
                #  Format is [Handler, [Filters]]
            }
        }
    }



