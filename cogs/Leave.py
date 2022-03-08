from nextcord.ext import commands

class Leave(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context = True, brief = "Leaves your voice channel.")
    async def leave(self, ctx):

        if ctx.voice_client is None:
            return await ctx.send("I'm not in a voice channel.")

        if ctx.author.voice is None:
            return await ctx.send('You need to be in a voice channel to use this command.')

        if (ctx.author.voice.channel != ctx.me.voice.channel):
            return await ctx.send('You need to be in ths same voice channel as me to execute this command.')
        
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("I have left the voice channel.")


def setup(bot):
    bot.add_cog(Leave(bot))