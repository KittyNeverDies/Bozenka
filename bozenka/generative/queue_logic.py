import asyncio
import logging
from asyncio import Queue

from bozenka.generative.generative_dict import generative_dict


# A queue object, to store all queue async
queue = Queue()


async def proccess_queue_request(request_details: tuple, queue: Queue):
    """
    This function is used to process the one request
    of queue.
    :param request_details: tuple, contains the request details
    :param queue: Queue, the queue object
    :return: None
    """

    # Getting the dictionery of data
    data_dict = request_details[0]
    request_details_for_generation = request_details[1]
    await request_details_for_generation[-1].delete()
    del request_details_for_generation[-1]
    print(request_details_for_generation)

    await generative_dict[data_dict['category']][data_dict['name']].generate_telegram(*request_details_for_generation)
    # Removing the request from the queue
    queue.task_done()


async def process_queue() -> None:
    """
    An infinity loop to process the queue
    :return: None
    """

    while True:
        await asyncio.sleep(1)
        if not queue.empty():
            request_details = await queue.get()
            asyncio.create_task(proccess_queue_request(request_details, queue))
