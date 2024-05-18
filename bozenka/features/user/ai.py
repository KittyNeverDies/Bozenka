from aiogram import F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bozenka.database.tables.telegram import TelegramChatSettings
from bozenka.features.main import BasicFeature
from bozenka.generative.generative_categories import commands
from bozenka.generative.queue_logic import queue
from bozenka.instances.telegram.filters import IsSettingEnabled
from bozenka.instances.telegram.utils.delete import delete_keyboard
from bozenka.instances.telegram.utils.simpler import AIGeneration


class GptStop(CallbackData, prefix="gs"):
    """
    Callback with information to stop conversation with GPT
    """
    user_id: int


class AiFeature(BasicFeature):

    """
    A class of AI features of the bot
    All staff related to it will be here
    """
    @staticmethod
    async def telegram_ready_to_answer_hanlder(msg: Message, state: FSMContext) -> None:
        """
        Working if user selected his generative AI for generation
        :param msg: Message telegram object
        :param state: FSMContext aiogram object
        :return: None
        """
        await state.set_state(AIGeneration.answering)

        data = await state.get_data()

        message_queue = await msg.reply(
            "Хорошо ✅\n\nВаш запрос находится в очереди на обработку.\n"
            f"Позиция в очереди: <b>{queue.qsize()}/{queue.maxsize}</b>\n"
            f"Мы сообщим, если что-то пошло не так.\n",
            reply_markup=delete_keyboard(admin_id=msg.from_user.id)
        )

        await queue.put(({
            "category": data["category"],
            "name": data["name"]
        }, [msg, state, message_queue]))

    @staticmethod
    async def telegram_answering_handler(msg: Message) -> None:
        """
        Working if user send request while we are already answering his question
        :param msg: Message telegram object
        :return: None
        """
        await msg.reply("<b>Не так быстро </b>✋\n\nМы уже генерируем ответ на ваш запрос.\n"
                        "Пожалуйста, подождите пока мы ответим на предыдущий ваш запрос, перед тем как задать новый")

    @staticmethod
    async def cancel_telegram_handler(msg: Message, state: FSMContext) -> None:
        """
        Cancel generation by generative AI
        :param msg: Message telegram object
        :param state: FSMContext aiogram object
        :return: None
        """
        if not await state.get_data():
            return

        await msg.reply("Хорошо ✅\n\nМы остановили генерацию ответов на ваши запросы. Теперь вы можете заниматься своими делами.\n", keyboard=delete_keyboard(admin_id=msg.from_user.id))

    @staticmethod
    async def telegram_stop_dialog_handler(call: CallbackQuery, callback_data: GptStop, state: FSMContext) -> None:
        """
        Query, what stops dialog
        :param call: CallbackQuery telegram class
        :param callback_data: GptStop class
        :param state: None
        """
        # Checking user_id of user
        if callback_data.user_id != call.from_user.id:
            return
        # Answering something
        await call.answer("Хорошо ✅")
        current_state = await state.get_state()
        data = await state.get_data() # Getting data from state
        if current_state in [AIGeneration.answering, AIGeneration.ready_to_answer] and data["category"] == "text2text":
            await call.message.edit_text(text=call.message.text + "\n\nДиалог остановлен ✅\n",
                                         reply_markup=delete_keyboard(admin_id=call.from_user.id))
        elif current_state in [AIGeneration.answering, AIGeneration.ready_to_answer] and data["category"] == "text2text":
            await call.message.edit_caption(caption=call.message.caption + "\n\nГенерация изображений остановленна")
        else:
            await call.message.delete()
        await call.message.answer(
            "Хорошо ✅\n\nМы остановили генерацию ответов на ваши запросы. Теперь вы можете заниматься своими делами.\n",
            keyboard=delete_keyboard(admin_id=call.message.from_user.id))
        # Clearing state
        await state.clear()

    # Telegram feature settings
    telegram_category = "user"
    telegram_commands: dict[str: str] = {}
    telegram_db_name = TelegramChatSettings.ai_working
    telegram_setting_in_list = True
    telegram_setting_name = "Искуственный Интелект 🤖"
    current_comands = ""
    for i in commands:
        current_comands += f"/{i.command} - {i.description}\n"
    telegram_setting_description = "<b>Приветсвенные сообщения 🤖</b>" \
                                   "\nИскуственный интелект, для работы с текстом и создания изображений.\n" \
                                   f"Текущие команды, доступные для использования:<pre>{current_comands}</pre>"
    telegram_cmd_avaible = False  # Is a feature have a commands
    telegram_message_handlers = [
        [cancel_telegram_handler, [Command('cancel')]],
        [telegram_ready_to_answer_hanlder, [F.chat.type == ChatType.PRIVATE, AIGeneration.ready_to_answer]],
        [telegram_ready_to_answer_hanlder, [~(F.chat.type == ChatType.PRIVATE), IsSettingEnabled(telegram_db_name), AIGeneration.ready_to_answer]],
    ]
    telegram_callback_handlers = [
        [telegram_stop_dialog_handler, [GptStop.filter()]]
    ]
