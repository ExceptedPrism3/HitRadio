from nextcord.ext import commands

class Shutdown(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True, aliases=['shut'], brief = "Turns the bot off.")
    async def shutdown(self, ctx):
        if ctx.author.id == 403667971089760257:
            await ctx.send("Bot Closed!")
            await self.bot.close()


def setup(bot):
    bot.add_cog(Shutdown(bot))