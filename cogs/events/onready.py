import nextcord
from nextcord.ext import commands, tasks
from itertools import cycle

from essentials import BOT_STATUS

class status(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.status = cycle(BOT_STATUS)

    @tasks.loop(seconds=300.0)
    async def change_status(self):
        await self.bot.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.listening, name = next(self.status)))
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('HitRadio has Started')
        print('-------------------')
        await self.bot.wait_until_ready()
        self.change_status.start()

def setup(bot):
    bot.add_cog(status(bot))