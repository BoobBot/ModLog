from functools import wraps

from discord import Guild

from utils.db import config


def no_op():
    pass


def server_configured(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        e = next((o for o in args if isinstance(o, Guild) or hasattr(o, 'guild')), None)

        if not e:
            print(f'[SUSPICIOUS] No entities passed to {func.__name__} are, or contain a `Guild`!')
            return no_op()

        if hasattr(e, 'guild'):
            e = e.guild

        guild_id = str(e.id)
        g_conf = config.find_one({'_id': guild_id})

        if g_conf and g_conf.get('channel') is not None:
            log_channel_id = int(g_conf['channel'])
            log_channel = next(c for c in e.text_channels if c.id == log_channel_id)
            return await func(*args, **kwargs, log_channel=log_channel)

        return no_op()  # Guild has no config, or existing log channel.

    return wrapper
