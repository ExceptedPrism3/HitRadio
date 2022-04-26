import nextcord
from nextcord.ext import commands

class SlashLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name = "leave", description = "Leaves your voice channel.")
    async def leave(self, interaction):

        voice_client = nextcord.utils.get(interaction.client.voice_clients, guild = interaction.guild)

        if not voice_client:
            return await interaction.send("I'm not in a voice channel.")

        if not interaction.user.voice:
            return await interaction.send("You need to be in a voice channel to use this command.")

        if (interaction.user.voice.channel != interaction.guild.me.voice.channel):
            return await interaction.send("You need to be in ths same voice channel as me to execute this command.")
        
        await interaction.guild.voice_client.disconnect()
        return await interaction.send("I have left the voice channel.")


def setup(bot):
    bot.add_cog(SlashLeave(bot))