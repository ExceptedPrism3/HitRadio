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
    
        embed2 = nextcord.Embed(title = "Warning", color = 0xFB401B, description = "Due to some complications " +
        "with Discord, a new bot has come in place to replace the current one. This bot will be offline " +
        "by the end of this month! Please make sure to invite the new bot before the deadline!\n\n" +
        "New Bot: <@967845086471815248>\n\n Bot Invite Link: https://discord.com/api/oauth2/authorize?client_id=967845086471815248&permissions=277062450240&scope=bot%20applications.commands")

        if (voice_client):
            return await interaction.send("I'm already connected to a channel.")

        if (interaction.user.voice):
            channel = interaction.user.voice.channel
            player = await channel.connect()
            player.play(FFmpegPCMAudio(STREAM_LINK))
            await interaction.send(f"I have joined the {interaction.user.voice.channel.mention} channel.")
            return await interaction.send(embed = embed2)
        else:
           return await interaction.send("You must be in a voice channel to run this command.")


def setup(bot):
    bot.add_cog(SlashJoin(bot))