import nextcord
from nextcord.ext import commands

class SlashPause(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name = "pause", description = "Pauses the Radio.")
    async def pause(self, interaction):

        if not interaction.client.voice_clients:
            return await interaction.send("I'm not in a voice channel.")

        if not interaction.user.voice:
            return await interaction.send("You need to be in a voice channel to use this command.")

        if (interaction.user.voice.channel != interaction.guild.me.voice.channel):
            return await interaction.send("You need to be in ths same voice channel as me to execute this command.")
        
        if interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.pause()
            await interaction.send("Radio Stopped.")
        else:
            await interaction.send(f"{interaction.user.mention} i'm already paused at the moment!")


def setup(bot):
    bot.add_cog(SlashPause(bot))