import nextcord
from nextcord.ext import commands, application_checks
from nextcord import Interaction

from essentials import BOT_OWNER_ID, GUILD_ID

class SlashShutDown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_if_is_is_me(interaction: Interaction):
        return interaction.user.id == BOT_OWNER_ID

    @nextcord.slash_command(name = "shutdown", description = "Admin command.", guild_ids = GUILD_ID)
    @application_checks.check(check_if_is_is_me)
    async def shutdown(self, interaction):
            await interaction.send("Bot Closed!")
            await self.bot.close()

def setup(bot):
    bot.add_cog(SlashShutDown(bot))