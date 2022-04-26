import nextcord 
from nextcord.ext import commands

class SlashPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name = "ping", description = "Shows the Bot's ping.")
    async def ping(self, interaction):

        embed = nextcord.Embed(title = "Ping", description = "**Calculating...**", color = 0xFB401B)

        await interaction.send(embed = embed)

        embedPing = nextcord.Embed(title = "🏓 Pong", description = f'Bot Latency: **{round(self.bot.latency * 1000)}** ms', color = 0xFB401B)

        return await interaction.edit_original_message(embed = embedPing)


def setup(bot):
    bot.add_cog(SlashPing(bot))