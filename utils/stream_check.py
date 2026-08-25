import asyncio
import logging
import aiohttp
import discord
from discord.ext import commands

import config
from db import database
from utils import voice

logger = logging.getLogger(__name__)

async def is_stream_working(stream_url: str = config.STREAM_URL) -> bool:
    """Performs a quick HTTP GET probe to verify the stream server is healthy."""
    try:
        timeout = aiohttp.ClientTimeout(total=8)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(stream_url) as response:
                return response.status == 200
    except aiohttp.ClientError as e:
        logger.warning(f"Network error checking radio stream URL: {e}")
        return False
    except Exception as e:
        logger.warning(f"Unexpected error probing stream: {e}")
        return False

async def check_stream_loop(bot: commands.Bot, interval_seconds: int = 30) -> None:
    """
    Proactive 24/7 background watchdog that:
    1. Reconnects the bot if Discord dropped the voice connection.
    2. Restarts audio playback if the stream stalled or encountered EOF/error.
    3. Keeps SQLite state and Discord voice connections synchronized.
    """
    await bot.wait_until_ready()
    logger.info("Proactive 24/7 stream watchdog loop started.")

    while not bot.is_closed():
        try:
            # Check stream URL reachability
            healthy = await is_stream_working()
            if not healthy:
                logger.warning("Radio stream server is temporarily unreachable. Retrying in next watchdog cycle...")
                await asyncio.sleep(interval_seconds)
                continue

            # Query all channels that should be actively streaming
            saved_channels = await database.get_saved_channels()

            for guild_id, channel_id in saved_channels:
                guild = bot.get_guild(guild_id)
                if not guild:
                    # Bot is no longer in this guild
                    logger.info(f"Guild {guild_id} not found in bot cache. Cleaning up state.")
                    await database.remove_state(guild_id)
                    continue

                channel = guild.get_channel(channel_id)
                if not channel or not isinstance(channel, (discord.VoiceChannel, discord.StageChannel)):
                    # Voice channel was deleted
                    logger.info(f"Voice channel {channel_id} in '{guild.name}' does not exist anymore. Cleaning up state.")
                    await database.remove_state(guild_id)
                    continue

                voice_client = guild.voice_client

                # Case 1: Bot got disconnected (Discord server restart, region shift, or network drop)
                if not voice_client or not voice_client.is_connected():
                    logger.info(f"[Watchdog Auto-Recovery] Reconnecting to '{channel.name}' in guild '{guild.name}' ({guild.id})...")
                    try:
                        await voice.join_and_play(channel, guild)
                        await asyncio.sleep(1.0)
                    except Exception as conn_err:
                        logger.error(f"Failed auto-reconnecting to {channel.name}: {conn_err}")

                # Case 2: Bot is connected to the channel, but playback stopped unexpectedly and is not paused
                elif not voice_client.is_playing() and not voice_client.is_paused():
                    logger.info(f"[Watchdog Auto-Recovery] Resuming stalled stream in guild '{guild.name}'...")
                    try:
                        await voice.restart_audio_stream(guild)
                    except Exception as play_err:
                        logger.error(f"Failed restarting stream in {guild.name}: {play_err}")

                # Case 3: Bot was moved to another channel in the same guild
                elif voice_client and voice_client.is_connected() and voice_client.channel and voice_client.channel.id != channel_id:
                    logger.info(f"Synchronizing updated voice channel in '{guild.name}' to '{voice_client.channel.name}'.")
                    await database.save_state(guild.id, voice_client.channel.id)

        except Exception as e:
            logger.error(f"Error in stream health watchdog iteration: {e}")

        await asyncio.sleep(interval_seconds)
