from nextcord.ext import commands

class Servers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def servers(self, ctx):
        if ctx.author.id == 403667971089760257:
            activeservers = self.bot.guilds                
            for guild in activeservers:
                await ctx.send(guild.name)
        else:
            await ctx.send('Only the Author can execute this command!')


def setup(bot):
    bot.add_cog(Servers(bot))