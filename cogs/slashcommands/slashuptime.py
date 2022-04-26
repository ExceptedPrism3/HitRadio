import nextcord
from nextcord.ext import commands
from datetime import datetime

class SlashUpTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.launch_time = datetime.utcnow()
    
    @nextcord.slash_command(name = "uptime", description = "Shows the Bot's uptime.")
    async def uptime(self, interaction):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = nextcord.Embed(description= f"**⏰ Uptime: {days}d, {hours}h, {minutes}m, {seconds}s**", color = 0xFB401B)
    
        embed2 = nextcord.Embed(title = "Warning", color = 0xFB401B, description = "Due to some complications " +
        "with Discord, a new bot has come in place to replace the current one. This bot will be offline " +
        "by the end of this month! Please make sure to invite the new bot before the deadline!\n\n" +
        "New Bot: <@967845086471815248>\n\n Bot Invite Link: https://discord.com/api/oauth2/authorize?client_id=967845086471815248&permissions=277062450240&scope=bot%20applications.commands")
        
        await interaction.send(embed = embed)
        return await interaction.send(embed = embed2)


def setup(bot):
    bot.add_cog(SlashUpTime(bot))