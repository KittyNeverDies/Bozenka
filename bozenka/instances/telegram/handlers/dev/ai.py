import logging
import os.path

import g4f
from gpt4all import GPT4All
from aiogram.fsm.context import FSMContext
from aiogram.types import Message as Message

from bozenka.generative.gpt4all import check
from bozenka.instances.telegram.utils.keyboards import gpt_categories_keyboard, delete_keyboard, response_keyboard
from bozenka.instances.telegram.utils.simpler import generate_gpt4free_providers, ru_cmds, AnsweringGpt4All, \
    AnsweringGPT4Free


async def already_answering(msg: Message, state: FSMContext):
    """
    Giving response, if answering user now,
    but he still asks something
    :param msg:
    :param state:
    :return:
    """
    await msg.answer("Подождите пожалуйста, мы уже генерируем ответ для вас, подождите, когда мы ответим на ваш передыдущий вопрос",
                     reply_markup=delete_keyboard(admin_id=msg.from_user.id))


async def start_dialog_cmd(msg: Message, state: FSMContext):
    """
    /conversation command handler, start
    :param msg:
    :param state:
    :return:
    """
    if await state.get_state():
        return
    await msg.answer("Пожалуста, выберите сервис для ИИ.",
                     reply_markup=gpt_categories_keyboard
                     (user_id=msg.from_user.id))


async def cancel_answering(msg: Message, state: FSMContext):
    """
    Canceling dialog with generative model
    Works on command /cancel
    :param msg:
    :param state:
    :return:
    """
    current = await state.get_state()
    if current is None:
        return
    await state.clear()
    await msg.answer("Удача ✅\n"
                     "Диалог отменён!", reply_markup=delete_keyboard(admin_id=msg.from_user.id))


async def g4a_generate_answer(msg: Message, state: FSMContext):
    """
    Generating answer if Gpt4All has been selected
    :param msg:
    :param state:
    :return:
    """
    await state.set_state(AnsweringGpt4All.answering)

    models = GPT4All.list_models()
    info = await state.get_data()
    answer = ""

    main_msg = await msg.answer("Пожалуйста подождите, мы генерируем вам ответ ⏰\n"
                                "Если что-то пойдет не так, мы вам сообщим 👌",
                                reply_markup=response_keyboard(user_id=msg.from_user.id))

    if not check(models[info["set_model"]]["filename"]):
        main_msg = await main_msg.edit_text(main_msg.text + "\nПодождите пожалуста, мы скачиваем модель...",
                                            reply_markup=main_msg.reply_markup)

    try:
        # Setting Gpt4All model
        model = GPT4All(model_name=models[info['set_model']]['filename'],
                        model_path="/bozenka/generative\\gpt4all\\models\\",
                        allow_download=True)
        # Setting our chat session if exist
        model.current_chat_session = [] if not info.get("ready_to_answer") else info["ready_to_answer"]
        # Generating answer
        with model.chat_session():
            answer = model.generate(msg.text)
            await state.update_data(ready_to_answer=model.current_chat_session)

    except Exception as S:
        answer = "Простите, произошла ошибка 😔\nЕсли это продолжается, пожалуйста используйте /cancel"
        logging.log(msg=f"Get an exception for generating answer={S}",
                    level=logging.INFO)
    finally:
        await main_msg.edit_text(answer, reply_markup=response_keyboard(user_id=msg.from_user.id))

    await state.set_state(AnsweringGpt4All.ready_to_answer)


async def g4f_generate_answer(msg: Message, state: FSMContext):
    """
    Generating answer if GPT4Free model and provider has been selected
    :param msg:
    :param state:
    :return:
    """
    await state.set_state(AnsweringGPT4Free.answering)

    info = await state.get_data()

    providers = generate_gpt4free_providers()
    reply = await msg.reply("Пожалуйста подождите, мы генерируем ответ от провайдера ⏰\n"
                            "Если что-то пойдет не так, мы вам сообщим 👌")

    current_messages = []
    if info.get("ready_to_answer"):
        for message in info["ready_to_answer"]:
            current_messages.append(message)
    current_messages.append({"role": "user", "content": msg.text})

    response = ""
    try:
        response = await g4f.ChatCompletion.create_async(
            model=info["set_model"],
            messages=current_messages,
            provider=providers[info["set_provider"]],
            stream=False
        )
    except NameError:
        try:
            response = g4f.ChatCompletion.create(
                model=info["set_model"],
                messages=current_messages,
                provider=providers[info["set_provider"]],
                stream=False
            )
        except Exception as S:
            response = "Простите, произошла ошибка 😔\nЕсли это продолжается, пожалуйста используйте /cancel"
            logging.log(msg=f"Get an exception for generating answer={S}",
                        level=logging.INFO)
    except Exception as S:
        response = "Простите, произошла ошибка 😔\nЕсли это продолжается, пожалуйста используйте /cancel"
        logging.log(msg=f"Get an exception for generating answer={S}",
                    level=logging.INFO)
    finally:
        await reply.edit_text(text=response, reply_markup=response_keyboard(user_id=msg.from_user.id))
        current_messages.append({"role": "assistant", "content": response})
        await state.update_data(ready_to_answer=current_messages)
    await state.set_state(AnsweringGPT4Free.ready_to_answer)


async def generate_image(msg: Message):
    """
    Image generation, planned in future
    :param msg:
    """
    pass
