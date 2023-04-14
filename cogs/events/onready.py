import asyncio
from itertools import cycle

import discord
import lavalink
from discord.ext import commands, tasks

from private.essentials import BOT_STATUS, LAVA_HOST, LAVA_PORT, LAVA_PASSWORD, LAVA_REGION, LAVA_NAME


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status = cycle(BOT_STATUS)

    @tasks.loop(seconds=10.0)
    async def change_status(self):
        activity = next(self.status)
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=activity))

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} has started')
        print('--------------------------')
        total_servers_line = f'Hits with {len(self.bot.guilds)} servers'
        BOT_STATUS.append(total_servers_line)
        self.change_status.start()
        self.bot.lavalink = lavalink.Client(self.bot.user.id)
        self.bot.lavalink.add_node(LAVA_HOST, LAVA_PORT, LAVA_PASSWORD, LAVA_REGION, LAVA_NAME)
        lavalink.add_event_hook(self.track_hook)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.WebSocketClosedEvent):
            if int(event.code) == 4006 and event.player.channel_id is not None:
                print(event.code)
                guild = self.bot.get_guild(int(event.player.guild_id))
                channel = self.bot.get_channel(event.player.channel_id)
                if not channel:
                    return
                await guild.change_voice_state(channel=channel)
            if int(event.code) == 4000 or int(event.code) == 1006:
                await asyncio.sleep(5)


def setup(bot):
    bot.add_cog(Status(bot))
