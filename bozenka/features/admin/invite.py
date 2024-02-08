import logging

from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bozenka.database.tables.telegram import TelegramChatSettings
from bozenka.features import BasicFeature
from bozenka.instances.telegram.utils.callbacks_factory import RevokeCallbackData
from bozenka.instances.telegram.utils.keyboards import invite_keyboard
from bozenka.instances.telegram.utils.simpler import ru_cmds


class Invite(BasicFeature):
    """
    A class with information about invite feature
    All codes will be here
    """

    @staticmethod
    async def telegram_invite_command_handler(msg: Message) -> None:
        """
        Generating invite to group by /invite command
        :param msg: Message telegram object
        :return: None
        """
        logging.log(msg=f"Generating invite for user_id={msg.from_user.id}",
                    level=logging.INFO)
        link = await msg.chat.create_invite_link()

        await msg.answer(
            f"<em> Держите ваше приглашение в чат, {msg.from_user.mention_html('пользователь')} 👋</em>",
            reply_markup=invite_keyboard(link=str(link.invite_link), admin_id=msg.from_user.id,
                                         chat_name=msg.chat.full_name)
        )

    @staticmethod
    async def telegram_revoke_callback_handler(call: CallbackQuery, callback_data: RevokeCallbackData) -> None:
        """
        Handler of CallbackQuery, revokes link after pressing button
        :param call: CallbackQuery aioram object
        :param callback_data: RevokeCallbackData object
        :return: Nothing
        """
        user_clicked = await call.message.chat.get_member(call.from_user.id)

        if callback_data.admin_id != call.from_user.id and \
                user_clicked.status != ChatMemberStatus.ADMINISTRATOR and user_clicked.status == ChatMemberStatus.CREATOR:
            return
        logging.log(msg=f"Revoking link for user_id={call.from_user.id}",
                        level=logging.INFO)
        await call.message.chat.revoke_invite_link(invite_link="https://" + str(callback_data.link))
        await call.answer("Удача ✅")
        await call.message.delete()

    def __init__(self):
        """
        All information about feature
        will be inside this function
        """
        super().__init__()
        """
        Telegram feature settings
        """
        # Telegram setting info
        self.telegram_setting_in_list = True
        self.telegram_setting_name = "Приглашения в Чат ✉"
        self.telegram_setting_description = "<b>Генератор приглашения в Чат ✉</b>\n" \
            "Разрешает использование комманды <code>/invite</code> в чате, для созданния приглашений.\n" \
            "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота.</b>"
        self.telegram_db_name = TelegramChatSettings.invite_generator
        # Telegram commands
        self.telegram_commands: dict[str: str] = {"/invite": 'Generates invite into current chat'}
        self.telegram_cmd_avaible = True  # Is a feature have a commands
        # List of aiogram handlers
        self.telegram_message_handlers = (
            #  Format is [Handler, [Filters]]
            [self.telegram_invite_command_handler, [Command(commands=["invite"])]]
        )
        self.telegram_callback_handlers = (
            #  Format is [Handler, [Filters]]
            [self.telegram_revoke_callback_handler, [RevokeCallbackData.filter()]]
        )
