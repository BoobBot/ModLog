"""
Provides log coverage of guild-related events.
"""

from discord.ext import commands
from discord.ext.commands import Cog

from utils.decorators import server_configured


class GuildLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # On ready, create a registry of all invites in a guild.

    @Cog.listener()
    async def on_ready(self):
        print('Connected to discord!!!')

    @server_configured
    @Cog.listener()
    async def on_guild_update(self, before, after):
        print('hi mom')

    @Cog.listener()
    async def on_member_join(self, member):
        ...

    @Cog.listener()
    async def on_member_remove(self, member):
        ...

    @Cog.listener()
    async def on_member_update(self, before, after):
        ...

    @Cog.listener()
    async def on_member_ban(self, guild, member):
        ...

    @Cog.listener()
    async def on_member_unban(self, guild, member):
        ...


def setup(bot):
    bot.add_cog(GuildLog(bot))
