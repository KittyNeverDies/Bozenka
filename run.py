import asyncio
import logging

from bozenka import launch_instances

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                        )
    logging.log(msg="Starting bozenka, lets go!", level=logging.INFO)
    try:
        asyncio.run(launch_instances())
    except (KeyboardInterrupt, SystemExit, RuntimeError):
        print("INFO: Bot closed")
    except ConnectionError:
        print("INFO: No internet connection for now")
