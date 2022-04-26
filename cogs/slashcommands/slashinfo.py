import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from essentials import BOT_INVITE, INVITE_LINK, BOT_OWNER_ID

class SlashInfoUI(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.add_item(nextcord.ui.Button(label = "Invite", url = BOT_INVITE, emoji= "➕"))
        self.add_item(nextcord.ui.Button(label = "Support", url = INVITE_LINK, emoji= "📩"))

class SlashInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name = "info", description = "Display some information about the Bot.")
    async def vote(self, interaction: Interaction):
        view = SlashInfoUI()
        embed = nextcord.Embed(title = "Bot Information", color = 0xFB401B, description = "Name: **HitRadio**\n\n" +
        "Description: **HitRadio that plays 100% Hits for you.**\n\n" +
        "Coded with: **Python**.\n\n" +
        "Host: **EU/France**\n\n\n" +
        f'Made with ❤️ by <@{BOT_OWNER_ID}>.')

        return await interaction.response.send_message(embed = embed, view = view)

def setup(client):
    client.add_cog(SlashInfo(client))