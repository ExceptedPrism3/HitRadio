from discord.ext import commands

class OnPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return
        if str(self.bot.user.id) in message.content:
            return await message.reply('Hi, to view my available commands, execute `/help` of the bot.')


def setup(bot):
    bot.add_cog(OnPing(bot))