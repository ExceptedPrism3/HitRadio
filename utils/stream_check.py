import asyncio
import logging

import aiohttp

from private.essentials import STREAM_LINK


# Function to check if the stream link is working
async def is_stream_working():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(STREAM_LINK) as response:
                return response.status == 200
    except aiohttp.ClientError as e:
        logging.error(f"Network error checking stream link: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False


# Function to check the stream periodically and restart if needed
async def check_stream(bot, db_path, restart_audio_stream, save_state):
    # Wait until the bot is ready
    await bot.wait_until_ready()
    # Continue checking as long as the bot is running
    while not bot.is_closed():
        # Iterate through each guild the bot is connected to
        for guild in bot.guilds:
            # Get the voice client for the guild
            voice_client = guild.voice_client
            # Check if the bot is connected to a voice channel and not playing
            if voice_client and voice_client.is_connected():
                if not voice_client.is_playing():
                    # Check if the stream link is working
                    if await is_stream_working():
                        # Restart the audio stream in the guild's voice channel
                        await restart_audio_stream(guild)
                        # Save the state to the database
                        await save_state(db_path, guild.id, voice_client.channel.id)
        # Wait for a specified interval before checking again
        await asyncio.sleep(60)
