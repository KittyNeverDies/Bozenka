import logging

from aiogram import F
from aiogram.enums import ChatMemberStatus, ChatType
from aiogram.filters import CommandObject, Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import async_sessionmaker

from bozenka.database.tables.telegram import get_chat_config_value, TelegramChatSettings
from bozenka.features import BasicFeature
from bozenka.instances.telegram.utils.callbacks_factory import UnbanData, BanData, UnmuteData, MuteData
from bozenka.instances.telegram.utils.filters import IsAdminFilter, BotHasPermissions, UserHasPermissions
from bozenka.instances.telegram.utils.keyboards import ban_keyboard, delete_keyboard, mute_keyboard, unmute_keyboard, \
    unban_keyboard
from bozenka.instances.telegram.utils.simpler import list_of_features, SolutionSimpler


class Moderation(BasicFeature):
    """
    A class of moderation related feature
    All staff related to it will be here
    """

    async def telegram_ban_callback_handler(call: CallbackQuery, callback_data: BanData,
                                            session_maker: async_sessionmaker) -> None:
        """
        CallbackQuery handler, what bannes users after callback
        :param call: CallBackQuery telegram object
        :param callback_data: BanData object
        :param session_maker: AsyncSessionmaker object
        :return: None
        """
        clicked_user = await call.message.chat.get_member(call.from_user.id)
        banned_user = await call.message.chat.get_member(int(callback_data.user_id_ban))

        send_notification = await get_chat_config_value(chat_id=call.message.chat.id, session=session_maker,
                                                        setting=list_of_features["Admins"][5])

        if call.from_user.id != callback_data.user_id_clicked \
                and clicked_user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            return
        await SolutionSimpler.inline_ban_user(call=call, data=callback_data, session=session_maker)

        if not banned_user.is_member and banned_user.status == ChatMemberStatus.KICKED:
            await call.answer("Уже заблокирован ✅")
        else:
            await call.answer("Успешно заблокирован ✅")

        await call.message.edit_text(
            "Удача ✅\n"
            f"{banned_user.user.mention_html('Этот пользователь')} был заблокирован {call.from_user.mention_html('этим пользователем')}.",
            reply_markup=ban_keyboard(admin_id=call.from_user.id, ban_id=banned_user.user.id)
        )

        if send_notification:
            await call.message.bot.send_message(
                chat_id=banned_user.user.id,
                text=f"{banned_user.user.mention_html('Вы')} были заблокированы {call.from_user.mention_html('этим пользователем')} в чате <code>{call.message.chat.id}</code>.",
                reply_markup=delete_keyboard(admin_id=banned_user.user.id)
            )

        logging.log(msg=f"Banned user @{banned_user.user.full_name} user_id=f{banned_user.user.id}", level=logging.INFO)

    async def telegram_unban_callback_handler(call: CallbackQuery, callback_data: UnbanData,
                                              session_maker: async_sessionmaker) -> None:
        """
        CallbackQuery handler, what unbannes users after callback
         :param call: CallBackQuery telegram object
        :param callback_data: UnbanData object
        :param session_maker: AsyncSessionmaker object
        :return: None
        """
        clicked_user = await call.message.chat.get_member(call.from_user.id)
        unbanned_user = await call.message.chat.get_member(int(callback_data.user_id_unban))

        if call.from_user.id != callback_data.user_id_clicked \
                and clicked_user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            return

        await SolutionSimpler.inline_unban_user(call=call, data=callback_data, session=session_maker)

        if unbanned_user.is_member and unbanned_user.status != ChatMemberStatus.KICKED:
            await call.answer("Уже разблокирован ✅")
        else:
            await call.answer("Успешно разблокирован ✅")
        await call.message.edit_text(
            "Удача ✅\n"
            f"{unbanned_user.user.mention_html('Этот пользователь')} был разблокирован {call.from_user.mention_html('этим пользователем')}.",
            reply_markup=unban_keyboard(admin_id=call.from_user.id, ban_id=unbanned_user.user.id)
        )

        if await get_chat_config_value(chat_id=call.message.chat.id, session=session_maker,
                                       setting=list_of_features["Admins"][5]):
            await call.message.bot.send_message(
                chat_id=unbanned_user.user.id,
                text=f"{unbanned_user.user.mention_html('Вы')} были разблокирован {call.from_user.mention_html('этим пользователем')} в чате <code>{call.message.chat.id}</code>.",
                reply_markup=delete_keyboard(admin_id=unbanned_user.user.id)
            )

        logging.log(msg=f"Unbanned user @{unbanned_user.user.full_name} user_id=f{unbanned_user.user.id}",
                    level=logging.INFO)

    async def telegram_ban_cmd_handler(msg: Message, command: CommandObject, session_maker: async_sessionmaker) -> None:
        """
        /ban command function, supports time and reasons.
        :param msg: Message telegram object
        :param command: Object of telegram command
        :param session_maker: Session maker object of SqlAlchemy
        :return: Nothing
        """
        banned_user = await msg.chat.get_member(msg.reply_to_message.from_user.id)
        send_to_dm = await get_chat_config_value(chat_id=msg.chat.id, session=session_maker,
                                                 setting=list_of_features["Admins"][4])
        send_notification = await get_chat_config_value(chat_id=msg.chat.id, session=session_maker,
                                                        setting=list_of_features["Admins"][5])

        where_send = {
            True: msg.from_user.id,
            False: msg.chat.id
        }

        if banned_user.status == ChatMemberStatus.KICKED:
            await msg.bot.send_message(chat_id=where_send[send_to_dm],
                                       text="Ошибка ❌\n"
                                            "Этот пользователь уже удален из группы",
                                       reply_markup=delete_keyboard(msg.from_user.id))
            return

        config = await SolutionSimpler.ban_user(msg, command, session_maker)
        if config["reason"] and config["ban_time"]:
            await msg.bot.send_message(chat_id=where_send[send_to_dm],
                                       text="Удача ✅\n"
                                            f"{msg.reply_to_message.from_user.mention_html('Этот пользователь')} "
                                            f"был заблокирован {msg.from_user.mention_html('этим пользователем')}.\n"
                                            f"По причине <code>{config['reason']}</code>, до даты <code>{config['ban_time']}</code>",
                                       reply_markup=ban_keyboard(msg.from_user.id, msg.reply_to_message.from_user.id))
            if send_notification:
                await msg.bot.send_message(chat_id=banned_user.user.id,
                                           text="Вы "
                                                f"были заблокированы {msg.from_user.mention_html('этим пользователем')} в чате <code>{msg.chat.title}</code>.\n"
                                                f"По причине <code>{config['reason']}, до даты <code>{config['ban_time']}</code>",
                                           reply_markup=delete_keyboard(admin_id=banned_user.user.id))
        elif config["reason"]:
            await msg.bot.send_message(chat_id=where_send[send_to_dm],
                                       text="Удача ✅\n"
                                            f"{msg.reply_to_message.from_user.mention_html('Этот пользователь')} "
                                            f"был заблокирован {msg.reply_to_message.from_user.mention_html('этим пользователем')}.\n"
                                            f"По причине <code>{config['reason']}</code>.",
                                       reply_markup=ban_keyboard(admin_id=msg.from_user.id,
                                                                 ban_id=msg.reply_to_message.from_user.id))
            if send_notification:
                await msg.bot.send_message(chat_id=banned_user.user.id,
                                           text=f"Вы "
                                                f"были заблокированы {msg.from_user.mention_html('этим пользователем')} в чате <code>{msg.chat.title}</code>.\n"
                                                f"По причине <code>{config['reason']}</code>.",
                                           reply_markup=delete_keyboard(admin_id=banned_user.user.id))
        elif config["ban_time"]:
            await msg.bot.send_message(chat_id=where_send[send_to_dm],
                                       text="Удача ✅\n"
                                            f"{msg.reply_to_message.from_user.mention_html('Этот пользователь')} "
                                            f"был заблокирован {msg.from_user.mention_html('этим пользователем')}, до даты <code>{config['ban_time']}</code>",
                                       reply_markup=ban_keyboard(admin_id=msg.from_user.id,
                                                                 ban_id=msg.reply_to_message.from_user.id))
            if send_notification:
                await msg.bot.send_message(chat_id=banned_user.user.id,
                                           text=f"Вы "
                                                f"были заблокированы {msg.from_user.mention_html('этим пользователем')} в чате <code>{msg.chat.title}</code>.\n"
                                                f"До даты <code>{config['ban_time']}</code>.",
                                           reply_markup=delete_keyboard(admin_id=banned_user.user.id))
        else:
            await msg.bot.send_message(chat_id=where_send[send_to_dm],
                                       text="Удача ✅\n"
                                            f"{msg.reply_to_message.from_user.mention_html('Этот пользователь')}"
                                            f" был заблокирован {msg.from_user.mention_html('этим пользователем')}.",
                                       reply_markup=ban_keyboard(msg.from_user.id, msg.reply_to_message.from_user.id))
            if send_notification:
                await msg.bot.send_message(chat_id=banned_user.user.id,
                                           text=f"Вы "
                                                f"были заблокированы {msg.from_user.mention_html('этим пользователем')} в чате "
                                                f"<code>{msg.chat.title}</code>.\n",
                                           reply_markup=delete_keyboard(admin_id=banned_user.user.id))

    async def telegram_unban_cmd_handler(msg: Message, command: CommandObject,
                                         session_maker: async_sessionmaker) -> None:
        """
        /unban command function
        :param msg: Message telegram object
        :param command: Object of telegram command
        :param session_maker: Session maker object of SqlAlchemy
        """
        await SolutionSimpler.unban_user(msg, session_maker)

        unbanned_user = await msg.chat.get_member(msg.reply_to_message.from_user.id)
        send_to_dm = await get_chat_config_value(chat_id=msg.chat.id, session=session_maker,
                                                 setting=list_of_features["Admins"][4])
        send_notification = await get_chat_config_value(chat_id=msg.chat.id, session=session_maker,
                                                        setting=list_of_features["Admins"][5])

        where_send = {
            True: msg.from_user.id,
            False: msg.chat.id
        }

        if unbanned_user.is_member and unbanned_user.status != ChatMemberStatus.KICKED:
            await msg.bot.send_message(
                chat_id=where_send[send_to_dm],
                text="Ошибка ❌\n"
                     "Этот пользователь не находится в бане.",
                reply_markup=delete_keyboard(admin_id=msg.from_user.id)
            )
            return
        elif not command.text:
            await msg.bot.send_message(
                chat_id=where_send[send_to_dm],
                text="Удача ✅\n"
                     f"{msg.reply_to_message.from_user.mention_html('Этот пользователь')} был разблокирован "
                     f"{msg.from_user.mention_html('этим пользователем')}.\n",
                reply_markup=unban_keyboard(admin_id=msg.from_user.id, ban_id=msg.reply_to_message.from_user.id)
            )
            if send_notification:
                await msg.bot.send_message(
                    chat_id=unbanned_user.user.id,
                    text=f"{msg.reply_to_message.from_user.mention_html('Вы')} "
                         f"был разблокированы {msg.from_user.mention_html('этим пользователем')} в чате <code>{msg.chat.title}</code>.\n",
                    reply_markup=delete_keyboard(admin_id=unbanned_user.user.id)
                )
        else:
            await msg.bot.send_message(
                chat_id=where_send[send_to_dm],
                text="Удача ✅\n"
                     f"Пользователь {msg.reply_to_message.from_user.mention_html()} был разблокирован пользователем {msg.from_user.mention_html()}.\n"
                     f"По причине {CommandObject.text}.",
                reply_markup=delete_keyboard(admin_id=unbanned_user.user.id)
            )
            if send_notification:
                await msg.bot.send_message(
                    chat_id=unbanned_user.user.id,
                    text=f"{msg.reply_to_message.from_user.mention_html('Вы')} "
                         f"был разблокированы {msg.from_user.mention_html('этим пользователем')} в чате <code>{msg.chat.title}</code>.\n"
                         f"По причине <code>{CommandObject.text}</code>",
                    reply_markup=delete_keyboard(admin_id=unbanned_user.user.id)
                )

    async def telegram_mute_callback_handler(call: CallbackQuery, callback_data: MuteData,
                                             session_maker: async_sessionmaker) -> None:
        """
        Query, what mutes users after callback
        :param call: CallBackQuery telegram object
        :param callback_data: BanData object
        :param session_maker: AsyncSessionmaker object
        :return:
        """
        clicked_user = await call.message.chat.get_member(call.from_user.id)
        muted_user = await call.message.chat.get_member(int(callback_data.user_id_mute))

        if call.from_user.id != callback_data.user_id_clicked \
                and clicked_user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            return
        await SolutionSimpler.inline_mute_user(call=call, data=callback_data, session=session_maker)

        if not muted_user.can_send_messages and muted_user.status == ChatMemberStatus.RESTRICTED:
            await call.answer("Уже замучен ✅")
        else:
            await call.answer("Успешно замучен ✅")

        await call.message.edit_text(
            "Удача ✅\n"
            f"{muted_user.user.mention_html('Этот пользователь')} был замучен {call.from_user.mention_html('этим пользователем')}.",
            reply_markup=mute_keyboard(admin_id=call.from_user.id, mute_id=callback_data.user_id_mute)
        )

        send_notification = await get_chat_config_value(chat_id=call.message.chat.id, session=session_maker,
                                                        setting=list_of_features["Admin"][5])
        if send_notification:
            await call.message.bot.send_message(
                chat_id=muted_user.user.id,
                text=f"{muted_user.user.mention_html('Вы')} были замучены {call.from_user.mention_html('этим пользователем')} в чате <code>{call.message.chat.id}</code>.",
                reply_markup=delete_keyboard(admin_id=muted_user.user.id)
            )

        logging.log(msg=f"Muted user @{muted_user.user.full_name} user_id=f{muted_user.user.id}", level=logging.INFO)

    async def telegram_unmute_callback_handler(call: CallbackQuery, callback_data: UnmuteData,
                                               session_maker: async_sessionmaker) -> None:
        """
        Query, what unbannes users after callback
        :param call: CallBackQuery telegram object
        :param callback_data: UnbanData object
        :param session_maker: AsyncSessionmaker object
        :return:
        """
        clicked_user = await call.message.chat.get_member(call.from_user.id)
        unmuted_user = await call.message.chat.get_member(int(callback_data.user_id_unmute))
        if call.from_user.id != callback_data.user_id_clicked \
                and clicked_user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            return

        await SolutionSimpler.inline_unmute_user(call=call, data=callback_data, session=session_maker)

        if unmuted_user.can_send_messages or unmuted_user.status == ChatMemberStatus.RESTRICTED:
            await call.answer("Уже размучен ✅")
        else:
            await call.answer("Успешно размучен ✅")
        await call.message.edit_text(
            "Удача ✅\n"
            f"{unmuted_user.user.mention_html('Этот пользователь')} был размучен {call.from_user.mention_html('этим пользователем')}.",
            reply_markup=unmute_keyboard(admin_id=call.from_user.id, unmute_id=unmuted_user.user.id)
        )

        send_notification = await get_chat_config_value(chat_id=call.message.chat.id, session=session_maker,
                                                        setting=list_of_features["Admin"][5])
        if send_notification:
            await call.message.bot.send_message(
                chat_id=unmuted_user.user.id,
                text=f"{unmuted_user.user.mention_html('Вы')} были размучены {call.from_user.mention_html('этим пользователем')} в чате <code>{call.message.chat.id}</code>.",
                reply_markup=delete_keyboard(admin_id=unmuted_user.user.id)
            )

        logging.log(msg=f"Unbanned user @{unmuted_user.user.full_name} user_id=f{unmuted_user.user.id}",
                    level=logging.INFO)

    async def telegram_mute_cmd_handler(msg: Message, command: CommandObject,
                                        session_maker: async_sessionmaker) -> None:
        """
        Handler of command /mute
        Restricts member from using chat
        :param msg: Message telegram object
        :param command: Object of telegram command
        :param session_maker: Session maker object of SqlAlchemy
        :return: Nothing
        """
        print(msg.reply_to_message)
        print("341414124")
        mute_user = await msg.chat.get_member(msg.reply_to_message.from_user.id)

        send_to_dm = await get_chat_config_value(chat_id=msg.chat.id, session=session_maker,
                                                 setting=list_of_features["Admins"][4])
        send_notification = await get_chat_config_value(chat_id=msg.chat.id, session=session_maker,
                                                        setting=list_of_features["Admins"][5])

        where_send = {
            True: msg.from_user.id,
            False: msg.chat.id
        }

        if mute_user.status == ChatMemberStatus.LEFT or mute_user.status == ChatMemberStatus.KICKED:
            return
        config = await SolutionSimpler.mute_user(msg, command, session_maker)
        if config["mute_time"] and config["reason"] != "":
            await msg.bot.send_message(
                chat_id=where_send[send_to_dm],
                text="Удача ✅\n"
                     f"{msg.from_user.mention_html('Этот пользователь')} запретил писать "
                     f"сообщения {msg.reply_to_message.from_user.mention_html('этому пользователю')}.\n"
                     f"По причине <code>{config['reason']}</code>, до даты <code>{config['mute_time']}</code>",
                reply_markup=mute_keyboard(msg.from_user.id, mute_user.user.id))
            if send_notification:
                await msg.bot.send_message(
                    chat_id=mute_user.user.id,
                    text=f"{msg.from_user.mention_html('Этот пользователь')} запретил писать "
                         f"сообщения {msg.reply_to_message.from_user.mention_html('вам')} в чате {msg.chat.title}.\n"
                         f"По причине <code>{config['reason']}</code>, до даты <code>{config['mute_time']}</code>",
                    reply_markup=delete_keyboard(admin_id=mute_user.user.id))

        elif config["reason"] != "":
            await msg.bot.send_message(
                chat_id=where_send[send_to_dm],
                text="Удача ✅\n"
                     f"{msg.from_user.mention_html('Этот пользователь')} запретил писать "
                     f"сообщения {msg.reply_to_message.from_user.mention_html('этому пользователю')}.\n"
                     f"По причине <code>{config['reason']}</code>.",
                reply_markup=mute_keyboard(msg.from_user.id, mute_user.user.id))
            if send_notification:
                await msg.bot.send_message(
                    chat_id=mute_user.user.id,
                    text=f"{msg.from_user.mention_html('Этот пользователь')} запретил писать "
                         f"сообщения {msg.reply_to_message.from_user.mention_html('вам')} в чате {msg.chat.title}.\n"
                         f"По причине <code>{config['reason']}</code>.",
                    reply_markup=delete_keyboard(admin_id=mute_user.user.id))
        elif config["mute_time"]:
            await msg.bot.send_message(
                chat_id=where_send[send_to_dm],
                text="Удача ✅\n"
                     f"{msg.from_user.mention_html('Этот пользователь')} запретил писать "
                     f"сообщения {msg.reply_to_message.from_user.mention_html('этому пользователю')}.\n"
                     f"До даты <code>{config['mute_time']}</code>",
                reply_markup=mute_keyboard(msg.from_user.id, mute_user.user.id))
            if send_notification:
                await msg.bot.send_message(
                    chat_id=mute_user.user.id,
                    text=f"{msg.from_user.mention_html('Этот пользователь')} запретил писать "
                         f"сообщения {msg.reply_to_message.from_user.mention_html('вам')} в чате {msg.chat.title}.\n"
                         f"До даты <code>{config['mute_time']}</code>",
                    reply_markup=delete_keyboard(admin_id=mute_user.user.id))
        else:
            await msg.bot.send_message(
                chat_id=where_send[send_to_dm],
                text="Удача ✅\n"
                     f"{msg.from_user.mention_html('Этот пользователь')} запретил писать "
                     f"сообщения {msg.reply_to_message.from_user.mention_html('этому пользователю')}.\n",
                reply_markup=mute_keyboard(msg.from_user.id, mute_user.user.id))
            if send_notification:
                await msg.bot.send_message(
                    chat_id=mute_user.user.id,
                    text=f"{msg.from_user.mention_html('Этот пользователь')} запретил писать "
                         f"сообщения {msg.reply_to_message.from_user.mention_html('вам')} в чате {msg.chat.title}.\n",
                    reply_markup=delete_keyboard(admin_id=mute_user.user.id))

    async def telegram_unmute_cmd_handler(msg: Message, session_maker: async_sessionmaker) -> None:
        """
        Handler of command /unmute
        Gives access member to send messages into chat
        :param msg: Message telegram object
        :param session_maker: Session maker object of SqlAlchemy
        :return: Nothing
        """
        await SolutionSimpler.unmute_user(msg, session_maker)

        send_to_dm = await get_chat_config_value(chat_id=msg.chat.id, session=session_maker,
                                                 setting=list_of_features["Admins"][4])
        send_notification = await get_chat_config_value(chat_id=msg.chat.id, session=session_maker,
                                                        setting=list_of_features["Admins"][5])

        where_send = {
            True: msg.from_user.id,
            False: msg.chat.id
        }

        await msg.bot.send_message(
            user_id=where_send[send_to_dm],
            text="Удача ✅"
                 f"{msg.from_user.mention_html('Этот пользователь')} разрешил писать\n"
                 f"сообщения {msg.reply_to_message.from_user.mention_html('этому пользователю')}",
            reply_markup=unmute_keyboard(msg.from_user.id, msg.reply_to_message.from_user.id))
        if send_notification:
            await msg.bot.send_message(
                user_id=msg.reply_to_message.from_user.id,
                text=f"{msg.from_user.mention_html('Этот пользователь')} разрешил писать\n"
                     f"сообщения {msg.reply_to_message.from_user.mention_html('вам')}",
                reply_markup=delete_keyboard(admin_id=msg.reply_to_message.from_user.id))

    # Help moderation telegram
    # Code part
    async def telegram_help_ban_handler(msg: Message) -> None:
        """
        Shows help message for /ban
        :param msg: Message telegram object
        :return: Nothing
        """
        await msg.answer("Использование:\n"
                         "<pre>/ban [время блокировки] [причина блокировки]</pre>\n"
                         "Ответьте на сообщение, чтобы заблокировать пользователя",
                         reply_markup=delete_keyboard(msg.from_user.id))

    async def telegram_help_unban_handler(msg: Message) -> None:
        """
        Shows help message for /unban
        :param msg: Message telegram object
        :return: Nothing
        """
        await msg.answer("Использование:\n"
                         "<pre>/unban</pre>\n"
                         "Ответьте на сообщение, чтобы разблокировать пользователя",
                         reply_markup=delete_keyboard(msg.from_user.id))

    async def telegram_help_mute_handler(msg: Message) -> None:
        """
        Shows help message for /mute
        :param msg: Message telegram object
        :return: Nothing
        """
        await msg.answer("Использование:\n"
                         "<pre>/mute [время мута] [причина мута]</pre>\n"
                         "Ответьте на сообщение, чтобы замутить пользователя",
                         reply_markup=delete_keyboard(msg.from_user.id))

    async def telegram_help_unmute_handler(msg: Message) -> None:
        """
        Shows help message for /unmute
        :param msg: Message telegram object
        :return: Nothing
        """
        await msg.answer("Использование:\n"
                         "<pre>/unmute</pre>\n"
                         "Ответьте на сообщение, чтобы замутить пользователя",
                         reply_markup=delete_keyboard(msg.from_user.id))

    telegram_setting_in_list = True
    telegram_setting_name = "Модерация чата 🕵️"
    telegram_setting_description = "<b>Модерация чата</b>🕵️\nДанная настройка включает следущие комманды:" \
                                   "\n<pre>/ban [время блокировки] [причина блокировки] - блокировка пользователя" \
                                   "\n/unban - разблокировка пользователя\n" \
                                   "/mute [время мута] [причина мута] - мут пользователя\n" \
                                   "/unmute - Размут пользователя</pre>\n" \
                                   "Время обозначается как:" \
                                   "<pre>1h - один час, " \
                                   "1d - один день, " \
                                   "1m - одна минута, " \
                                   "1s - одна секунда</pre>\n" \
                                   "Для того, " \
                                   "чтобы выполнить одну из комманд по отношению к пользователю, " \
                                   "ответьте на сообщение пользователя и используйте команду\n" \
                                   "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота.</b>"

    telegram_db_name = TelegramChatSettings.moderation
    # Telegram commands
    telegram_commands: dict[str: str] = {
        "ban": "Command to ban user in chat",
        "unban": "Command to unban user in chat",
        "mute": "Command to mute user in chat",
        "unmute": "Command to unmute user in chat",
    }
    telegram_cmd_avaible = True  # Is a feature have a commands
    # All handlers
    telegram_message_handlers = [
        #  Format is [Handler, [Filters]]
        [telegram_ban_cmd_handler, [Command(commands="ban"),
                                    IsAdminFilter(True, True), F.reply_to_message.text,
                                    ~(F.chat.type == ChatType.PRIVATE)]],
        [telegram_unban_cmd_handler, [Command(commands="unban"),
                                      IsAdminFilter(True, True), F.reply_to_message.text,
                                      ~(F.chat.type == ChatType.PRIVATE)]],
        [telegram_mute_cmd_handler, [Command(commands=["mute", "re"]),
                                     UserHasPermissions(["can_restrict_members"]),
                                     BotHasPermissions(["can_restrict_members"]), ~(F.chat.type == ChatType.PRIVATE), F.reply_to_message.text]],
        [telegram_unmute_cmd_handler, [Command(commands=["unmute"]),
                                       UserHasPermissions(["can_restrict_members"]),
                                       BotHasPermissions(["can_restrict_members"]),
                                       ~(F.chat.type == ChatType.PRIVATE), F.reply_to_message.text]],
        [telegram_help_ban_handler,
         [Command(commands="ban"), IsAdminFilter(True, True), ~(F.chat.type == ChatType.PRIVATE)]],
        [telegram_help_unban_handler,
         [Command(commands="unban"), IsAdminFilter(True, True), ~(F.chat.type == ChatType.PRIVATE)]],
        [telegram_help_mute_handler, [Command(commands=["mute", "re"]), UserHasPermissions(["can_restrict_members"]),
                                      BotHasPermissions(["can_restrict_members"]), ~(F.chat.type == ChatType.PRIVATE)]],
        [telegram_help_unmute_handler,
         [Command(commands="unmute"), ~(F.chat.type == ChatType.PRIVATE), UserHasPermissions(["can_restrict_members"]),
          BotHasPermissions(["can_restrict_members"])]]
    ]
    telegram_callback_handlers = [
        #  Format is [Handler, [Filters]]
        [telegram_ban_callback_handler, [BanData.filter()]],
        [telegram_unban_callback_handler, [UnbanData.filter()]],
        [telegram_mute_callback_handler, [MuteData.filter()]],
        [telegram_unmute_callback_handler, [UnmuteData.filter()]]]
