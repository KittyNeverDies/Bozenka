import asyncio
import logging

import g4f

from bozenka.instances.telegram import launch_telegram_instance
from bozenka.database import generate_url, get_async_engine, get_sessions_maker


def launch_instances() -> None:
    """
    Launches bozenka instances, working async
    :return:
    """
    logging.log(msg="Setting up g4f logging!", level=logging.INFO)
    logging.basicConfig(level=logging.INFO)
    logging.log(msg="Setting up logging!", level=logging.INFO)
    g4f.logging = True

    db_url = generate_url()
    engine = get_async_engine(db_url)
    session_maker = get_sessions_maker(engine)
    asyncio.run(launch_telegram_instance(session_maker))

    logging.log(msg="Launched all instances!", level=logging.INFO)
