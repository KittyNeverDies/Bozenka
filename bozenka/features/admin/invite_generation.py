import logging

from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bozenka.database.tables.telegram import TelegramChatSettings
from bozenka.features.main import BasicFeature
from bozenka.instances.telegram.utils.callbacks_factory import RevokeCallbackData, DeleteMenu


# Invite keyboard
def invite_telegram_keyboard(invite_link: str, admin_id: int, chat_name: str) -> InlineKeyboardMarkup:
    """
    Generating menu for /invite command. Should be reworked.
    :param invite_link: Invite link to chat
    :param admin_id: User_id of telegram administrator
    :param chat_name: Name  of group chat
    :return: Nothing
    """
    invite_revoke_link = invite_link.replace("https://", "")
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=chat_name, url=invite_link)],
        [InlineKeyboardButton(text="Отозвать 🛠️",
                              callback_data=RevokeCallbackData(admin_id=admin_id, link=invite_revoke_link).pack())],
        [InlineKeyboardButton(text="Спасибо ✅",
                              callback_data=DeleteMenu(user_id_clicked=str(admin_id)).pack())]])
    return kb


class Invite(BasicFeature):
    """
    A class with information about invite feature
    All codes will be here
    """

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
            reply_markup=invite_telegram_keyboard(invite_link=str(link.invite_link), admin_id=msg.from_user.id,
                                                  chat_name=msg.chat.full_name)
        )

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

    """
    Telegram feature settings
    """
    # Telegram setting info
    telegram_setting_in_list = True
    telegram_setting_name = "Приглашения в Чат ✉"
    telegram_setting_description = "<b>Генератор приглашения в Чат ✉</b>\n" \
                                   "Разрешает использование комманды <code>/invite</code> в чате, для созданния приглашений.\n" \
                                   "Для исполнения <b>требует соответсвующих прав от пользователя и их наличие у бота.</b>"
    telegram_db_name = TelegramChatSettings.invite_generator
    telegram_category = "admin"
    # Telegram commands
    telegram_commands: dict[str: str] = {"/invite": 'Generates invite into current chat'}
    telegram_cmd_avaible = True  # Is a feature have a commands
    # List of aiogram handlers
    telegram_message_handlers = [
        #  Format is [Handler, [Filters]]
        [telegram_invite_command_handler, [Command(commands=["invite"])]]
    ]
    telegram_callback_handlers = [
        #  Format is [Handler, [Filters]]
        [telegram_revoke_callback_handler, [RevokeCallbackData.filter()]]
    ]
