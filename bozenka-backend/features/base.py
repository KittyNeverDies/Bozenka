class BasicFeature:
    """
    A basic class for all features of bozenka platform.
    There is described the structure of information, stored in classes of features.
    Don't touch it unless you know what you're doing.
    """


    settings_name = "Example name of setting"
    settings_description = "Example description of setting"
    setting_database_row = None

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



