import discord
from discord.ext import commands


class SlashPing(commands.Cog):
    """
    A cog that handles the slash command /ping to show the bot's latency.

    Attributes
    ----------
    bot : commands.Bot
        The bot instance associated with this cog.

    Methods
    -------
    ping(ctx)
        Sends an embed message in response to the /ping command.

    """

    def __init__(self, bot):
        """
        Parameters
        ----------
        bot : commands.Bot
            The bot instance associated with this cog.
        """
        self.bot = bot

    @commands.slash_command(description="Shows the Bot's ping.")
    async def ping(self, ctx):
        """
        Sends an embed message in response to the /ping command.

        Parameters
        ----------
        ctx : commands.Context
            The context object associated with the command.

        Returns
        -------
        None
        """
        embed = discord.Embed(title="🏓 Pong", description=f'Bot Latency: **{round(self.bot.latency * 1000)}** ms',
                              color=0xFB401B)

        await ctx.respond(embeds=[embed], ephemeral=True)


def setup(bot):
    """
    Adds the SlashPing cog to the bot.

    Parameters
    ----------
    bot : commands.Bot
        The bot instance to add the cog to.

    Returns
    -------
    None
    """
    bot.add_cog(SlashPing(bot))
