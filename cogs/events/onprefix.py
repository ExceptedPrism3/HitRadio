from nextcord.ext import commands

from essentials import BOT_INVITE, BOT_PREFIX

class OnPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        
        if str(BOT_PREFIX) in message.content:
            await message.reply("❗ All commands have been replaced with **__Slash Commands__** ❗\n\n" +
            "To view all available commands, execute `/help` command of the bot.\n\n" +
            "If you can't see **HITRADIO** commands list, try **re-inviting** the bot via the link bellow:\n" +
            "**" + BOT_INVITE + "**")


def setup(bot):
    bot.add_cog(OnPrefix(bot))