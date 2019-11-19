"""
Provides log coverage of message-related events.
"""

from discord.ext import commands
from discord.ext.commands import Cog


class MessageLog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_edit(self, before, after):
        ...

    @Cog.listener()
    async def on_message_delete(self, message):
        ...


def setup(bot):
    bot.add_cog(MessageLog(bot))
