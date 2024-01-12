from datetime import datetime

import discord
from discord.app_commands import command
from discord.ext import commands


# Cog to handle the /uptime command
class SlashUpTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.launch_time = datetime.utcnow()  # Record bot's launch time

    # Shows how long the bot has been running
    @command(name="uptime", description="Shows the Bot's uptime.")
    async def uptime(self, interaction: discord.Interaction):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(
            description=f"⏰ Uptime: {days}d, {hours}h, {minutes}m, {seconds}s",
            color=0xFB401B
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(SlashUpTime(bot))
