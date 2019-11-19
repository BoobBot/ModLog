"""
Provides log coverage of message-related events.
"""

from discord.ext import commands
from discord.ext.commands import Cog

from utils.decorators import server_configured
from utils.time import now


class MessageLog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    @server_configured
    async def on_message_edit(self, before, after, log_channel):
        if len(after) == 0:
            return

        msg = f'📝 `{now()}` **Message Edited** (ID: `{before.id}`)\n' \
              f'**Channel:** {before.channel.mention} (`{before.channel.id}`)\n' \
              f'**Author:** {before.author} (`{before.author.id}`)\n' \
              f'**Before:** {before.clean_content}\n' \
              f'**After:** {after.clean_content}'
        await log_channel.send(msg)

    @Cog.listener()
    @server_configured
    async def on_message_delete(self, message, log_channel):
        msg = f'📝 `{now()}` **Message Deleted** (ID: `{message.id}`)\n' \
              f'**Channel:** {message.channel.mention} (`{message.channel.id}`)\n' \
              f'**Author:** {message.author} (`{message.author.id}`)\n' \
              f'**Content:** {message.clean_content}'
        await log_channel.send(msg)


def setup(bot):
    bot.add_cog(MessageLog(bot))
