import discord
from discord.ext import commands
from discord.commands import slash_command
from datetime import datetime

class SlashUpTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.launch_time = datetime.utcnow()
    
    @slash_command(description = "Shows the Bot's uptime.")
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(description= f"**⏰ Uptime: {days}d, {hours}h, {minutes}m, {seconds}s**", color = 0xFB401B)
        
        return await ctx.respond(embed = embed, ephemeral = True)


def setup(bot):
    bot.add_cog(SlashUpTime(bot))
