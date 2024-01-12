import discord
from discord.app_commands import command
from discord.ext import commands

from private.essentials import BOT_INVITE, VOTE


# UI Class for vote and invite links
class SlashVoteUI(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Top.gg", url=VOTE, emoji="💖", style=discord.ButtonStyle.link))
        self.add_item(discord.ui.Button(label="Invite", url=BOT_INVITE, emoji="➕", style=discord.ButtonStyle.link))


# Cog to handle the /vote command
class SlashVote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Displays voting and invite links
    @command(name="vote", description="Display the vote and the invite link.")
    async def vote(self, interaction: discord.Interaction):
        view = SlashVoteUI()
        embed = discord.Embed(title='Vote for the Bot', color=0xFB401B)
        embed.description = "Support us by **voting** on **Top.gg** & **inviting** the bot to your **server**! 💖"
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(SlashVote(bot))
