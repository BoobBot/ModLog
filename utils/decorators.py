from functools import wraps

from discord import Guild

from utils.db import config


def server_configured(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        e = next((o for o in args if isinstance(o, Guild) or hasattr(o, 'guild')), None)

        if not e:
            print(f'[SUSPICIOUS] No entities passed to {func.__name__} are, or contain a `Guild`!')
            return

        if hasattr(e, 'guild'):
            e = e.guild

        guild_id = str(e.id)
        g_conf = config.find_one({'_id': guild_id})

        if g_conf and g_conf.get('channel') is not None:
            log_channel_id = int(g_conf['channel'])
            log_channel = next(c for c in e.text_channels if c.id == log_channel_id)

            if 'log_channel' in func.__code__.co_varnames:
                return await func(*args, **kwargs, log_channel=log_channel)

            return await func(*args, **kwargs)

        return  # Guild has no config, or existing log channel.

    return wrapper
