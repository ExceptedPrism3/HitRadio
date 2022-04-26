import nextcord 
from nextcord.ext import commands

class SlashPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name = "ping", description = "Shows the Bot's ping.")
    async def ping(self, interaction):

        embed = nextcord.Embed(title = "Ping", description = "**Calculating...**", color = 0xFB401B)
    
        embed2 = nextcord.Embed(title = "Warning", color = 0xFB401B, description = "Due to some complications " +
        "with Discord, a new bot has come in place to replace the current one. This bot will be offline " +
        "by the end of this month! Please make sure to invite the new bot before the deadline!\n\n" +
        "New Bot: <@967845086471815248>\n\n Bot Invite Link: https://discord.com/api/oauth2/authorize?client_id=967845086471815248&permissions=277062450240&scope=bot%20applications.commands")

        await interaction.send(embed = embed)

        embedPing = nextcord.Embed(title = "🏓 Pong", description = f'Bot Latency: **{round(self.bot.latency * 1000)}** ms', color = 0xFB401B)

        await interaction.edit_original_message(embed = embedPing)

        return await interaction.send(embed = embed2)


def setup(bot):
    bot.add_cog(SlashPing(bot))