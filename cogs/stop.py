from nextcord.ext import commands

class Stop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True, brief="Pauses the currently playing song.")
    async def pause(self, ctx):
        # Checks if music is playing and pauses it, otherwise sends the player a message that nothing is playing
        try:
            ctx.voice_client.pause()
            await ctx.send("Radio Stopped.")
        except:
            await ctx.send(f"{ctx.author.mention} i'm not playing music at the moment!")


def setup(bot):
    bot.add_cog(Stop(bot))