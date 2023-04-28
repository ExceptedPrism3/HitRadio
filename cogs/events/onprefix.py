from discord.ext import commands

from private.essentials import BOT_INVITE, BOT_PREFIX


class OnPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if BOT_PREFIX in message.content:
            await message.respond(f"❗ All commands have been replaced with **__Slash Commands__** ❗\n\n"
                                   f"To view all available commands, execute `/help` command of the bot.\n\n"
                                   f"If you can't see **HITRADIO** commands list, try **re-inviting** the bot via the link below:\n"
                                   f"**{BOT_INVITE}**")


def setup(bot):
    bot.add_cog(OnPrefix(bot))
