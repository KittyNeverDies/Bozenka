import asyncio
import logging

import g4f

from bozenka.telegram import launch_telegram_instance
from bozenka.db import generate_url, get_async_engine, get_sessions_maker
import threading


def launch_instances() -> None:
    """
    Launches bozenka instances, working async
    :return:
    """
    logging.log(msg="Setting up g4f logging!", level=logging.INFO)
    g4f.logging = True

    db_url = generate_url()
    engine = get_async_engine(db_url)
    session_maker = get_sessions_maker(engine)
    asyncio.run(launch_telegram_instance(session_maker))

    logging.log(msg="Launched all instances!", level=logging.INFO)
