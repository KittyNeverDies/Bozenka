from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bozenka.telegram.utils.callbacks_factory import *
from bozenka.telegram.utils.simpler import gpt_categories, gpt4free_providers, generate_gpt4free_providers

"""
File, contains inline keyboard & menus and their work.
Right now only on Russian language, multi-language planning soon.
"""


def setup_keyboard(owner_id):
    """
    Generate keybaord for /setup command
    :param owner_id:
    :return:
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Администраторы 👮‍♂",
                             callback_data=SetupCategory(owner_id=owner_id, category_name="Admins").pack())
    ], [
        InlineKeyboardButton(text="Пользователи 👤",
                             callback_data=SetupCategory(owner_id=owner_id, category_name="Members").pack())
    ]])
    return kb


def delete_keyboard(admin_id):
    """
    Basic keyboard for all messages from bot.
    By pressing this button, message from bot will get deleted.
    :param admin_id:
    :return:
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Спасибо ✅", callback_data=DeleteCallbackData(user_id_clicked=str(admin_id)).pack())
    ]])
    return kb


def gpt_categories_keyboard(user_id: int):
    """
    Create list keyboard list of gpt libraries, available in the bot
    :param user_id:
    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    for category in gpt_categories:
        builder.button(text=category, callback_data=GptCategory(
            user_id=str(user_id),
            category=category,
        ))
    return builder.as_markup()


def generate_gpt4free_page(user_id, page):
    """
    Generate page of gpt providers, can be used by user.
    :param user_id:
    :param page:
    :return:
    """
    names = []
    providers = generate_gpt4free_providers()
    pages = [len(providers) // 4 - 1 if page - 1 == -1 else page - 1,
             0 if page + 1 >= len(providers) // 4 else page + 1]
    for provider, count in zip(providers, range(1, len(providers))):
        if count not in [0 + page * 4, 1 + page * 4, 2 + page * 4, 3 + page * 4]:
            continue
        names.append(provider)
    generated_page = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=names[0],
                              callback_data=Gpt4FreeProvider
                              (user_id=user_id,
                               provider=names[0]).pack())],
        [InlineKeyboardButton(text=names[1],
                              callback_data=Gpt4FreeProvider
                              (user_id=user_id,
                               provider=names[1]).pack())],
        [InlineKeyboardButton(text=names[2],
                              callback_data=Gpt4FreeProvider
                              (user_id=user_id,
                               provider=names[2]).pack())],
        [InlineKeyboardButton(text=names[3],
                              callback_data=Gpt4FreeProvider
                              (user_id=user_id,
                               provider=names[3]).pack())] if len(names) == 4 else [],
        [
            InlineKeyboardButton(text=str(len(providers) // 4 if page == 0 else "1"),
                                 callback_data=Gpt4FreePage(
                                     page=str(len(providers) // 4 - 1 if page == 0 else "1"),
                                     user_id=user_id).pack()),
            InlineKeyboardButton(text="⬅️", callback_data=Gpt4FreePage(page=pages[0], user_id=user_id).pack()),
            InlineKeyboardButton(text=str(page + 1), callback_data="gotpages"),
            InlineKeyboardButton(text="➡️", callback_data=Gpt4FreePage(page=pages[1], user_id=user_id).pack()),
            InlineKeyboardButton(text=str(len(providers) // 4),
                                 callback_data=Gpt4FreePage(
                                     page=str(len(providers) // 4 - 1),
                                     user_id=user_id).pack())
        ]
    ])
    return generated_page


def gpt4free_category_keyboard(user_id):
    """
        Generating list of GPT4Free providers, can be used to generate text.
        Will be reworked.
        :param user_id:
        :return:
    """
    builder = InlineKeyboardBuilder()
    for provider in gpt4free_providers:
        print(provider)
        builder.button(text=provider,
                       callback_data=Gpt4FreeProvider(user_id=str(user_id), provider=provider).pack())
    return builder.as_markup()


def gpt4free_models_keyboard(user_id, provider):
    """
        Generating list of GPT4Free provider's models, can be used to generate text.
        Will be also reworked.
    """
    builder = InlineKeyboardBuilder()
    if provider in gpt4free_providers:
        for model in gpt4free_providers[provider]:
            builder.row(InlineKeyboardButton(
                text=model.replace("-", " "),
                callback_data=Gpt4freeResult(user_id=str(user_id),
                                             provider=provider,
                                             model=model).pack()))
    else:
        providers = generate_gpt4free_providers()
        if providers[provider].supports_gpt_4:
            builder.row(InlineKeyboardButton(text="gpt 4",
                                             callback_data=Gpt4freeResult(user_id=str(user_id),
                                                                          provider=provider,
                                                                          model="gpt-4").pack()))
        if providers[provider].supports_gpt_35_turbo:
            builder.row(InlineKeyboardButton(text="gpt 3.5 turbo",
                                             callback_data=Gpt4freeResult(user_id=str(user_id),
                                                                          provider=provider,
                                                                          model="gpt-3.5-turbo").pack()))
    return builder.as_markup()


def ban_keyboard(admin_id, ban_id):
    """
        Generating menu for /ban command.
        :param admin_id:
        :param ban_id:
        :return:
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Спасибо ✅", callback_data=DeleteCallbackData(user_id_clicked=str(admin_id)).pack())
    ], [
        InlineKeyboardButton(text="Разбанить 🛠️", callback_data=UnbanData(user_id_unban=str(ban_id),
                                                                          user_id_clicked=str(admin_id)).pack())
    ]])
    return kb


def unban_keyboard(admin_id, ban_id):
    """
        Generating menu for /unban command.
        :param admin_id:
        :param ban_id:
        :return:
    """
    print(ban_id)
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Спасибо ✅", callback_data=DeleteCallbackData(user_id_clicked=str(admin_id)).pack())
    ], [
        InlineKeyboardButton(text="Забанить 🛠️", callback_data=BanData(user_id_ban=str(ban_id),
                                                                       user_id_clicked=str(admin_id)).pack())
    ]])
    return kb


def mute_keyboard(admin_id, ban_id):
    """
       Generating menu for /mute command.
       :param admin_id:
       :param ban_id:
       :return:
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Спасибо ✅", callback_data=DeleteCallbackData(user_id_clicked=str(admin_id)).pack())
    ], [
        InlineKeyboardButton(text="Размутить 🛠️",
                             callback_data=UnmuteData(user_id_unmute=ban_id, user_id_clicked=admin_id).pack())
    ]])
    return kb


def unmute_keyboard(admin_id, ban_id):
    """
        Generating menu for /unmute command.
        :param admin_id:
        :param ban_id:
        :return:
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Спасибо ✅", callback_data=DeleteCallbackData(user_id_clicked=str(admin_id)).pack())
    ], [
        InlineKeyboardButton(text="Замутить 🛠️",
                             callback_data=MuteData(user_id_mute=ban_id, user_id_clicked=admin_id).pack())
    ]])
    return kb


def invite_keyboard(link: str, admin_id, chat_name):
    """
        Generating menu for /invite command. Should be reworked.
        :param link:
        :param admin_id:
        :param chat_name:
        :return:
    """
    link = link.replace("https://", "")
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=chat_name, url=link)
    ], [
        InlineKeyboardButton(text="Отозвать 🛠️", callback_data=RevokeCallbackData(admin_id=admin_id, link=link).pack())
    ], [
        InlineKeyboardButton(text="Спасибо ✅",
                             callback_data=DeleteCallbackData(user_id_clicked=str(admin_id)).pack())
    ]])
    return kb


about_keyboard = InlineKeyboardBuilder()
about_keyboard.button(
    text="Bozo Development", url="https://t.me/BozoDevelopement"
)