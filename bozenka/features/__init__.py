

class BasicFeature:
    """
    A classic class of lineral (basic)
    feature of bozenka. IN FUTURE!
    """
    telegram_setting_in_list = False   # Does feature shows in /setup list
    telegram_setting_name = None       # Setting title in /setup command
    telegram_setting_description = None    # Setting description in /setup command
    telegram_db_name = None                # Name of TelegramChatSettings column will be affected
    # Telegram commands list of feature
    telegram_commands: dict[str: str] = {
            #
            # Format is  "CommandNameHere": "Command description is here"
            #
            "example": "Its an example"
    }
    telegram_cmd_avaible = True  # Does this feature have a telegram commands
    # All handlers
    telegram_message_handlers = [
            #  Format is [Handler, [Filters]]
    ]
    telegram_callback_handlers = [
            #  Format is [Handler, [Filters]]
    ]
