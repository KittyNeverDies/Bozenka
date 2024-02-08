import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import Message as Message, FSInputFile

from bozenka.generative.kadinsky import kadinsky_gen
from bozenka.instances.telegram.utils.keyboards import delete_keyboard, image_generation_keyboard, \
    image_response_keyboard
from bozenka.instances.telegram.utils.simpler import GeneratingImages


async def already_generating(msg: Message, state: FSMContext):
    """
    Giving response, if generating image for user right now,
    but user still asks something
    :param msg: Message telegram object
    :param state: FSM state of bot
    :return:
    """
    await msg.answer(
        "Подождите пожалуйста, мы уже генерируем изображение для вас, подождите, когда мы ответим на ваш передыдущий вопрос",
        reply_markup=delete_keyboard(admin_id=msg.from_user.id))


async def start_imagine_cmd(msg: Message, state: FSMContext):
    """
    /iamgine command handler, start menu
    :param msg: Message telegram object
    :param state: FSM state of bot
    :return:
    """
    if await state.get_state():
        return
    await msg.answer("Пожалуста, выберите сервис / модель для генерации изображений",
                     reply_markup=image_generation_keyboard(user_id=msg.from_user.id))


async def kadinsky_generating_images(msg: Message, state: FSMContext):
    """
    Message handler for kandinsky to generate image by text from message
    :param msg: Message telegram object
    :param state: FSM state of bot
    :return:
    """
    await state.set_state(GeneratingImages.generating)
    message = await msg.answer("Пожалуйста подождите, мы генерируем изображение ⏰\n"
                               "Если что-то пойдет не так, мы вам сообщим 👌")
    data = await state.get_data()

    try:

        model_id = kadinsky_gen.get_model()
        width, height = data["set_size"].split("x")
        generating = kadinsky_gen.generate(model=model_id,
                                           prompt=msg.text,
                                           width=int(width),
                                           height=int(height))
        result = kadinsky_gen.check_generation(request_id=generating)

        if result:
            path = kadinsky_gen.save_image(result[0], f"telegram_{msg.from_user.id}")
            photo = FSInputFile(path)
            await msg.answer_photo(photo=photo,
                                   caption=msg.text,
                                   reply_markup=image_response_keyboard(user_id=msg.from_user.id))
            await message.delete()
        else:
            await message.edit_text("Простите, произошла ошибка 😔\n"
                                    "Убедитесь, что севрера kadinsky работают и ваш промт не является неподобающим и неприемлимым\n"
                                    "Если это продолжается, пожалуйста используйте /cancel",
                                    reply_markup=image_response_keyboard(user_id=msg.from_user.id))

    except Exception as ex:
        logging.log(msg=f"Get an exception for generating answer={ex}",
                    level=logging.ERROR)
    finally:
        logging.log(msg=f"Generated image for user_id={msg.from_user.id} with promt",
                    level=logging.INFO)
    await state.set_state(GeneratingImages.ready_to_generate)


async def cancefl_answering(msg: Message, state: FSMContext):
    """
    Canceling generating images for user
    Works on command /cancel
    :param msg: Message telegram object
    :param state: FSM state of bot
    :return:
    """
    current = await state.get_state()
    if current is None:
        return
    await state.clear()
    await msg.answer("Удача ✅\n"
                     "Диалог отменён!", reply_markup=delete_keyboard(admin_id=msg.from_user.id))
