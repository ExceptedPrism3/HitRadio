from nextcord.ext import commands

class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context = True, brief = "Shows the Bot's ping.")
    async def ping(self, ctx):
        return await ctx.send(f'Pong! {round(self.bot.latency * 1000)} ms')


def setup(bot):
    bot.add_cog(Ping(bot))