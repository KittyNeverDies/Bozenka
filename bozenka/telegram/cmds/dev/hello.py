from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Message as Message, User, Chat
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.telegram.utils.simpler import ru_cmds


async def hi(msg: Message):
    """
    Test command, sending welcome message.
    Made for testing bot working status.
    :param msg:
    :return:
    """
    await msg.answer(
        ru_cmds["hi"].replace("user", msg.from_user.mention_html(ru_cmds["user"])))


async def testing(msg: Message, session_maker: async_sessionmaker, command: CommandObject, user: User, target: User, chat: Chat, bot: Bot):
    print(user.full_name)
    print(target.full_name)
    print(msg)
    print(command.args)
    print(command.mention)
    print(command.command)
