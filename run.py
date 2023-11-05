import asyncio
import logging

import g4f
from gpt4all import GPT4All

from bozenka import launch_instances

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.log(msg="Starting bozenka, lets go!", level=logging.INFO)
    try:
        launch_instances()
    except (KeyboardInterrupt, SystemExit, RuntimeError):
        print("INFO: Bot closed")
    except ConnectionError:
        print("INFO: No internet connection for now")
