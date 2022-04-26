import nextcord
from nextcord.ext import commands

class SlashHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name = "help", description = "Displays the help menu.")
    async def help(self, interaction):
    
        embed = nextcord.Embed(title = "Help Commands", color = 0xFB401B)
        embed.add_field(name = "Join", value = "Join your voice channel and plays the Hits.\n`/join`")
        embed.add_field(name = "Resume", value = "Resume playing hits whens stopped.\n`/resume`")
        embed.add_field(name = "Ping", value = "Check the Bot's Ping.\n`/ping`")
        embed.add_field(name = "Leave", value = "Leave your voice channel.\n`/leave`")
        embed.add_field(name = "Stop", value = "Stop playing the Hits.\n`/stop`")
        embed.add_field(name = "Vote", value = "Display Links of the Bot.\n`/vote`")
        embed.add_field(name = "uptime", value = "Display the Bot's uptime.\n`/uptime`")
    
        embed2 = nextcord.Embed(title = "Warning", color = 0xFB401B, description = "Due to some complications " +
        "with Discord, a new bot has come in place to replace the current one. This bot will be offline " +
        "by the end of this month! Please make sure to invite the new bot before the deadline!\n\n" +
        "New Bot: <@967845086471815248>\n\n Bot Invite Link: https://discord.com/api/oauth2/authorize?client_id=968211299043536976&permissions=277062450240&scope=bot%20applications.commands")

        await interaction.send(embed = embed)
        return await interaction.send(embed = embed2)


def setup(bot):
    bot.add_cog(SlashHelp(bot))