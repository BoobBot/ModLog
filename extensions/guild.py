"""
Provides log coverage of guild-related events.
"""

from discord.ext import commands
from discord.ext.commands import Cog

from utils.decorators import server_configured
from utils.time import now


class GuildLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # On ready, create a registry of all invites in a guild.

    @Cog.listener()
    async def on_ready(self):
        print('Connected to discord!!!')

    @Cog.listener()
    @server_configured
    async def on_guild_update(self, before, after, log_channel):
        msg = f'🌐 `{now()}` **Guild Updated**\n'

        if before.name != after.name:
            msg += f'**Name:** {before.name} **->** {after.name}\n'

        if before.region != after.region:
            msg += f'**Region:** {before.region} **->** {after.region}\n'

        if before.icon != after.icon:
            msg += f'**Icon:** <{before.icon_url}> **->** <{after.icon_url}>'

        await log_channel.send(msg)

    @Cog.listener()
    @server_configured
    async def on_guild_emojis_update(self, guild, before, after, log_channel):
        msg = f'🌐 `{now()}` **Emojis Updated**\n'
        added = next((e for e in after if e not in before), None)
        removed = next((e for e in before if e not in after), None)

        if added:
            msg += f'Added {added}\n'

        if removed:
            msg += f'Removed {removed.name} (`{removed.id}`)\n'

        await log_channel.send(msg)

    @Cog.listener()
    @server_configured
    async def on_member_join(self, member, log_channel):
        msg = f'✅ `{now()}` **Member Joined**\n' \
              f'**Member:** {member} (`{member.id}`)\n' \
              f'**Total Members:** `{member.guild.member_count}`'
        await log_channel.send(msg)
        # track invites and sync

    @Cog.listener()
    @server_configured
    async def on_member_remove(self, member, log_channel):
        msg = f'✅ `{now()}` **Member Left/Kicked**\n' \
              f'**Member:** {member} (`{member.id}`)\n' \
              f'**Total Members:** `{member.guild.member_count}`'
        await log_channel.send(msg)

    @Cog.listener()
    @server_configured
    async def on_member_update(self, before, after, log_channel):
        msg = f'🙎🏽 `{now()}` **Member Updated**\n' \
              f'**Member:** {before} (`{before.id}`)\n'

        changes = False

        if before.name != after.name:
            changes = True
            msg += f'**Username:** {before.name} **->** {after.name}\n'

        if before.nick != after.nick:
            changes = True
            msg += f'**Nickname:** {before.nick} **->** {after.nick}\n'

        if before.roles != after.roles:
            changes = True
            msg += '**Roles:**\n'
            added = [r.name for r in after.roles if r not in before.roles]
            removed = [r.name for r in before.roles if r not in after.roles]

            if added:
                msg += f'• Added: {", ".join(added)}\n'

            if removed:
                msg += f'• Removed: {", ".join(removed)}\n'

        if not before.bot and before.avatar != after.avatar:
            changes = True
            msg += f'**Avatar:** <{before.avatar_url}> **->** <{after.avatar_url}>'

        if changes:
            await log_channel.send(msg)

    @Cog.listener()
    @server_configured
    async def on_member_ban(self, guild, member, log_channel):
        msg = f'🔨 `{now()}` **Member Banned**\n' \
              f'**Member:** {member} (`{member.id}`)'

        await log_channel.send(msg)

    @Cog.listener()
    @server_configured
    async def on_member_unban(self, guild, member, log_channel):
        msg = f'🕊 `{now()}` **Member Unbanned**\n' \
              f'**Member:** {member} (`{member.id}`)'

        await log_channel.send(msg)


def setup(bot):
    bot.add_cog(GuildLog(bot))
