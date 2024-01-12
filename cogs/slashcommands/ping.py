import discord
from discord.app_commands import command
from discord.ext import commands


# Cog to handle the /ping command
class SlashPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Responds with the bot's current latency
    @command(name="ping", description="Shows the Bot's ping.")
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🏓 Pong",
            description=f'Bot Latency: **{round(self.bot.latency * 1000)}** ms',
            color=0xFB401B
        )
        await interaction.response.send_message(embeds=[embed], ephemeral=True)


async def setup(bot):
    await bot.add_cog(SlashPing(bot))
