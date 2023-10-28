import logging

from aiogram import Bot
from aiogram.types import Message as Message
from bozenka.telegram.utils.simpler import ru_cmds


async def join(msg: Message):
    """
    Send welcome message, after adding new member to chat.
    Also works on adding bot to chat and sending welcome message.
    :param msg:
    :return:
    """
    for new in msg.new_chat_members:
        if new.id != msg.bot.id:
            logging.log(msg=f"Saing welcome for user_id={new.id}, chat_id={msg.chat.id}",
                        level=logging.INFO)
            await msg.answer(
                    f"Пользователь {new.mention_html()} переехал в конфу, благодаря {msg.from_user.mention_html()}👋",
            )
        else:
            logging.log(msg=f"Saing welcome to administrators for chat_id={msg.chat.id}",
                        level=logging.INFO)
            await msg.answer(ru_cmds["after_adding"])
    await msg.delete()


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

