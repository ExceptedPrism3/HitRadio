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
    """Performs a quick HTTP HEAD/GET probe to verify the stream server is healthy."""
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

async def check_stream_loop(bot: commands.Bot, interval_seconds: int = 60) -> None:
    """
    Background watchdog that regularly inspects all connected voice clients.
    If a stream stalled or dropped while the bot is supposed to be playing,
    it verifies stream health and restarts playback automatically.
    """
    await bot.wait_until_ready()
    logger.info("Stream health watchdog loop started.")

    while not bot.is_closed():
        try:
            for guild in bot.guilds:
                voice_client = guild.voice_client
                # Bot is connected, but not actively playing and not deliberately paused
                if voice_client and voice_client.is_connected() and not voice_client.is_playing() and not voice_client.is_paused():
                    logger.warning(f"Voice client in guild '{guild.name}' ({guild.id}) is idle. Checking stream...")
                    healthy = await is_stream_working()
                    if healthy:
                        logger.info(f"Stream is reachable. Restarting playback for guild '{guild.name}'...")
                        await voice.restart_audio_stream(guild)
                        await database.save_state(guild.id, voice_client.channel.id)
                    else:
                        logger.warning("Stream is currently unreachable from host network. Will retry next cycle.")
        except Exception as e:
            logger.error(f"Error in stream health watchdog iteration: {e}")

        await asyncio.sleep(interval_seconds)
