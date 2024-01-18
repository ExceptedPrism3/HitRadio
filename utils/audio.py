import asyncio
import logging

import discord

from private.essentials import STREAM_LINK


# Function to join a voice channel and start playing audio
async def join_and_play(channel, guild):
    # Check if the bot is not connected or in a different channel
    if not guild.voice_client or (guild.voice_client and not guild.voice_client.is_connected()):
        try:
            await channel.connect()
        except discord.ClientException as e:
            print(f"Error connecting to channel: {e}")
            return
    elif guild.voice_client.channel != channel:
        # If connected to a different channel, move to the new channel
        try:
            await guild.voice_client.move_to(channel)
        except discord.ClientException as e:
            print(f"Error moving to a new channel: {e}")
            return

    # Play the audio stream
    play_audio(guild.voice_client)


# Function to play audio in a voice channel
def play_audio(voice_client):
    try:
        audio_source = discord.FFmpegPCMAudio(STREAM_LINK, options='-b:a 96k')
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=lambda e: handle_playback_errors(e, voice_client))
    except Exception as e:
        logging.error(f"Error starting FFmpeg audio stream: {e}")

        # wait 10 seconds before retrying
        asyncio.sleep(10)
        play_audio(voice_client)  # Retry playing the audio


def handle_playback_errors(error, voice_client):
    if error:
        logging.error(f"FFmpeg playback error: {error}")
        # Implement error recovery such as restarting the stream
        restart_audio_stream(voice_client.guild)


# Function to restart the audio stream in a guild's voice channel
async def restart_audio_stream(guild):
    # Get the voice client of the guild
    voice_client = guild.voice_client
    # Check if the voice client is connected
    if voice_client and voice_client.is_connected():
        # Stop any currently playing audio
        voice_client.stop()
        # Replay the audio stream
        play_audio(voice_client)
