import discord
from discord.ext import commands


class OnPing(commands.Cog):
    # Initialization of the Cog with the bot instance
    def __init__(self, bot):
        self.bot = bot

    # Event listener for every message sent in a channel where the bot is present
    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from bots to prevent potential spam or loops
        if message.author.bot:
            return

        # Check if the bot is mentioned in the message
        if self.bot.user in message.mentions:
            # Create an embed with a response to the mention
            embed = discord.Embed(
                title="👋 Hey there!",
                description="Hi, to view my available commands, execute `/help` of the bot.",
                color=discord.Color.blue()
            )
            # Reply to the message with the embed
            await message.reply(embed=embed)


# Setup function to add this Cog to the bot
async def setup(bot):
    await bot.add_cog(OnPing(bot))
