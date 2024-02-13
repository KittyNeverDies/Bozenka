from aiogram import F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bozenka.database.tables.telegram import TelegramChatSettings
from bozenka.features.main import BasicFeature
from bozenka.instances.telegram.utils.callbacks_factory import PinMsg, UnpinMsg, DeleteMenu
from bozenka.instances.telegram.filters import UserHasPermissions, BotHasPermissions, IsAdminFilter
from bozenka.instances.telegram.utils.delete import delete_keyboard
from bozenka.instances.telegram.utils.simpler import SolutionSimpler


# Pin / Unpin command
def telegram_pin_msg_keyboard(user_id: int, msg_id: int) -> InlineKeyboardMarkup:
    """
    Generate menu for /pin command
    :param user_id: User_id of user pinned the message
    :param msg_id: Message_id of pinned message
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открепить сообщение 📌",
                              callback_data=UnpinMsg(user_id=user_id, msg_id=msg_id).pack())],
        [InlineKeyboardButton(text="Спасибо ✅", callback_data=DeleteMenu(user_id_clicked=str(user_id)).pack())]
    ])
    return kb


def telegram_unpin_msg_keyboard(user_id: int, msg_id: int) -> InlineKeyboardMarkup:
    """
    Generate menu for /unpin command
    :param user_id: User_id of user unpinned the message
    :param msg_id: Message_id of unpinned message
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открепить сообщение 📌",
                              callback_data=PinMsg(user_id=user_id, msg_id=msg_id).pack())],
        [InlineKeyboardButton(text="Спасибо ✅", callback_data=DeleteMenu(user_id_clicked=str(user_id)).pack())]
    ])
    return kb


class Pins(BasicFeature):
    """
    A class of pins related commands
    All staff related to it will be here
    """

    async def telegram_pin_callback_handler(call: CallbackQuery, callback_data: PinMsg) -> None:
        """
        Query, what pins message
        :param call:
        :param callback_data:
        :return:
        """
        if callback_data.user_id == call.from_user.id:
            return

        await call.message.chat.pin_message(message_id=callback_data.msg_id)
        await call.message.edit_text("Удача ✅\n"
                                     "Сообщение было закреплено 📌",
                                     reply_markup=telegram_pin_msg_keyboard(user_id=call.from_user.id,
                                                                            msg_id=callback_data.msg_id))

    async def telegram_unpin_callback_handler(call: CallbackQuery, callback_data: UnpinMsg) -> None:
        """
        Query, what unpins message
        :param call:
        :param callback_data:
        :return:
        """
        if callback_data.user_id == call.from_user.id:
            return

        await call.message.chat.pin_message(message_id=callback_data.msg_id)
        await call.message.edit_text("Удача ✅\n"
                                     "Сообщение было откреплено 📌",
                                     reply_markup=telegram_unpin_msg_keyboard(user_id=call.from_user.id,
                                                                              msg_id=callback_data.msg_id))

    async def telegram_pin_cmd(msg: Message) -> None:
        """
        /pin command function, pins replied command
        :param msg: Message telegram object
        :return: Nothing
        """
        await SolutionSimpler.pin_msg(msg)
        await msg.answer("Удача ✅\n"
                         "Сообщение было закреплено 📌",
                         reply_markup=telegram_pin_msg_keyboard(msg_id=msg.reply_to_message.message_id,
                                                                user_id=msg.from_user.id))

    async def telegram_unpin_cmd(msg: Message) -> None:
        """
        /unpin command function, unpins replied command
        :param msg: Message telegram object
        :return: Nothing
        """
        await SolutionSimpler.unpin_msg(msg)
        await msg.answer("Удача ✅\n"
                         "Сообщение было откреплено 📌",
                         reply_markup=telegram_unpin_msg_keyboard(msg_id=msg.reply_to_message.message_id,
                                                                  user_id=msg.from_user.id))

    async def telegram_unpinall_cmd(msg: Message) -> None:
        """
        /unpin_all command function, unpins all messages in chat
        :param msg: Message telegram object
        :return: Nothing
        """
        await SolutionSimpler.unpin_all_messages(msg)
        await msg.answer("Удача ✅\n"
                         "Все сообщения были откреплены 📌",
                         reply_markup=delete_keyboard(admin_id=msg.from_user.id))

    async def telegram_help_pin_cmd(msg: Message) -> None:
        """
        Shows help message for /mute
        :param msg: Message telegram object
        :return: Nothing
        """
        await msg.answer("Использование:\n"
                         "<pre>/pin</pre>\n"
                         "Ответьте на сообщение, чтобы закрепить сообщение",
                         reply_markup=delete_keyboard(msg.from_user.id))

    async def telegramm_help_unpin_cmd(msg: Message) -> None:
        """
        Shows help message for /mute
        :param msg: Message telegram object
        :return: Nothing
        """
        await msg.answer("Использование:\n"
                         "<pre>/unpin</pre>\n"
                         "Ответьте на сообщение, чтобы открепить сообщение",
                         reply_markup=delete_keyboard(msg.from_user.id))

    """
    Telegram feature settings
    """
    # Telegram feature settings
    telegram_setting_in_list = True
    telegram_setting_name = "Закреп 📌"
    telegram_setting_description = "<b>Закреп</b>📌" \
                                   "\nДанная функция включает команды:" \
                                   "<pre>/pin - закрепляет сообщение\n" \
                                   "/unpin - открепляет сообщение\n" \
                                   "/unpin_all - открепляет все сообщения, которые видит бот</pre>\n" \
                                   "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота.</b>"
    telegram_db_name = TelegramChatSettings.pins
    telegram_category = "admin"
    # Telegram commands
    telegram_commands: dict[str: str] = {
        'pin': 'Pin fast any message in chat',
        'unpin': 'Unpin fast any message in chat',
    }
    telegram_cmd_avaible = True  # Is a feature have a commands
    # Telegram Handler
    telegram_message_handlers = [
        #  Format is [Handler, [Filters]]
        [telegram_pin_cmd, [Command(commands="pin"), UserHasPermissions(["can_pin_messages"]),
                            BotHasPermissions(["can_pin_messages"]), F.reply_to_message,
                            ~(F.chat.type == ChatType.PRIVATE)]],
        [telegram_unpin_cmd, [Command(commands="unpin"), UserHasPermissions(["can_pin_messages"]),
                              BotHasPermissions(["can_pin_messages"]), F.reply_to_message,
                              ~(F.chat.type == ChatType.PRIVATE)]],
        [telegram_unpinall_cmd, [Command(commands="unpin_all"), IsAdminFilter(True, False),
                                 BotHasPermissions(["can_pin_messages"]), F.reply_to_message.text,
                                 ~(F.chat.type == ChatType.PRIVATE)]],
        [telegram_help_pin_cmd, [Command(commands="pin"), UserHasPermissions(["can_pin_messages"]),
                                 BotHasPermissions(["can_pin_messages"]), ~(F.chat.type == ChatType.PRIVATE)]],
        [telegramm_help_unpin_cmd, [Command(commands="unpin"), UserHasPermissions(["can_pin_messages"]),
                                    BotHasPermissions(["can_pin_messages"]), ~(F.chat.type == ChatType.PRIVATE)]]

    ]
    telegram_callback_handlers = [
        #  Format is [Handler, [Filters]]
        [telegram_pin_callback_handler, [PinMsg.filter()]],
        [telegram_unpin_callback_handler, [UnpinMsg.filter()]]
    ]
