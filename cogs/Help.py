import nextcord
from nextcord.ext import commands

class Help(commands.Cog):

    def __int__(self, client):
        self.client = client
    
    @commands.command()
    async def helpo(self, ctx):
        embed = nextcord.Embed(title = "Help Commands", color = 0xFB401B)
        embed.set_author(name = "HitRadio", url = "https://prism3.me", icon_url = "https://cdn.discordapp.com/attachments/947328978857898016/949764854149959710/HitRadio.png")
        embed.add_field(name = "Commands", value = "**/join** - Joins your voice channel and plays the Hits.\n\n**/leave** - Leaves your voice channel.\n\n**/vote** - Vote for the Bot.\n\n**/invite** - Invite the Bot to your Server.")
        await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Help(client))