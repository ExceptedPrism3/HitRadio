import nextcord
from nextcord.ext import commands
from datetime import datetime

class SlashUpTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name = "uptime", description = "Shows the Bot's uptime.")
    async def uptime(self, interaction):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = nextcord.Embed(title = "", description= f"**⏰ Uptime: {days}d, {hours}h, {minutes}m, {seconds}s**", color = 0xFB401B)
        await interaction.send(embed = embed)


def setup(bot):
    bot.add_cog(SlashUpTime(bot))