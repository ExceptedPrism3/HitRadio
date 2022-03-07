import nextcord
from nextcord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        embed = nextcord.Embed(title = "Help Commands", color = 0xFB401B)
        embed.add_field(name = "Join", value = "Join your voice channel and plays the Hits.\n`hr!join`")
        embed.add_field(name = "Resume", value = "Resume playing hits whens stopped.\n`hr!resume`")
        embed.add_field(name = "Stop", value = "Stop playing the Hits.\n`hr!stop`")
        embed.add_field(name = "Leave", value = "Leave your voice channel.\n`hr!leave`")
        embed.add_field(name = "Ping", value = "Check the Bot's Ping.\n`hr!ping`")
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Help(bot))