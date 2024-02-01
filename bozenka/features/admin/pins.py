from aiogram.types import Message, CallbackQuery

from bozenka.features import BasicFeature
from bozenka.instances.telegram.utils.callbacks_factory import PinMsg, UnpinMsg
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
        self.telegram_setting = None
        self.telegram_commands: list[str | None] = ["start"]
        self.telegram_cmd_avaible = True  # Is a feature have a commands
        self.telegram_callback_factory = None
        self.telegram_message_handlers = {

        }
        self.telegram_callback_handlers = {

        }
