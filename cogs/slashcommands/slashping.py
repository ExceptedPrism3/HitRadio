import discord 
from discord.ext import commands
from discord.commands import slash_command

class SlashPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @slash_command(description = "Shows the Bot's ping.")
    async def ping(self, ctx):

        embed = discord.Embed(title = "Ping", description = "**Calculating...**", color = 0xFB401B)

        msg = await ctx.send(embeds = [embed])

        embedPing = discord.Embed(title = "🏓 Pong", description = f'Bot Latency: **{round(self.bot.latency * 1000)}** ms', color = 0xFB401B)

        return await msg.edit(embeds = [embedPing])


def setup(bot):
    bot.add_cog(SlashPing(bot))