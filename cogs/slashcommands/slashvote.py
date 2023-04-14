import discord
from discord.ext import commands
from discord.commands import slash_command

from private.essentials import BOT_INVITE, VOTE


class SlashVote(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.add_item(discord.ui.Button(label="Top.gg", url=VOTE, emoji="💖"))
        self.add_item(discord.ui.Button(label="Invite", url=BOT_INVITE, emoji="➕"))


class SlashUI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(description="Display the vote and invite links.")
    async def vote(self, ctx):
        view = SlashVote()
        embed = discord.Embed(title=':heart: Vote for the Bot',
                              description=":arrow_forward: Tog.gg **|** :arrow_forward: Invite to your Server",
                              color=0xFB401B)

        return await ctx.respond(embed=embed, view=view, ephemeral=True)


def setup(client):
    client.add_cog(SlashUI(client))
