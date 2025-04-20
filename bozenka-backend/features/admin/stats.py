
from features.base import BasicFeature


class TestFeature(BasicFeature):
    """
    Test feature implementation, shows what
    features autoregistration is working
    """


    async def vk_hi_handler(message):
        await message.answer("Hello 👋")

    @staticmethod
    async def tg_echo_handler(message) -> None:
        """
        Handler will forward receive a message back to the sender
        By default, message handler will handle all message types (like a text, photo, sticker etc.)
        """
        try:
            # Send a copy of the received message
            await message.send_copy(chat_id=message.chat.id)
        except TypeError:
            # But not all the types is supported to be copied so need to handle it
            await message.answer("Nice try!")
    
    async def dsc_hello_handler(ctx):
        await ctx.respond("Hey!")


    platforms_available: dict[str: list | str | dict] = {
        "telegram": {
            'handlers': {
                #  Format is [Handler, [Filters]]
                'callback_query': [],  # Handlers for callback queries
                'message': [
                    [tg_echo_handler, []]
                ],  # Handlers for messages
            }
        },
        "discord": {
            'handlers': [
                #  Format is [Handler, {'name': 'example', 'description': 'It is an example'}]
                [dsc_hello_handler, {'name': 'hello', 'description': 'Hello world!'}]
            ]
        },
        "vkontakte": {
            # In development right now
            'handlers': {
                #  Format is [Handler, [Filters]]
                'private_message': [
                    [vk_hi_handler, []]
                ]
            }
        }

    }

