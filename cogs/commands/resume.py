import discord
from discord.app_commands import command
from discord.ext import commands

from utils.voice_channel import VoiceChannelUtility


# Cog to handle the /resume command
class SlashResume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Resumes paused radio/music
    @command(name="resume", description="Resumes the paused Radio.")
    async def resume(self, interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.green())

        # Check if the user and bot are in the same voice channel
        if not await VoiceChannelUtility.check_voice_state(interaction, embed):
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        guild_voice_state = interaction.guild.voice_client
        # Resume playback if currently paused
        if guild_voice_state.is_paused():
            guild_voice_state.resume()
            embed.description = "▶️ Radio Resuming..."
        else:
            embed.description = f"{interaction.user.mention} ▶️ I'm already playing the Hits!"
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(SlashResume(bot))
