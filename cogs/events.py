import asyncio
import logging
from itertools import cycle
from typing import Optional

import discord
from discord.ext import commands, tasks

import config
from db import database
from utils import voice, stream_check

logger = logging.getLogger(__name__)

class Events(commands.Cog):
    """Cog handling lifecycle events, voice state updates, and background monitoring."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.status_messages = cycle(config.BOT_STATUS)
        self.stream_task: Optional[asyncio.Task] = None

    @tasks.loop(seconds=15.0)
    async def rotate_presence(self):
        """Periodically cycles through rich presence status messages."""
        try:
            guild_count = len(self.bot.guilds)
            status_text = next(self.status_messages, f"Hits in {guild_count} servers")
            activity = discord.Activity(
                type=discord.ActivityType.listening,
                name=f"{status_text} | /help"
            )
            await self.bot.change_presence(activity=activity)
        except Exception as e:
            logger.debug(f"Error rotating presence: {e}")

    @rotate_presence.before_loop
    async def before_rotate_presence(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        """Lifecycle hook when the bot connects and is fully ready."""
        logger.info(f"Logged in as {self.bot.user.name}#{self.bot.user.discriminator} (ID: {self.bot.user.id})")
        logger.info(f"Connected to {len(self.bot.guilds)} guilds.")

        # Setup database
        await database.setup_db()

        # Start presence cycle
        if not self.rotate_presence.is_running():
            self.rotate_presence.start()

        # Sync application commands
        try:
            synced = await self.bot.tree.sync()
            logger.info(f"Successfully synced {len(synced)} application command(s).")
        except Exception as e:
            logger.error(f"Failed to sync slash commands with Discord: {e}")

        # Auto-reconnect to saved voice channels from previous session
        await self.restore_saved_voice_connections()

        # Start proactive 24/7 stream health watchdog if not already running
        if self.stream_task is None or self.stream_task.done():
            self.stream_task = asyncio.create_task(stream_check.check_stream_loop(self.bot))

    async def restore_saved_voice_connections(self):
        """Restores voice playback in guilds stored in database after restart or crash."""
        saved_channels = await database.get_saved_channels()
        if not saved_channels:
            return

        logger.info(f"Found {len(saved_channels)} saved voice connection(s). Restoring...")
        for guild_id, channel_id in saved_channels:
            try:
                guild = self.bot.get_guild(guild_id)
                if not guild:
                    continue

                channel = guild.get_channel(channel_id)
                if isinstance(channel, (discord.VoiceChannel, discord.StageChannel)):
                    logger.info(f"Reconnecting to '{channel.name}' in guild '{guild.name}'...")
                    await voice.join_and_play(channel, guild)
                    await asyncio.sleep(1.0)  # Rate-limit safety pause between reconnects
            except Exception as e:
                logger.error(f"Failed restoring voice state in guild {guild_id}: {e}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """Tracks bot voice state changes without erasing 24/7 channel memory on drops."""
        if member != self.bot.user:
            return

        # Case 1: Temporary disconnect or server migration
        # Note: Do NOT erase the channel from database! The watchdog will auto-recover it.
        if before.channel and not after.channel:
            logger.warning(f"Bot voice connection dropped from '{before.channel.name}' in '{before.channel.guild.name}'. The 24/7 watchdog will restore it.")

        # Case 2: Bot was moved to another channel within the guild
        elif after.channel and before.channel != after.channel:
            logger.info(f"Bot moved to '{after.channel.name}' in '{after.channel.guild.name}'. Updating saved state.")
            await database.save_state(after.channel.guild.id, after.channel.id)
            await asyncio.sleep(0.5)
            if after.channel.guild.voice_client and not after.channel.guild.voice_client.is_playing():
                await voice.play_audio(after.channel.guild.voice_client)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        """Clean up saved voice state if the voice channel was deleted."""
        if isinstance(channel, (discord.VoiceChannel, discord.StageChannel)):
            saved_channels = await database.get_saved_channels()
            for guild_id, channel_id in saved_channels:
                if channel.id == channel_id:
                    logger.info(f"Channel '{channel.name}' ({channel.id}) was deleted. Removing state.")
                    await database.remove_state(guild_id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        """Clean up saved voice state if the bot is removed/kicked from a guild."""
        logger.info(f"Bot was removed from guild '{guild.name}' ({guild.id}). Cleaning up state.")
        await database.remove_state(guild.id)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Responds with helpful command guidance when the bot is mentioned."""
        if message.author.bot:
            return

        if self.bot.user in message.mentions and not message.mention_everyone:
            embed = discord.Embed(
                title="📻 HitRadio is Online!",
                description=(
                    "Hey there! Ready for nonstop 100% Hits?\n\n"
                    "• Use `/play` to start streaming in your voice channel.\n"
                    "• Use `/help` to see all available commands.\n"
                    "• Use `/volume` to adjust playback level."
                ),
                color=config.EMBED_COLOR
            )
            await message.reply(embed=embed)

    def cog_unload(self):
        """Cleans up background loops and tasks when cog is unloaded."""
        self.rotate_presence.cancel()
        if self.stream_task:
            self.stream_task.cancel()

async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
