from discord.ext import commands


class OnPing(commands.Cog):
    """
    A cog that listens for messages and sends a response if the bot's user ID is mentioned.

    Attributes
    ----------
    bot : commands.Bot
        The bot instance associated with this cog.

    Methods
    -------
    on_message(message)
        Listens for messages and sends a response if the bot's user ID is mentioned.

    """

    def __init__(self, bot):
        """
        Parameters
        ----------
        bot : commands.Bot
            The bot instance associated with this cog.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Listens for messages and sends a response if the bot's user ID is mentioned.

        Parameters
        ----------
        message : discord.Message
            The message object that triggered the listener.

        Returns
        -------
        None
        """
        if message.author.bot:
            return
        if str(self.bot.user.id) in message.content:
            return await message.reply('Hi, to view my available commands, execute `/help` of the bot.')



def setup(bot):
    """
    Adds the OnPing cog to the bot.

    Parameters
    ----------
    bot : commands.Bot
        The bot instance to add the cog to.

    Returns
    -------
    None
    """
    bot.add_cog(OnPing(bot))
