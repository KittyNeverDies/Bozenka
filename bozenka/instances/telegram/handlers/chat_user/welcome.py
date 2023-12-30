import logging

from aiogram import Bot
from aiogram.types import Message as Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.instances.telegram.utils.simpler import SolutionSimpler


async def join(msg: Message, session_maker: async_sessionmaker):
    """
    Send welcome message, after adding new member to chat.
    Also works on adding bot to chat and sending welcome message.
    :param msg:
    :param session_maker:
    :return:
    """
    for new in msg.new_chat_members:
        if new.id != msg.bot.id:
            logging.log(msg=f"Saing welcome for user_id={new.id}, chat_id={msg.chat.id}",
                        level=logging.INFO)
            await msg.answer(
                f"Пользователь {new.mention_html()} переехал в конфу, благодаря {msg.from_user.mention_html()}👋",
            )
            await msg.delete()
        else:
            logging.log(msg=f"Saing welcome to administrators for chat_id={msg.chat.id}",
                        level=logging.INFO)
            await msg.answer("Здраствуйте администраторы чата 👋\n"
                             "Я - <b>бозенька</b>, мультифункциональный бот, разрабатываемый Bozo Developement\n"
                             "Выдайте мне <b>полные права администратора</b> для моей полной работы.\n"
                             "Чтобы настроить функционал, используйте /setup или кнопку под сообщением", )
            await SolutionSimpler.auto_settings(msg=msg, session=session_maker)


async def leave(msg: Message, bot: Bot):
    """
    Sens goodbye message, after deleting member from chat
    :param msg:
    :param bot:
    :return:
    """
    await msg.delete()
    if msg.from_user.id == bot.id:
        return
    logging.log(msg=f"Saing goodbye for user_id={msg.left_chat_member.id}, chat_id={msg.chat.id}",
                level=logging.INFO)
    await msg.answer(
        f"Пользователь {msg.left_chat_member.mention_html()} съехал с конфы, благодаря {msg.from_user.mention_html()}👋"
    )
