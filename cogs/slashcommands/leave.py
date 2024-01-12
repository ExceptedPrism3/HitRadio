import discord
from discord.app_commands import command
from discord.ext import commands

from utils.voice_channel import VoiceChannelUtility


# Cog for handling the /leave command
class SlashLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash command for leaving the voice channel
    @command(name="leave", description="Leaves your voice channel.")
    async def leave(self, interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.red())

        # Check if user and bot are in the same voice channel
        if not await VoiceChannelUtility.check_voice_state(interaction, embed):
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        # Disconnect the bot from the voice channel
        await interaction.guild.voice_client.disconnect(force=True)
        embed.description = "👋 I have left the voice channel."
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(SlashLeave(bot))
