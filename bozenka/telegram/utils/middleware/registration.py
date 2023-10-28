
'''
import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, ContentType
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bozenka.db import Users

class Registration(BaseMiddleware):
    """
    Checks, is user & group registered.
    """
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                result = await session.execute(select(Users).where(Users.user_id == event.from_user.id and Users.chat_id == event.chat.id))
                user = result.one_or_none()
                logging.log(msg=f"Checking user registration with id={event.from_user.id}", level=logging.INFO)
                if user is None:
                    logging.log(msg=f"Registering user into database with id={event.from_user.id}", level=logging.INFO)
                    user = Users(
                        user_id=event.from_user.id,
                        chat_id=event.chat.id
                    )
                    await session.merge(user)

        if not data:
            return await handler(event, None)
'''