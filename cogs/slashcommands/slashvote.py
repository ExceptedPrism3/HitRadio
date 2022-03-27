import nextcord
from nextcord.ext import commands
from nextcord import Interaction

from essentials import INVITE, VOTE

class SlashVote(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.add_item(nextcord.ui.Button(label = "Top.gg", url = VOTE, emoji= "💖"))
        self.add_item(nextcord.ui.Button(label = "Invite", url = INVITE, emoji= "➕"))

class SlashUI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name = "vote", description = "Display the vote and invite links.")
    async def vote(self, interaction: Interaction):
        view = SlashVote()
        embed = nextcord.Embed(title = ':heart: Vote for the Bot', description = ":arrow_forward: Tog.gg **|** :arrow_forward: Invite to your Server", color = 0xFB401B)

        await interaction.response.send_message(embed = embed, view = view, delete_after = 60)

def setup(client):
    client.add_cog(SlashUI(client))