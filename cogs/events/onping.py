from nextcord.ext import commands

class OnPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        
        if str(self.bot.user.id) in message.content:
            await message.reply('Hi, to view my available commands, execute `/help` of the bot.')


def setup(bot):
    bot.add_cog(OnPing(bot))