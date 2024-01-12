import discord
from discord.app_commands import command
from discord.ext import commands

from utils.voice_channel import VoiceChannelUtility


# Cog for handling the /pause command
class SlashPause(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash command for pausing the radio
    @command(name="pause", description="Pause the Radio.")
    async def pause(self, interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.blue())

        # Check if user and bot are in the same voice channel
        if not await VoiceChannelUtility.check_voice_state(interaction, embed):
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        guild_voice_state = interaction.guild.voice_client
        # Pause the audio if it's playing
        if guild_voice_state.is_paused():
            embed.description = "⏸️ I'm already paused at the moment!"
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        guild_voice_state.pause()
        embed.description = "⏸️ Radio Paused."
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(SlashPause(bot))
