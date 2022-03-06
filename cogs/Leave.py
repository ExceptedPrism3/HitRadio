import nextcord
from nextcord.ext import commands

class Leave(commands.Cog):

    def __int__(self, client):
        self.client = client
    
    @commands.command(pass_context = True)
    async def leave(self, ctx):
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("I have left the voice channel.")
        else:
            await ctx.send("I'm not in a voice channel.")


def setup(client):
    client.add_cog(Leave(client))