from discord.ext import commands
from discord.commands import slash_command


class SlashVolume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Adjust the Bots Volume")
    async def volume(self, ctx, vol: int) -> None:
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player:
            return await ctx.respond("I'm not playing any music.", ephemeral=True)

        vol = max(min(100, vol), 0)
        await player.set_volume(vol)
        return await ctx.respond(f"Set volume to {vol}", ephemeral=True)


def setup(bot):
    bot.add_cog(SlashVolume(bot))
