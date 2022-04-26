import nextcord
from nextcord.ext import commands

class OnPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
    
        embed2 = nextcord.Embed(title = "Warning", color = 0xFB401B, description = "Due to some complications " +
        "with Discord, a new bot has come in place to replace the current one. This bot will be offline " +
        "by the end of this month! Please make sure to invite the new bot before the deadline!\n\n" +
        "New Bot: <@967845086471815248>\n\n Bot Invite Link: https://discord.com/api/oauth2/authorize?client_id=967845086471815248&permissions=277062450240&scope=bot%20applications.commands")

        if message.author.bot:
            return
        if str(self.bot.user.id) in message.content:
            await message.reply('Hi, to view my available commands, execute `/help` of the bot.')
            return await message.reply(embed = embed2)


def setup(bot):
    bot.add_cog(OnPing(bot))