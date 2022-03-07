from nextcord.ext import commands

class Resume(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True, aliases=['continue', 'kml'], brief="Resumes the paused music.")
    async def resume(self, ctx):
        # Checks if music is paused and resumes it, otherwise sends the player a message that nothing is playing
        try:
            ctx.voice_client.resume()
            await ctx.send("Radio Resuming...")
        except:
            await ctx.send(f"{ctx.author.mention} I'm already playing the Hits!")


def setup(bot):
    bot.add_cog(Resume(bot))