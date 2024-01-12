import logging

import discord
from discord.ext import commands

# Error codes for different types of errors
ERROR_CODE_COMMAND_INVOKE_ERROR = "00x01"
ERROR_CODE_CONNECTION_RESET_ERROR = "00x02"
ERROR_CODE_GENERAL_ERROR = "00x03"
ERROR_CODE_MISSING_PERMISSIONS = "00x04"
ERROR_CODE_CHECK_FAILURE = "00x05"


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        # Initialize ErrorHandler with a reference to the bot
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Handles errors triggered by command execution."""
        # Ignore errors if the command was not found
        if isinstance(error, commands.CommandNotFound):
            return

        # Handle other types of errors
        await self.handle_error(ctx, error)

    async def handle_error(self, ctx, error):
        """Handle different types of errors with specific responses."""
        # Create an embed to display the error message
        embed = discord.Embed(color=discord.Color.red())

        # Determine the type of error and set the appropriate message and error code
        if isinstance(error, commands.CommandInvokeError):
            embed.description = f"⚠️ Command error occurred. Error Code={ERROR_CODE_COMMAND_INVOKE_ERROR}"
        elif isinstance(error, ConnectionResetError):
            embed.description = f"⚠️ Connection error occurred. Error Code={ERROR_CODE_CONNECTION_RESET_ERROR}"
        elif isinstance(error, commands.MissingPermissions):
            embed.description = f"⚠️ You lack the necessary permissions. Error Code={ERROR_CODE_MISSING_PERMISSIONS}"
        elif isinstance(error, commands.CheckFailure):
            embed.description = f"⚠️ Check failure occurred. Error Code={ERROR_CODE_CHECK_FAILURE}"
        else:
            embed.description = f"⚠️ An unexpected error occurred. Error Code={ERROR_CODE_GENERAL_ERROR}"

        # Log the error for debugging purposes
        logging.error(f"Error in command '{ctx.command}': [{type(error)}] {error}")

        # Respond with the error embed
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    # Add the ErrorHandler cog to the bot
    bot.add_cog(ErrorHandler(bot))
