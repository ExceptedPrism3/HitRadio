import discord
from discord import app_commands
from discord.ext import commands

import config
from db import database
from utils import voice

class Music(commands.Cog):
    """Cog handling music playback and voice channel controls."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _verify_voice_channel(self, interaction: discord.Interaction, require_same_channel: bool = False) -> bool:
        """Helper to validate user's voice status and bot permissions."""
        if not interaction.user.voice or not interaction.user.voice.channel:
            embed = discord.Embed(
                description="🚫 You must be in a voice channel to use this command.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False

        user_channel = interaction.user.voice.channel
        bot_voice = interaction.guild.voice_client

        if require_same_channel:
            if not bot_voice or not bot_voice.is_connected():
                embed = discord.Embed(
                    description="🚫 I'm not currently connected to any voice channel.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return False

            if bot_voice.channel != user_channel:
                embed = discord.Embed(
                    description=f"🚫 You must be in {bot_voice.channel.mention} with me to use this command.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return False

        # Check permissions in user's channel
        bot_member = interaction.guild.me
        permissions = user_channel.permissions_for(bot_member)
        if not permissions.connect or not permissions.speak:
            embed = discord.Embed(
                description=f"⛔ I lack `Connect` or `Speak` permissions in {user_channel.mention}.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False

        return True

    @app_commands.command(name="play", description="Stream Hit Radio live in your voice channel.")
    async def play(self, interaction: discord.Interaction):
        """Starts 24/7 streaming in the user's voice channel."""
        if not await self._verify_voice_channel(interaction, require_same_channel=False):
            return

        user_channel = interaction.user.voice.channel
        await interaction.response.defer(ephemeral=False)

        voice_client = await voice.connect_to_voice(user_channel, interaction.guild)
        if not voice_client:
            embed = discord.Embed(
                description="⚠️ Failed to connect to the voice channel. Please check my permissions.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        if voice_client.is_playing():
            embed = discord.Embed(
                description=f"🎶 Already playing **Hit Radio** in {user_channel.mention}!",
                color=config.EMBED_COLOR
            )
            await interaction.followup.send(embed=embed)
            return

        success = await voice.play_audio(voice_client)
        if success:
            await database.save_state(interaction.guild.id, user_channel.id)
            embed = discord.Embed(
                title="📻 Now Playing Hit Radio",
                description=f"Streaming live 100% Hits in {user_channel.mention} 🎵",
                color=config.EMBED_COLOR
            )
            embed.set_footer(text="24/7 Live Stream | Use /volume to adjust audio")
            await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(
                description="⚠️ Failed to start audio playback. Please try again shortly.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="pause", description="Pause radio playback.")
    async def pause(self, interaction: discord.Interaction):
        """Pauses the current stream."""
        if not await self._verify_voice_channel(interaction, require_same_channel=True):
            return

        voice_client = interaction.guild.voice_client
        if not voice_client or not voice_client.is_playing():
            embed = discord.Embed(
                description="⏸️ Radio is not currently playing.",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        voice_client.pause()
        embed = discord.Embed(
            description="⏸️ **Hit Radio** playback paused. Use `/resume` to continue.",
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="resume", description="Resume paused radio playback.")
    async def resume(self, interaction: discord.Interaction):
        """Resumes the paused stream."""
        if not await self._verify_voice_channel(interaction, require_same_channel=True):
            return

        voice_client = interaction.guild.voice_client
        if not voice_client or not voice_client.is_paused():
            embed = discord.Embed(
                description="▶️ Radio is not currently paused.",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        voice_client.resume()
        embed = discord.Embed(
            description="▶️ Resumed **Hit Radio** live stream!",
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="volume", description="Adjust the bot's playback volume (1-100%).")
    @app_commands.describe(level="Volume level from 1 to 100")
    async def volume(self, interaction: discord.Interaction, level: app_commands.Range[int, 1, 100]):
        """Sets the volume level."""
        if not await self._verify_voice_channel(interaction, require_same_channel=True):
            return

        voice_client = interaction.guild.voice_client
        if not voice_client or not voice_client.source:
            embed = discord.Embed(
                description="🔇 No active audio stream to adjust volume.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        vol_multiplier = level / 100.0
        if isinstance(voice_client.source, discord.PCMVolumeTransformer):
            voice_client.source.volume = vol_multiplier
        else:
            voice_client.source = discord.PCMVolumeTransformer(voice_client.source, volume=vol_multiplier)

        embed = discord.Embed(
            description=f"🔊 Radio volume set to **{level}%**",
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leave", description="Disconnect the bot from your voice channel.")
    async def leave(self, interaction: discord.Interaction):
        """Disconnects the bot and removes saved state."""
        if not await self._verify_voice_channel(interaction, require_same_channel=True):
            return

        voice_client = interaction.guild.voice_client
        if voice_client:
            await voice_client.disconnect(force=True)

        await database.remove_state(interaction.guild.id)

        embed = discord.Embed(
            description="👋 Left the voice channel. Thanks for listening to **Hit Radio**!",
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
