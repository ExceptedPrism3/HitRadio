from nextcord.ext import commands

class Pause(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True, aliases=['stop', 'hault'], brief = "Pauses the currently playing song.")
    async def pause(self, ctx):

        if ctx.voice_client is None:
            return await ctx.send("I'm not in a voice channel.")

        if ctx.author.voice is None:
            return await ctx.send('You need to be in a voice channel to use this command.')

        if (ctx.author.voice.channel != ctx.me.voice.channel):
            return await ctx.send('You need to be in ths same voice channel as me to execute this command.')
        
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Radio Stopped.")
        else:
            await ctx.send(f"{ctx.author.mention} i'm already paused at the moment!")


def setup(bot):
    bot.add_cog(Pause(bot))