import discord
from discord.app_commands import command
from discord.ext import commands

from utils.voice_channel import VoiceChannelUtility


# Cog to handle the /volume command
class SlashVolume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Adjusts the volume of the bot's audio in the voice channel
    @command(name="volume", description="Adjust the Bot's volume.")
    async def volume(self, interaction: discord.Interaction, vol: int) -> None:
        guild = interaction.guild

        # Create an embed for messages
        embed = discord.Embed()

        # Check if the user is in the same voice channel as the bot
        if not await VoiceChannelUtility.check_voice_state(interaction, embed):
            # If not in the same voice channel, send the appropriate message
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        # Check if the bot is playing music
        if not guild.voice_client.is_playing():
            embed.description = "🔇 I'm not currently playing any Hits."
            embed.color = discord.Color.red()
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        # Adjust volume and respond with confirmation
        vol = max(min(vol, 100), 0) / 100
        if isinstance(guild.voice_client.source, discord.PCMVolumeTransformer):
            guild.voice_client.source.volume = vol
        else:
            guild.voice_client.source = discord.PCMVolumeTransformer(guild.voice_client.source, volume=vol)

        embed.description = f"🔊 Radio volume set to {vol * 100}%"
        embed.color = discord.Color.green()
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(SlashVolume(bot))
