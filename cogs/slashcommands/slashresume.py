from discord.ext import commands
from discord.commands import slash_command


class SlashResume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Resumes the paused Radio.")
    async def resume(self, ctx):

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player:
            return await ctx.respond("I'm not in a voice channel.", ephemeral=True)

        if not ctx.user.voice:
            return await ctx.respond("You need to be in a voice channel to use this command.", ephemeral=True)

        if ctx.user.voice.channel != ctx.guild.me.voice.channel:
            return await ctx.respond("You need to be in ths same voice channel as me to execute this command.",
                                     ephemeral=True)

        if player.paused:
            await player.set_pause(False)
            return await ctx.respond("Radio Resuming...", ephemeral=True)
        elif not player.paused:
            return await ctx.respond(f"{ctx.user.mention} I'm already playing the Hits!", ephemeral=True)


def setup(bot):
    bot.add_cog(SlashResume(bot))
