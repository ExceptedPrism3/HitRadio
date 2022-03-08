import nextcord
from nextcord.ext import commands

class Vote(nextcord.ui.View):

    def __init__(self):
        super().__init__()
        self.value = None
        vote = 'https://top.gg/bot/949629320110944256/vote'
        invite = 'https://top.gg/bot/949629320110944256/invite'
        self.add_item(nextcord.ui.Button(label = 'Top.gg', url = vote))
        self.add_item(nextcord.ui.Button(label = 'Invite', url = invite))

class UI(commands.Cog):

    def __int__(bot, self):
        self.bot = bot

    @commands.command(pass_context = True)
    async def vote(self, ctx):
        view = Vote()
        ncsdocsembed = nextcord.Embed(title = ':heart: Vote for the Bot', description = ":fast_forward: Tog.gg **|** :arrow_forward: Invite to your Server", color = 0xFB401B)

        return await ctx.reply(embed = ncsdocsembed, view = view, delete_after = 60)


def setup(bot):
    bot.add_cog(UI(bot))
