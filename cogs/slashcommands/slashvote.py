import nextcord
from nextcord.ext import commands
from nextcord import Interaction

from essentials import BOT_INVITE, VOTE

class SlashVote(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.add_item(nextcord.ui.Button(label = "Top.gg", url = VOTE, emoji= "💖"))
        self.add_item(nextcord.ui.Button(label = "Invite", url = BOT_INVITE, emoji= "➕"))

class SlashUI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name = "vote", description = "Display the vote and invite links.")
    async def vote(self, interaction: Interaction):

        view = SlashVote()
        embed = nextcord.Embed(title = ':heart: Vote for the Bot', description = ":arrow_forward: Tog.gg **|** :arrow_forward: Invite to your Server", color = 0xFB401B)
    
        embed2 = nextcord.Embed(title = "Warning", color = 0xFB401B, description = "Due to some complications " +
        "with Discord, a new bot has come in place to replace the current one. This bot will be offline " +
        "by the end of this month! Please make sure to invite the new bot before the deadline!\n\n" +
        "New Bot: <@967845086471815248>\n\n Bot Invite Link: hhttps://discord.com/api/oauth2/authorize?client_id=967845086471815248&permissions=277062450240&scope=bot%20applications.commands")

        await interaction.response.send_message(embed = embed, view = view, delete_after = 60)
        return await interaction.send(embed = embed2)

def setup(client):
    client.add_cog(SlashUI(client))