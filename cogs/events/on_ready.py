import asyncio
from itertools import cycle

import discord
from discord.ext import commands, tasks

from db import voice_channel_database
from private.essentials import BOT_STATUS
from utils import audio, stream_check


# Cog that handles events when the bot is ready
class OnReady(commands.Cog):
    def __init__(self, bot):
        # Initialization with bot instance, status messages, and database path
        self.bot = bot
        self.status_messages = cycle(BOT_STATUS)
        self.db_path = 'bot.db'
        self.check_stream_task = None  # Task to check the stream status

    @tasks.loop(seconds=10.0)
    async def change_status(self):
        # Task to periodically change the bot's status message
        total_servers_line = f'Hits with {len(self.bot.guilds)} servers'
        activity = next(self.status_messages) if self.status_messages else total_servers_line
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity))

    @commands.Cog.listener()
    async def on_ready(self):
        # Called when the bot becomes ready after starting up
        print(f'{self.bot.user} has started')
        self.change_status.start()  # Start the status change task
        await self.bot.tree.sync()  # Sync the bot's commands with Discord
        await voice_channel_database.setup_db(self.db_path)  # Setup the voice channel database
        await self.initial_connect()  # Connect to voice channels based on saved states
        self.start_check_stream_task()  # Start the task to check the audio stream

    async def initial_connect(self):
        # Connects the bot to previously joined voice channels from the database
        channels = await voice_channel_database.get_initial_channels(self.db_path)
        for guild_id, channel_id in channels:
            guild = self.bot.get_guild(guild_id)
            if guild:
                channel = guild.get_channel(channel_id)
                if channel:
                    await audio.join_and_play(channel, guild)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Handles voice state updates, especially for the bot itself
        if member == self.bot.user:
            if before.channel and not after.channel:
                # Bot left a channel; remove its state from the database
                await voice_channel_database.remove_state(self.db_path, before.channel.guild.id)
            elif after.channel:
                # Bot joined a new channel; restart the audio stream
                await asyncio.sleep(1)  # Wait briefly for stable connection
                await audio.restart_audio_stream(after.channel.guild)
                await voice_channel_database.save_state(self.db_path, after.channel.guild.id, after.channel.id)

    def start_check_stream_task(self):
        # Starts a new task for checking the stream if it's not already running
        if self.check_stream_task is None or self.check_stream_task.done():
            self.check_stream_task = self.bot.loop.create_task(
                stream_check.check_stream(self.bot, self.db_path, audio.restart_audio_stream,
                                          voice_channel_database.save_state)
            )

    def cog_unload(self):
        # Cleanup when the cog is unloaded
        if self.check_stream_task:
            self.check_stream_task.cancel()  # Cancel the stream check task if it exists


async def setup(bot):
    # Setup function to add the OnReady cog to the bot
    await bot.add_cog(OnReady(bot))
