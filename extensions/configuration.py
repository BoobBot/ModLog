import discord
from discord.ext import commands
from discord.ext.commands import Cog, errors

from utils.db import config


class Configuration(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, (errors.MissingRequiredArgument, errors.BadArgument)):
            if isinstance(error, errors.MissingRequiredArgument):
                msg = f'You need to specify `{error.param.name}`'
            elif isinstance(error, errors.BadArgument):
                msg = error.args[0].replace('"', '`')

            msg += f'\n\nUse `{ctx.prefix}help {ctx.command}` to view the syntax of the command'

            await ctx.send(msg)
        elif isinstance(error, errors.MissingPermissions):
            permissions = '\n'.join(f'- {p.title().replace("_", " ")}' for p in error.missing_perms)
            await ctx.send(f'**You need the following permissions:**\n{permissions}')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def channel(self, ctx, channel: discord.TextChannel):
        """ Sets the channel used for logging events. """
        config.update_one({'_id': str(ctx.guild.id)},
                          {'$set': {'channel': str(channel.id)}},
                          True)
        await ctx.send(f'Channel set to {channel.mention}')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def disable(self, ctx):
        """ Disables logging on the server. """
        config.delete_one({'_id': str(ctx.guild.id)})
        await ctx.send('Logging disabled.')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def status(self, ctx):
        """ Displays the current logging status. """
        g_conf = config.find_one({'_id': str(ctx.guild.id)})

        if not g_conf or not g_conf['channel']:
            return await ctx.send('Logging is not enabled in this server.')

        channel_id = int(g_conf['channel'])
        channel = next((c for c in ctx.guild.text_channels if c.id == channel_id), None)

        if not channel:
            return await ctx.send('Logging was previously enabled in the server, but the channel no longer exists.')

        await ctx.send(f'Currently logging to {channel.mention}')


def setup(bot):
    bot.add_cog(Configuration(bot))
