import logging
import discord
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger(__name__)

class Errors(commands.Cog):
    """Cog handling global application command errors and reporting user-friendly alerts."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Register tree error handler
        bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Global handler for slash command exceptions."""
        embed = discord.Embed(color=discord.Color.red())

        # Extract underlying exception if wrapped in CommandInvokeError
        original_error = getattr(error, "original", error)

        if isinstance(error, app_commands.CommandOnCooldown):
            embed.title = "⏳ Cooldown Active"
            embed.description = f"Please wait **{error.retry_after:.1f}s** before using this command again."
        elif isinstance(error, app_commands.MissingPermissions):
            missing = ", ".join(f"`{perm}`" for perm in error.missing_permissions)
            embed.title = "⛔ Missing Permissions"
            embed.description = f"You require the following permission(s) to run this command: {missing}"
        elif isinstance(error, app_commands.BotMissingPermissions):
            missing = ", ".join(f"`{perm}`" for perm in error.missing_permissions)
            embed.title = "⛔ Bot Missing Permissions"
            embed.description = f"I require the following permission(s) to complete this action: {missing}"
        elif isinstance(error, app_commands.CheckFailure):
            embed.title = "🚫 Check Failure"
            embed.description = "You cannot execute this command at this time."
        else:
            embed.title = "⚠️ An Error Occurred"
            embed.description = "An unexpected error occurred while executing this command. The issue has been logged."
            logger.error(
                f"Unhandled AppCommand error in /{interaction.command.name if interaction.command else 'unknown'}: {original_error}",
                exc_info=original_error
            )

        try:
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as send_err:
            logger.error(f"Failed to deliver error message to interaction: {send_err}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Errors(bot))
