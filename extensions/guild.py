"""
Provides log coverage of guild-related events.
"""
import discord
from discord.ext import commands
from discord.ext.commands import Cog

from utils.db import invites
from utils.decorators import server_configured
from utils.time import now


class GuildLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.synced_invites = False

    @Cog.listener()
    async def on_ready(self):
        if self.synced_invites:
            return

        print('Syncing invites for all guilds...')
        self.synced_invites = True

        for g in self.bot.guilds:
            await self.sync_invites_for(g)

        print('Invites synced.')

    async def sync_invites_for(self, guild):
        if not guild.me.guild_permissions.manage_guild:
            return

        try:
            guild_invites = await guild.invites()
        except discord.HTTPException:
            return
        else:
            for i in guild_invites:
                invites.update_one({'guild': str(guild.id), 'code': i.code}, {'$set': {'uses': i.uses}}, True)

    async def determine_used_invite(self, guild):
        if not guild.me.guild_permissions.manage_guild:
            return None

        cached_invites = invites.find({'guild': str(guild.id)})
        guild_invites = await guild.invites()

        if not cached_invites:
            if len(guild_invites) > 0:
                await self.sync_invites_for(guild)
            return None

        cached_invite_dict = {
            i['code']: i
            for i in cached_invites
        }
        cached_codes = [i['code'] for i in cached_invites]
        guild_codes = [i.code for i in guild_invites]

        added = sum(1 for code in guild_codes if code not in cached_codes)
        removed = sum(1 for code in cached_codes if code not in guild_codes)

        used = next((i for i in guild_invites if i.code in cached_invite_dict and i.uses > cached_invite_dict[i.code]['uses']),
                    None)

        await self.sync_invites_for(guild)

        if used:
            return used

        if added == 1 and removed == 0:  # None were removed, but 1 was added. Chances are, the member joined with the new invite.
            return next(i for i in guild_invites if i.code not in cached_codes)

        return None  # Unable to distinguish, too many added/removed.

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
              f'**Member:** {member} (`{member.id}`)\n'

        invite = await self.determine_used_invite(member.guild)

        if invite is not None:
            msg += f'**Invite Used:** `{invite.code}` (`{invite.uses}` uses, created by {invite.inviter} (`{invite.inviter.id}`))\n'

        msg += f'**Total Members:** `{member.guild.member_count}`'
        await log_channel.send(msg)

    @Cog.listener()
    @server_configured
    async def on_member_remove(self, member, log_channel):
        msg = f'❎ `{now()}` **Member Left/Kicked**\n' \
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
