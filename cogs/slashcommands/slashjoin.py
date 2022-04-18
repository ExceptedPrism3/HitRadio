import nextcord
from nextcord import FFmpegPCMAudio
from nextcord.ext import commands

from essentials import STREAM_LINK

class SlashJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name = "join", description = "Joins your voice channel and play the hits.")
    async def join(self, interaction):

        voice_client = nextcord.utils.get(interaction.client.voice_clients, guild=interaction.guild)

        if (voice_client):
            return await interaction.send("I'm already connected to a channel.")

        if (interaction.user.voice):
            channel = interaction.user.voice.channel
            player = await channel.connect()
            player.play(FFmpegPCMAudio(STREAM_LINK))
            await interaction.send(f"I have joined the {interaction.user.voice.channel.mention} channel.")
        else:
           await interaction.send("You must be in a voice channel to run this command.")


def setup(bot):
    bot.add_cog(SlashJoin(bot))