from discord.ext import commands
from private.essentials import BOT_INVITE, BOT_PREFIX

class OnPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if str(BOT_PREFIX) in message.content:
            reply_message = (
                "❗ All commands have been replaced with **__Slash Commands__** ❗\n\n"
                "To view all available commands, execute `/help` command of the bot.\n\n"
                "If you can't see **HITRADIO** commands list, try **re-inviting** the bot via the link below:\n"
                f"**{BOT_INVITE}**"
            )
            await message.reply(reply_message)


def setup(bot):
    bot.add_cog(OnPrefix(bot))
