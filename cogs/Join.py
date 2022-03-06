import nextcord
from nextcord.ext import commands

class Join(commands.Cog):

    def __int__(self, client):
        self.client = client
    
    @commands.command(pass_context = True)
    async def join(self, ctx):
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
            await ctx.send("I have joined the channel")
        else:
            await ctx.send("You must be in a voice channel to run this command.")


def setup(client):
    client.add_cog(Join(client))