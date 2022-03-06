import nextcord
from nextcord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        embed = nextcord.Embed(title = "Help Commands", color = 0xFB401B)
        embed.add_field(name = "Join", value = "Joins your voice channel and plays the Hits.\n`hr!join`")
        embed.add_field(name = "Leave", value = "Leaves your voice channel.\n`hr!leave`")
        embed.add_field(name = "Vote", value = "Vote for the Bot.\n`hr!vote`")
        embed.add_field(name = "Invite", value = "Invite the Bot to your Server.\n`hr!invite`")
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Help(bot))