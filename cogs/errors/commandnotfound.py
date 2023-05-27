import logging
from discord.ext import commands

class ErrorNotFound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("error_handler")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

        # Handle unexpected exceptions
        self.logger.exception("An error occurred during command execution", exc_info=error)

    @commands.Cog.listener()
    async def on_command_error_handler(self, ctx, error):

        if isinstance(error, commands.CommandInvokeError):
            await ctx.respond("An error has occurred. If the issue persists, contact the author! Error Code=00x01", ephemeral=True)

        elif isinstance(error, ConnectionResetError):
            await ctx.respond("An error has occurred. If the issue persists, contact the author! Error Code=00x02", ephemeral=True)

    def cog_unload(self):
        """Cog unload handler. This removes any event hooks that were registered."""
        self.bot.lavalink.remove_event_hooks()

def setup(bot):
    bot.add_cog(ErrorNotFound(bot))
