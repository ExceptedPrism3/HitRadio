from nextcord.ext import commands

class Resume(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True, aliases=['continue', 'kml'], brief = "Resumes the paused music.")
    async def resume(self, ctx):
        
        if ctx.voice_client is None:
            return await ctx.send("I'm not in a voice channel.")

        if ctx.author.voice is None:
            return await ctx.send('You need to be in a voice channel to use this command.')

        if (ctx.author.voice.channel != ctx.me.voice.channel):
            return await ctx.send('You need to be in ths same voice channel as me to execute this command.')

        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Radio Resuming...")
        else:
            await ctx.send(f"{ctx.author.mention} I'm already playing the Hits!")


def setup(bot):
    bot.add_cog(Resume(bot))