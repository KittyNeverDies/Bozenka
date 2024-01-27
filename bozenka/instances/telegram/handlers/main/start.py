from aiogram.enums import ChatType
from aiogram.types import Message as Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bozenka.instances.telegram.utils.keyboards import help_keyboard, start_keyboard


async def start_cmd(msg: Message) -> None:
    """
    /start command function handler
    Shows menu and basic information about bozenka
    :param msg: Message telegram object
    :return: Nothing
    """
    await msg.answer(
        """
        Привет 👋
Я - бозенька, бот с открытым исходным кодом, который поможет тебе в различных задачах. 
    
Вот что ты можешь сделать с помощью меню:
• Добавить в чат: добавляет меня в групповой чат, чтобы я мог выполнять свои функции внутри него.
• Функционал: показывает список доступных функций и команд, которые я могу выполнить.
• О разработчиках: предоставляет информацию о команде разработчиков, которые создали и поддерживают этого бота.
• О запущенном экземпляре: выводит информацию о текущей версии и состоянии запущенного экземпляра бота.
• Начать диалог с ИИ: позволяет начать диалог с искусственным интеллектом, который может отвечать на вопросы и предоставлять информацию.
• Генерация изображений: позволяет сгенерировать изображения на основе заданных параметров и промта
    
Вот нужные ссылки обо мне:
• <a href='https://t.me/bozodevelopment'>Канал с новостями об разработке</a>
• <a href='https://github.com/kittyneverdies/bozenka/'>Исходный код на Github</a>
    
Чтобы воспользоваться какой-либо функцией, просто нажми на соответствующую кнопку ниже. 
Если у тебя возникнут вопросы или проблемы, не стесняйся обратиться к команде разработчиков или написать в обсуждении телеграм канала. 
Удачного использования!
        """,
        reply_markup=start_keyboard(), disable_web_page_preview=True)
