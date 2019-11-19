import json
import os
import traceback

import discord
from discord.ext import commands

with open('config.json') as f:
    config = json.load(f)


class Bot(commands.AutoShardedBot):
    def __init__(self, **options):
        super().__init__(**options)
        self._load_cogs()

    def _load_cogs(self):
        for ext in os.listdir('extensions'):
            if ext.endswith('.py'):
                try:
                    self.load_extension(f'extensions.{ext[:-3]}')
                except (ImportError, SyntaxError, discord.ClientException):
                    traceback.print_exc()

    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)


bot = Bot(command_prefix=config.get('prefixes'))
bot.run(config.get('token'))
