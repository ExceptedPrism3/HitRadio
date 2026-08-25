import asyncio
import logging
from typing import Optional

import discord
import config

logger = logging.getLogger(__name__)

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

def create_audio_source(stream_url: str = config.STREAM_URL, volume: float = 1.0) -> discord.PCMVolumeTransformer:
    """Creates a FFmpeg audio source wrapped in a PCM volume transformer."""
    audio_source = discord.FFmpegPCMAudio(stream_url, **FFMPEG_OPTIONS)
    return discord.PCMVolumeTransformer(audio_source, volume=volume)

def handle_playback_error(error: Optional[Exception], voice_client: discord.VoiceClient) -> None:
    """Callback triggered if FFmpeg stream encounters an error or ends unexpectedly."""
    if error:
        logger.error(f"FFmpeg audio playback error in guild {voice_client.guild.id}: {error}")
    
    # If the bot is still connected and not intentionally stopped, attempt stream restart
    if voice_client and voice_client.is_connected() and not voice_client.is_playing() and not voice_client.is_paused():
        logger.info(f"Attempting to auto-recover stream in guild {voice_client.guild.name} ({voice_client.guild.id})...")
        try:
            loop = voice_client.client.loop
            if loop.is_running():
                asyncio.run_coroutine_threadsafe(restart_audio_stream(voice_client.guild), loop)
        except Exception as ex:
            logger.error(f"Failed to trigger auto-recovery task: {ex}")

async def play_audio(voice_client: discord.VoiceClient, stream_url: str = config.STREAM_URL, volume: float = 1.0) -> bool:
    """Starts playback of the radio stream on the given voice client."""
    if not voice_client or not voice_client.is_connected():
        logger.warning("Cannot play audio: voice client is disconnected.")
        return False

    try:
        if voice_client.is_playing():
            voice_client.stop()

        source = create_audio_source(stream_url, volume=volume)
        voice_client.play(source, after=lambda e: handle_playback_error(e, voice_client))
        return True
    except Exception as e:
        logger.error(f"Error starting audio stream in guild {voice_client.guild.id}: {e}")
        return False

async def restart_audio_stream(guild: discord.Guild, stream_url: str = config.STREAM_URL) -> None:
    """Restarts playback in the guild's current voice channel, preserving volume settings."""
    voice_client = guild.voice_client
    if voice_client and voice_client.is_connected():
        current_volume = 1.0
        if isinstance(voice_client.source, discord.PCMVolumeTransformer):
            current_volume = voice_client.source.volume

        voice_client.stop()
        await asyncio.sleep(0.5)
        await play_audio(voice_client, stream_url=stream_url, volume=current_volume)

async def connect_to_voice(channel: discord.VoiceChannel, guild: discord.Guild) -> Optional[discord.VoiceClient]:
    """Connects or moves the bot to a voice channel with safety checks."""
    voice_client = guild.voice_client

    try:
        if voice_client and voice_client.is_connected():
            if voice_client.channel != channel:
                await voice_client.move_to(channel)
            return voice_client
        else:
            return await channel.connect(timeout=20.0, reconnect=True)
    except discord.ClientException as e:
        logger.error(f"ClientException connecting to {channel.name}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error connecting to {channel.name}: {e}")
        return None

async def join_and_play(channel: discord.VoiceChannel, guild: discord.Guild, stream_url: str = config.STREAM_URL) -> Optional[discord.VoiceClient]:
    """Convenience helper to join a voice channel and start playback."""
    voice_client = await connect_to_voice(channel, guild)
    if voice_client:
        await play_audio(voice_client, stream_url=stream_url)
    return voice_client
