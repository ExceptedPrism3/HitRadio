import nextcord
from nextcord.ext import commands
from datetime import datetime

class UpTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.launch_time = datetime.utcnow()

    @commands.command(pass_context = True, brief = "Shows the Bot's uptime.")
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = nextcord.Embed(description= f"**⏰ Uptime: {days}d, {hours}h, {minutes}m, {seconds}s**", color = 0xFB401B)
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(UpTime(bot))