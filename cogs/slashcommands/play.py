import logging

import discord
from discord.app_commands import command
from discord.ext import commands

from utils import audio


class SlashPlay(commands.Cog):
    # Initialize the class with the bot object
    def __init__(self, bot):
        self.bot = bot

    # Method to connect to a voice channel
    async def connect_to_channel(self, voice_channel):
        try:
            return await voice_channel.connect()
        except discord.ClientException as e:
            # Log any exceptions during connection
            logging.error(f"ClientException in connect_to_channel: {e}")
            return None

    # Ensure the bot is in the correct voice channel before playing
    async def ensure_voice(self, interaction):
        embed = discord.Embed(color=discord.Color.blue())

        # Check if user is in a voice channel
        if interaction.user.voice is None or interaction.user.voice.channel is None:
            embed.description = "🚫 You must be in a voice channel to run this command."
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return None

        voice_channel = interaction.user.voice.channel
        guild_voice_state = interaction.guild.voice_client

        # Check if already in requested voice channel
        if guild_voice_state and guild_voice_state.channel == voice_channel:
            embed.description = "🎶 I'm already in your voice channel."
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return None
        # Check if connected to a different channel
        elif guild_voice_state:
            embed.description = f"🔊 I'm already connected to a different channel: {guild_voice_state.channel.mention}"
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return None
        else:
            # Check for necessary permissions
            permissions = voice_channel.permissions_for(interaction.guild.me)
            if not permissions.connect or not permissions.speak:
                embed.description = "⛔ I need the `CONNECT` and `SPEAK` permissions."
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return None

            # Connect to the voice channel
            return await self.connect_to_channel(voice_channel)

    # Slash command to play music
    @command(name="play", description="Join your voice channel and plays the Hits.")
    async def play(self, interaction: discord.Interaction):
        # Ensure bot is in the correct voice channel
        voice_client = await self.ensure_voice(interaction)
        if voice_client is None:
            return

        embed = discord.Embed(color=discord.Color.green())

        if not voice_client.is_playing():
            # Use VoiceManager's logic to join and play
            await audio.join_and_play(interaction.user.voice.channel, interaction.guild)
            embed.description = f"🎵 Playing Hits in {interaction.user.voice.channel.mention}"
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed.description = "🔊 Already playing audio in this channel."
            await interaction.followup.send(embed=embed, ephemeral=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(SlashPlay(bot))
