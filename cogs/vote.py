import nextcord
from nextcord.ext import commands

from essentials import INVITE, VOTE

class Vote(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.add_item(nextcord.ui.Button(label = 'Top.gg', url = VOTE, emoji = "💖"))
        self.add_item(nextcord.ui.Button(label = 'Invite', url = INVITE, emoji = "➕"))

class UI(commands.Cog):
    def __init__(bot, self):
        self.bot = bot

    @commands.command(pass_context = True, aliases=['invite'], brief = "Display the vote and invite links.")
    async def vote(self, ctx):
        view = Vote()
        embed = nextcord.Embed(title = ':heart: Vote for the Bot', description = ":arrow_forward: Tog.gg **|** :arrow_forward: Invite to your Server", color = 0xFB401B)

        await ctx.reply(embed = embed, view = view, delete_after = 60)


def setup(bot):
    bot.add_cog(UI(bot))
