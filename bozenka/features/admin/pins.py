from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bozenka.database.tables.telegram import TelegramChatSettings
from bozenka.features import BasicFeature
from bozenka.instances.telegram.utils.callbacks_factory import PinMsg, UnpinMsg
from bozenka.instances.telegram.utils.filters import UserHasPermissions, BotHasPermissions, IsAdminFilter
from bozenka.instances.telegram.utils.keyboards import unpin_msg_keyboard, delete_keyboard, pin_msg_keyboard
from bozenka.instances.telegram.utils.simpler import SolutionSimpler


class Pins(BasicFeature):
    """
    A class of pins related commands
    All staff related to it will be here
    """

    @staticmethod
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
                                     reply_markup=pin_msg_keyboard(user_id=call.from_user.id,
                                                                   msg_id=callback_data.msg_id))

    @staticmethod
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
                                     reply_markup=unpin_msg_keyboard(user_id=call.from_user.id,
                                                                     msg_id=callback_data.msg_id))

    @staticmethod
    async def telegram_pin_cmd(msg: Message) -> None:
        """
        /pin command function, pins replied command
        :param msg: Message telegram object
        :return: Nothing
        """
        await SolutionSimpler.pin_msg(msg)
        await msg.answer("Удача ✅\n"
                         "Сообщение было закреплено 📌",
                         reply_markup=pin_msg_keyboard(msg_id=msg.reply_to_message.message_id,
                                                       user_id=msg.from_user.id))

    @staticmethod
    async def telegram_unpin_cmd(msg: Message) -> None:
        """
        /unpin command function, unpins replied command
        :param msg: Message telegram object
        :return: Nothing
        """
        await SolutionSimpler.unpin_msg(msg)
        await msg.answer("Удача ✅\n"
                         "Сообщение было откреплено 📌",
                         reply_markup=unpin_msg_keyboard(msg_id=msg.reply_to_message.message_id,
                                                         user_id=msg.from_user.id))

    @staticmethod
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

    def __init__(self):
        """
        All information about feature
        will be inside this function
        """
        super().__init__()
        self.cmd_description: str = "Your description of command"
        # Telegram feature settings
        self.telegram_setting_in_list = True
        self.telegram_setting_name = "Закреп 📌"
        self.telegram_setting_description = "<b>Закреп</b>📌" \
                                            "\nДанная функция включает команды:" \
                                            "<pre>/pin - закрепляет сообщение\n" \
                                            "/unpin - открепляет сообщение\n" \
                                            "/unpin_all - открепляет все сообщения, которые видит бот</pre>\n" \
                                            "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота.</b>"
        self.telegram_db_name = TelegramChatSettings.pins
        # Telegram commands
        self.telegram_commands: dict[str: str] = {
            'pin': 'Pin fast any message in chat',
            'unpin': 'Unpin fast any message in chat',
        }
        self.telegram_cmd_avaible = True  # Is a feature have a commands
        # Telegram Handler
        self.telegram_message_handlers = {
            self.telegram_pin_cmd: [Command(commands="pin"), UserHasPermissions(["can_pin_messages"]),
                                    BotHasPermissions(["can_pin_messages"]), F.reply_to_message],
            self.telegram_unpin_cmd: [Command(commands="unpin"), UserHasPermissions(["can_pin_messages"]),
                                      BotHasPermissions(["can_pin_messages"]), F.reply_to_message],
            self.telegram_unpinall_cmd: [Command(commands="unpin_all"), IsAdminFilter(True),
                                         BotHasPermissions(["can_pin_messages"]), F.reply_to_message.text],
        }
        self.telegram_callback_handlers = {
            self.telegram_pin_callback_handler: [PinMsg.filter()],
            self.telegram_unpin_callback_handler: [UnpinMsg.filter()]
        }
