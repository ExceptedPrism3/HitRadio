import logging
from discord.ext import commands

ERROR_CODE_COMMAND_INVOKE_ERROR = "00x01"
ERROR_CODE_CONNECTION_RESET_ERROR = "00x02"


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Ignore CommandNotFound errors"""
        if isinstance(error, commands.CommandNotFound):
            return

    async def cog_command_error(self, ctx, error):
        """Handle command errors"""
        logging.exception(error)

        if isinstance(error, commands.CommandInvokeError):
            error_message = f"An error has occurred, if the issue persists contact the author! Error Code={ERROR_CODE_COMMAND_INVOKE_ERROR}"
            await ctx.respond(error_message, ephemeral=True)

        if isinstance(error, ConnectionResetError):
            error_message = f"An error has occurred, if the issue persists contact the author! Error Code={ERROR_CODE_CONNECTION_RESET_ERROR}"
            await ctx.respond(error_message, ephemeral=True)

    def cog_unload(self):
        """Cog unload handler. This removes any event hooks that were registered."""
        self.bot.lavalink._event_hooks.clear()


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
