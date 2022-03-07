from discord import FFmpegPCMAudio
from nextcord.ext import commands

from bottoken import STREAM_LINK

class Join(commands.Cog):

    def __int__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context = True, aliases=['p', 'play'])
    async def join(self, ctx,  url: str = STREAM_LINK):
        if (ctx.voice_client):
            await ctx.send("I'm already connected to a channel.")
            return

        if (ctx.author.voice):
                channel = ctx.message.author.voice.channel
                player = await channel.connect()
                player.play(FFmpegPCMAudio(STREAM_LINK))
                await ctx.send(f"I have joined the **{ctx.author.voice.channel}** channel.")
        else:
           await ctx.send("You must be in a voice channel to run this command.")


def setup(bot):
    bot.add_cog(Join(bot))