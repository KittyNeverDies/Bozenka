import g4f
from gpt4all import GPT4All
from aiogram.fsm.context import FSMContext
from aiogram.types import Message as Message
from bozenka.telegram.utils.keyboards import gpt_categories_keyboard, delete_keyboard
from bozenka.telegram.utils.simpler import generate_gpt4free_providers, ru_cmds


async def start_gpt_cmd(msg: Message, state: FSMContext):
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
    Canceling dialog with ChatGPT
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
    model = GPT4All("ggml-model-gpt4all-falcon-q4_0.bin")
    model.list_models()
    output = model.generate(msg.text, max_tokens=3, )
    await msg.answer(text=output)


async def g4f_generate_answer(msg: Message, state: FSMContext):
    """
    Generating answer if GPT4Free model and provider has been selected
    :param msg:
    :param state:
    :return:
    """
    print("starting")
    info = await state.get_data()
    """
    if info.get("forum_thread_id") is not None:
        if msg.message_thread_id != info["forum_thread_id"] and info["forum_thread_id"] is not None:
            return
    """
    print("starting 2")
    providers = generate_gpt4free_providers()
    reply = await msg.reply(ru_cmds["generate_answer"])
    # try:
    messages = []
    messages.append({"role": "user", "content": msg.text})
    if info.get("ready_to_answer"):
        for message in info["ready_to_answer"]:
            messages.append(message)
    response = await g4f.ChatCompletion.create_async(
        model=info["set_model"],
        messages=messages,
        provider=providers[info["set_provider"]],
        stream=False
    )
    print(response)
    await reply.edit_text(response)
    messages.append({"role": "assistant", "content": response})
    await state.update_data(ready_to_answer=messages)
#    except Exception:
    print(Exception)
#        await reply.edit_text("Простите, произошла ошибка 😔\n"
#                        "Если это продолжается, пожалуйста используйте /cancel", reply_markup=delete_keyboard(admin_id=msg.from_user.id))


async def generate_image(msg: Message):
    pass
