from nextcord.ext import commands

class Servers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True, brief = "Shows the servers that the bot is in.")
    async def servers(self, ctx):
        if ctx.author.id == 403667971089760257:
            activeservers = self.bot.guilds         
            i = 0       
            for guild in activeservers:
                await ctx.send(guild.name)
                i+=1

            await ctx.send('Total Joined Server(s): **{}**'.format(i))


def setup(bot):
    bot.add_cog(Servers(bot))