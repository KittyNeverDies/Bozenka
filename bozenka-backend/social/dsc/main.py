import discord
import asyncio
import inspect
import os # default module


def static_to_coroutine(func):
    """
    Converts a static method (or a regular function) into a coroutine function, what
    we need to register.
    :param func: Function to convert
    :return: Coroutine function
    :raise TypeError: If func is not a static method or a regular function
    """
    import functools

    if not callable(func):
        raise TypeError("Input must be a callable (function or method).")

    if asyncio.iscoroutinefunction(func) or inspect.isasyncgenfunction(func):
        return func

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper



async def launch_discord_bot_instance(features: dict[str: list]) -> None:
    """
    Launches discord bot instance for bozenka platform
    :param features: List of features, that instance should have to register
    :return: Nothing
    """

    # Initializing discord bot
    bot = discord.Bot()

    # Initializing all slash commands, written for discord
    # in features of platform
    for list_of_features in features.values():
        for feature in list_of_features:
            if not feature.platforms_available.get('discord'):
                continue
            for command in feature.platforms_available['discord']['handlers']:
                print(asyncio.iscoroutinefunction(command))
                print(command[0])
                bot.add_application_command(
                    discord.SlashCommand(
                        func=static_to_coroutine(command[0]),
                        name=command[1]['name'],
                        description=command[1]['description'],
                    )
                )

    # Starting the bot
    await bot.start(os.getenv('DISCORD_TOKEN'))
