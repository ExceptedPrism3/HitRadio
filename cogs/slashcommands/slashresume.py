import nextcord
from nextcord.ext import commands

class SlashResume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name = "resume", description = "Resumes the paused Radio.")
    async def resume(self, interaction):

        voice_client = nextcord.utils.get(interaction.client.voice_clients, guild=interaction.guild)

        if not voice_client:
            return await interaction.send("I'm not in a voice channel.")

        if not interaction.user.voice:
            return await interaction.send("You need to be in a voice channel to use this command.")

        if (interaction.user.voice.channel != interaction.guild.me.voice.channel):
            return await interaction.send("You need to be in ths same voice channel as me to execute this command.")

        if interaction.guild.voice_client.is_paused():
            interaction.guild.voice_client.resume()
            await interaction.send("Radio Resuming...")
        else:
            await interaction.send(f"{interaction.user.mention} I'm already playing the Hits!")


def setup(bot):
    bot.add_cog(SlashResume(bot))