class BasicFeature:
    """
    A classic class of lineral (basic)
    feature of bozenka. IN FUTURE!
    :param  telegram_setting_in_list: Does feature shows in /setup list
    """
    telegram_setting_in_list: bool = False              # Does feature shows in /setup list
    telegram_setting_name: str | None = None            # Setting title in /setup command
    telegram_setting_description: str | None = None     # Setting description in /setup command
    telegram_db_name = None                             # Name of TelegramChatSettings column will be affected
    telegram_category: str | None = None                # Telegram category name, current
    # Telegram commands list of feature
    telegram_commands: dict[str: str] = {
            #
            # Format is  "CommandNameHere": "Command description is here"
            #
            "example": "Its an example"
    }
    telegram_cmd_avaible = True  # Does this feature have a telegram commands

    # All handlers to register automaticly by bozenka
    telegram_message_handlers = [
            #  Format is [Handler, [Filters]]
    ]
    telegram_callback_handlers = [
            #  Format is [Handler, [Filters]]
    ]
