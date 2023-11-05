import gpt4all

from typing import Any

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from gpt4all import GPT4All

from bozenka.instances.telegram.utils.callbacks_factory import *
from bozenka.instances.telegram.utils.simpler import gpt_categories, gpt4free_providers, generate_gpt4free_providers

"""
File, contains inline keyboard & menus and their work.
Right now only on Russian language, multi-language planning soon.
"""


def setup_keyboard(owner_id) -> InlineKeyboardMarkup:
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


def delete_keyboard(admin_id) -> InlineKeyboardMarkup:
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


def gpt_categories_keyboard(user_id: int) -> InlineKeyboardMarkup:
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


def items_list_generator(page: int, list_of_items, count_of_items: int) -> list[Any]:
    """
    Generate page, made for backend
    :param page:
    :param list_of_items:
    :param count_of_items:
    """
    items = []
    required_items = [item + page * count_of_items for item in range(count_of_items)]
    for item, count in zip(list_of_items, range(0, len(list_of_items))):
        if count not in required_items:
            continue
        items.append(item)
    print(items)
    return items


def generate_gpt4free_providers_page(user_id: int, page: int) -> InlineKeyboardMarkup:
    """
    Generate page of gpt providers, can be used by user.
    :param user_id:
    :param page:
    :return:
    """
    providers = generate_gpt4free_providers()
    names = items_list_generator(page, providers, 4)
    pages = [len(providers) // 4 - 1 if page - 1 == -1 else page - 1,
             0 if page + 1 >= len(providers) // 4 else page + 1]
    generated_page = InlineKeyboardMarkup(inline_keyboard=[
        # First one provider
        [InlineKeyboardButton(text=names[0],
                              callback_data=Gpt4FreeProvider(user_id=user_id, provider=names[0], page="0").pack())],
        # Second one provider
        [InlineKeyboardButton(text=names[1],
                              callback_data=Gpt4FreeProvider(user_id=user_id, provider=names[1], page="0").pack())],
        # Third one provider
        [InlineKeyboardButton(text=names[2],
                              callback_data=Gpt4FreeProvider(user_id=user_id, provider=names[2], page="0").pack())],
        # Fourh one provider (if exist)
        [InlineKeyboardButton(text=names[3],
                              callback_data=Gpt4FreeProvider(user_id=user_id, provider=names[3],
                                                             page="0").pack())] if len(
            names) == 4 else [],
        # Page right
        [InlineKeyboardButton(text=str(len(providers) // 4 if page == 0 else "1"),
                              callback_data=Gpt4FreeProviderPage(
                                  page=str(len(providers) // 4 - 1 if page == 0 else "0"),
                                  user_id=user_id).pack()),

         InlineKeyboardButton(text="⬅️", callback_data=Gpt4FreeProviderPage(page=pages[0], user_id=user_id).pack()),
         InlineKeyboardButton(text=str(page + 1), callback_data="gotpages"),
         # Page left
         InlineKeyboardButton(text="➡️", callback_data=Gpt4FreeProviderPage(page=pages[1], user_id=user_id).pack()),
         InlineKeyboardButton(text=str(len(providers) // 4 if page != len(providers) // 4 - 1 else "1"),
                              callback_data=Gpt4FreeProviderPage(
                                  page=str(len(providers) // 4 - 1 if page != len(providers) // 4 - 1 else "0"),
                                  user_id=user_id).pack())
         ],
        [InlineKeyboardButton(text="🔙 Вернуться к категориям",
                              callback_data=GptBackMenu(user_id=user_id, back_to="category").pack())]
    ])
    return generated_page


def generate_gpt4free_models_page(user_id: int, provider, page: int) -> InlineKeyboardMarkup:
    """
    Generating list of GPT4Free provider's models, can be used to generate text.
    Will be also reworked.
    :param user_id:
    :param provider:
    :param page:
    """
    builder = InlineKeyboardBuilder()
    if provider in gpt4free_providers:
        names = items_list_generator(page, gpt4free_providers[provider], 4)
        for name in names:
            builder.row(InlineKeyboardButton(text=name.replace('-', ' '),
                                             callback_data=
                                             Gpt4freeResult(user_id=str(user_id),
                                                            provider=provider,
                                                            model=name).pack()))
        pages = [len(gpt4free_providers[provider]) // 4 - 1 if page - 1 == -1 else page - 1,
                 0 if page + 1 >= len(gpt4free_providers[provider]) // 4 else page + 1]
        if len(gpt4free_providers[provider]) > 4:
            builder.row(InlineKeyboardButton(text=str(len(gpt4free_providers[provider]) // 4 if page == 0 else "1"),
                                             callback_data=Gpt4FreeModelPage(
                                                 page=str(
                                                     len(gpt4free_providers[provider]) // 4 - 1 if page == 0 else "1"),
                                                 user_id=user_id,
                                                 provider=provider
                                             ).pack(),
                                             ),
                        InlineKeyboardButton(text="⬅️",
                                             callback_data=Gpt4FreeModelPage(
                                                 user_id=str(user_id),
                                                 page=pages[0],
                                                 provider=provider
                                             ).pack()),
                        InlineKeyboardButton(text=str(page + 1), callback_data="gotpages"),
                        InlineKeyboardButton(text="➡️",
                                             callback_data=Gpt4FreeModelPage(
                                                 user_id=str(user_id),
                                                 page=pages[1],
                                                 provider=provider
                                             ).pack()),
                        InlineKeyboardButton(text=str(len(gpt4free_providers[provider]) // 4 if page != 0 else "1"),
                                             callback_data=Gpt4FreeModelPage(
                                                 page=str(
                                                     len(gpt4free_providers[provider]) // 4 - 1) if page != 0 else "1",
                                                 user_id=user_id,
                                                 provider=provider
                                             ).pack(),

                                             ))
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
    builder.row(InlineKeyboardButton(text="🔙 Вернуться к провайдерам",
                                     callback_data=GptBackMenu(user_id=user_id, back_to="providers").pack()))
    return builder.as_markup()


def generate_gpt4all_page(user_id: int) -> InlineKeyboardMarkup:
    """
    Generating list of GPT4All models.
    :param user_id:
    """
    models = GPT4All.list_models()

    builder = InlineKeyboardBuilder()

    for model in models:
        builder.row(InlineKeyboardButton(
            text=model["name"],
            callback_data=Gpt4AllModel(user_id=str(user_id), model_index=str(models.index(model))).pack())
        )
    builder.row(InlineKeyboardButton(text="🔙 Вернуться к списку",
                                     callback_data=GptBackMenu(user_id=user_id, back_to="category").pack()))
    return builder.as_markup()


def inline_gpt4all_select(user_id: int) -> InlineKeyboardMarkup:
    """
    Generates menu of enabling
    :param user_id:
    """


def gpt_answer_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Generating menu for answer from gpt
    :param user_id:
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Спасибо ✅", callback_data=DeleteCallbackData(user_id_clicked=str(user_id)).pack()),
         InlineKeyboardButton(text="Завершить диалог 🚫", callback_data=GptStop(user_id=str(user_id)).pack())]
    ])
    return kb


def ban_keyboard(admin_id: int, ban_id: int) -> InlineKeyboardMarkup:
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


def unban_keyboard(admin_id: int, ban_id: int) -> InlineKeyboardMarkup:
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


def mute_keyboard(admin_id: int, ban_id: int) -> InlineKeyboardMarkup:
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


def unmute_keyboard(admin_id: int, ban_id: int) -> InlineKeyboardMarkup:
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


def invite_keyboard(link: str, admin_id: int, chat_name: str) -> InlineKeyboardMarkup:
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
    text="Bozo Development", url="https://t.me/BozoDevelopment"
)
