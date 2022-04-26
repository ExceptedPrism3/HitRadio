import re
import nextcord
from nextcord.ext import commands

class SlashLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name = "leave", description = "Leaves your voice channel.")
    async def leave(self, interaction):

        voice_client = nextcord.utils.get(interaction.client.voice_clients, guild=interaction.guild)
    
        embed2 = nextcord.Embed(title = "Warning", color = 0xFB401B, description = "Due to some complications " +
        "with Discord, a new bot has come in place to replace the current one. This bot will be offline " +
        "by the end of this month! Please make sure to invite the new bot before the deadline!\n\n" +
        "New Bot: <@967845086471815248>\n\n Bot Invite Link: https://discord.com/api/oauth2/authorize?client_id=967845086471815248&permissions=277062450240&scope=bot%20applications.commands")

        if not voice_client:
            return await interaction.send("I'm not in a voice channel.")

        if not interaction.user.voice:
            return await interaction.send("You need to be in a voice channel to use this command.")

        if (interaction.user.voice.channel != interaction.guild.me.voice.channel):
            return await interaction.send("You need to be in ths same voice channel as me to execute this command.")
        
        await interaction.guild.voice_client.disconnect()
        await interaction.send("I have left the voice channel.")
        return await interaction.send(embed = embed2)


def setup(bot):
    bot.add_cog(SlashLeave(bot))