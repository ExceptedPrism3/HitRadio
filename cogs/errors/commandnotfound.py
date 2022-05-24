from discord.ext import commands

class ErrorNotFound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

    async def cog_command_error(self, ctx, error):
        
        print(error)
        if isinstance(error, commands.CommandInvokeError):
            if error is not None:
                await ctx.respond("An error has occurred, if the issue persists contact the Author! Error Code=00x01", ephemeral= True)

        if isinstance(error, ConnectionResetError):
            await ctx.respond("An error has occurred, if the issue persists contact the Author! Error Code=00x02", ephemeral= True)
            return

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()


def setup(bot):
    bot.add_cog(ErrorNotFound(bot))