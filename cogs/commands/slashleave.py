from discord.ext import commands
from discord.commands import slash_command

class SlashLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(description="Leaves your voice channel.")
    async def leave(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        
        if not player:
            return await ctx.respond("I'm not in a voice channel.", ephemeral=True)

        if not ctx.author.voice:
            return await ctx.respond("You need to be in a voice channel to use this command.", ephemeral=True)

        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            return await ctx.respond("You need to be in the same voice channel as me to execute this command.", ephemeral=True)
        
        await player.stop()
        await ctx.voice_client.disconnect(force=True)

        return await ctx.respond("I have left the voice channel.", ephemeral=True)


def setup(bot):
    bot.add_cog(SlashLeave(bot))
