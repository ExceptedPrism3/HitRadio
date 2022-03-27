from nextcord import FFmpegPCMAudio
from nextcord.ext import commands

from essentials import STREAM_LINK

class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context = True, aliases=['p', 'play'], brief = "Joins your voice channel and play the hits.")
    async def join(self, ctx):
        if (ctx.voice_client):
            return await ctx.send("I'm already connected to a channel.")

        if (ctx.author.voice):
                channel = ctx.message.author.voice.channel
                player = await channel.connect()
                player.play(FFmpegPCMAudio(STREAM_LINK))
                await ctx.send(f"I have joined the {ctx.author.voice.channel.mention} channel.")
        else:
           await ctx.send("You must be in a voice channel to run this command.")


def setup(bot):
    bot.add_cog(Join(bot))