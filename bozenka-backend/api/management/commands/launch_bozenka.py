import asyncio
import logging
import sys
import uvicorn
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from features import get_list_of_features
from social.dsc import launch_discord_bot_instance
from social.vkontakte import launch_vk_bot_instance
from social.telegram import launch_telegram_bot_instance

class Command(BaseCommand):
    help = 'Run Django server with bots'

    def handle(self, *args, **kwargs):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            stream=sys.stdout
        )

        # Load environment variables
        load_dotenv()

        # Run both the server and bots
        try:
            asyncio.run(self.run_all())
        except KeyboardInterrupt:
            logging.info("We got Keyboard Interrupt error, probably due to CTRL+C, server shutting down or intervention to proccess")

    async def launch_instances(self) -> None:
        features = get_list_of_features()

        discord_task = asyncio.create_task(launch_discord_bot_instance(features))
        vk_task = asyncio.create_task(launch_vk_bot_instance(features))
        telegram_task = asyncio.create_task(launch_telegram_bot_instance(features))

        await asyncio.wait([telegram_task, vk_task, discord_task])

    async def run_server(self):
        config = uvicorn.Config(
            "bozenka.asgi:application",
            host="127.0.0.1",  # Use localhost instead of 0.0.0.0
            port=8000,
            reload=True
        )
        server = uvicorn.Server(config)
        await server.serve()

    async def run_all(self):
        # Create tasks for both the server and bots
        server_task = asyncio.create_task(self.run_server())
        bots_task = asyncio.create_task(self.launch_instances())

        # Wait for both tasks
        await asyncio.gather(server_task, bots_task)
