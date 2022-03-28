import nextcord 
from nextcord.ext import commands

class SlashPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name = "ping", description = "Shows the Bot's ping.")
    async def ping(self, interaction):
        await interaction.send('Calculating...')
        return await interaction.edit_original_message(content=f'🏓 Pong! **{round(self.bot.latency * 1000)}** ms')


def setup(bot):
    bot.add_cog(SlashPing(bot))