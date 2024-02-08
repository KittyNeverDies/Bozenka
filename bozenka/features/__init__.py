

class BasicFeature:
    """
    A classic class of lineral (basic)
    feature of bozenka. IN FUTURE!
    """
    def __init__(self):
        """
        All information about feature
        will be inside this function
        """

        # Telegram setting info
        self.telegram_setting_in_list = False   # Does feature shows in /setup list
        self.telegram_setting_name = None       # Setting title in /setup command
        self.telegram_setting_description = None    # Setting description in /setup command
        self.telegram_db_name = None                # Name of TelegramChatSettings column will be affected
        # Telegram commands list of feature
        self.telegram_commands: dict[str: str] = {
            #
            # Format is  "CommandNameHere": "Command description is here"
            #
            "example": "Its an example"
        }
        self.telegram_cmd_avaible = True  # Does this feature have a telegram commands
        # All handlers
        self.telegram_message_handlers = (
            #  Format is [Handler, [Filters]]
        )
        self.telegram_callback_handlers = (
            #  Format is [Handler, [Filters]]
        )