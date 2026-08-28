import asyncio
import gc
import logging
from typing import Dict
import aiohttp
import discord
from discord.ext import commands

import config
from db import database
from utils import voice

logger = logging.getLogger(__name__)

# Tracks consecutive failed connection attempts per guild to prevent retry spam
_failed_attempts: Dict[int, int] = {}

async def is_stream_working(stream_url: str = config.STREAM_URL) -> bool:
    """Performs a quick HTTP GET probe to verify the stream server is healthy."""
    try:
        timeout = aiohttp.ClientTimeout(total=8)
        headers = {"User-Agent": "HitRadioDiscordBot/4.0"}
        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
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
    Proactive 24/7 background watchdog:
    1. Reconnects the bot if Discord disconnected the voice connection (with exponential backoff on permission failures).
    2. Resumes audio playback seamlessly if the stream stalled, without dropping the Discord voice call.
    3. Keeps SQLite state synchronized.
    """
    await bot.wait_until_ready()
    logger.info("Proactive 24/7 stream watchdog loop started.")

    iteration = 0

    while not bot.is_closed():
        iteration += 1

        # Periodically trigger garbage collection every 10 minutes to maintain rock-solid low memory
        if iteration % 20 == 0:
            gc.collect()

        try:
            # Check stream reachability
            healthy = await is_stream_working()
            if not healthy:
                logger.warning("Radio stream server is temporarily unreachable. Retrying next cycle...")
                await asyncio.sleep(interval_seconds)
                continue

            # Query all channels that should be actively streaming
            saved_channels = await database.get_saved_channels()

            for guild_id, channel_id in saved_channels:
                guild = bot.get_guild(guild_id)
                if not guild:
                    # Bot was removed from guild
                    logger.info(f"Guild {guild_id} not found in bot cache. Cleaning up state.")
                    await database.remove_state(guild_id)
                    _failed_attempts.pop(guild_id, None)
                    continue

                channel = guild.get_channel(channel_id)
                if not channel or not isinstance(channel, (discord.VoiceChannel, discord.StageChannel)):
                    # Voice channel was deleted
                    logger.info(f"Voice channel {channel_id} in '{guild.name}' no longer exists. Cleaning up state.")
                    await database.remove_state(guild_id)
                    _failed_attempts.pop(guild_id, None)
                    continue

                # Validate permissions before touching voice connection
                permissions = channel.permissions_for(guild.me)
                if not permissions.connect or not permissions.speak or not permissions.view_channel:
                    fails = _failed_attempts.get(guild_id, 0) + 1
                    _failed_attempts[guild_id] = fails

                    # If missing permissions repeatedly, back off to once every 10 cycles (5 minutes)
                    if fails % 10 == 1:
                        logger.warning(
                            f"Missing Connect/Speak permissions in '{channel.name}' ({guild.name}). "
                            "Backing off auto-reconnect retries until permissions are granted."
                        )
                    continue

                voice_client = guild.voice_client

                # Case 1: Bot is disconnected from voice
                if not voice_client or not voice_client.is_connected():
                    fails = _failed_attempts.get(guild_id, 0)
                    if fails >= 3 and iteration % 6 != 0:
                        # Back off retries for temporarily unroutable Discord voice regions
                        continue

                    logger.info(f"[Watchdog Auto-Recovery] Reconnecting to '{channel.name}' in '{guild.name}' ({guild.id})...")
                    try:
                        vc = await voice.join_and_play(channel, guild)
                        if vc and vc.is_connected():
                            _failed_attempts.pop(guild_id, None)
                        else:
                            _failed_attempts[guild_id] = fails + 1
                        await asyncio.sleep(1.0)
                    except Exception as conn_err:
                        _failed_attempts[guild_id] = fails + 1
                        logger.error(f"Failed auto-reconnecting to {channel.name}: {conn_err}")

                # Case 2: Bot is connected to the channel, but playback stalled/stopped unexpectedly
                elif not voice_client.is_playing() and not voice_client.is_paused():
                    logger.info(f"[Watchdog Auto-Recovery] Resuming stalled stream in '{guild.name}' (retaining voice call)...")
                    try:
                        await voice.restart_audio_stream(guild)
                        _failed_attempts.pop(guild_id, None)
                    except Exception as play_err:
                        logger.error(f"Failed restarting stream in {guild.name}: {play_err}")

                # Case 3: Bot was moved to another channel within the guild
                elif voice_client and voice_client.is_connected() and voice_client.channel and voice_client.channel.id != channel_id:
                    logger.info(f"Synchronizing voice channel in '{guild.name}' to '{voice_client.channel.name}'.")
                    await database.save_state(guild.id, voice_client.channel.id)
                    _failed_attempts.pop(guild_id, None)

        except Exception as e:
            logger.error(f"Error in stream health watchdog iteration: {e}")

        await asyncio.sleep(interval_seconds)
