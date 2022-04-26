from operator import ne
import nextcord
from nextcord.ext import commands
import nextcord

from essentials import BOT_INVITE, BOT_PREFIX

class OnPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
    
        embed2 = nextcord.Embed(title = "Warning", color = 0xFB401B, description = "Due to some complications " +
        "with Discord, a new bot has come in place to replace the current one. This bot will be offline " +
        "by the end of this month! Please make sure to invite the new bot before the deadline!\n\n" +
        "New Bot: <@967845086471815248>\n\n Bot Invite Link: https://discord.com/api/oauth2/authorize?client_id=967845086471815248&permissions=277062450240&scope=bot%20applications.commands")
        
        if str(BOT_PREFIX) in message.content:
            await message.reply("❗ All commands have been replaced with **__Slash Commands__** ❗\n\n" +
            "To view all available commands, execute `/help` command of the bot.\n\n" +
            "If you can't see **HITRADIO** commands list, try **re-inviting** the bot via the link bellow:\n" +
            "**" + BOT_INVITE + "**")
            return await message.reply(embed = embed2)


def setup(bot):
    bot.add_cog(OnPrefix(bot))