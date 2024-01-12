import logging

import discord
from discord.app_commands import command
from discord.ext import commands

from private.essentials import BOT_INVITE, INVITE_LINK, BOT_OWNER_ID, OTHER_BOT_1, OTHER_BOT_2


# Class for creating a custom interactive view for the /info command
class SlashInfoUI(discord.ui.View):
    def __init__(self):
        super().__init__()
        # Add 'Invite' button for the bot
        self.add_item(discord.ui.Button(label="Invite", url=BOT_INVITE, emoji="➕", style=discord.ButtonStyle.link))
        # Add 'Support' button for the bot
        self.add_item(discord.ui.Button(label="Support", url=INVITE_LINK, emoji="📩", style=discord.ButtonStyle.link))

        # Create 'Other Bots' button and set its callback method
        other_bots_button = discord.ui.Button(label="Other Bots", custom_id="other_bots", emoji="🤖",
                                              style=discord.ButtonStyle.secondary)
        other_bots_button.callback = self.other_bots_button_callback
        self.add_item(other_bots_button)

    # Callback method for 'Other Bots' button
    async def other_bots_button_callback(self, interaction: discord.Interaction):
        # Create an embed with information about other bots
        embed = discord.Embed(title="Here's all Discord bots by the same author", color=0x00ff00)
        # Add fields to the embed
        embed.add_field(name="🟢 Online", value="\u200B", inline=False)
        embed.add_field(name="🎵 HitRadio", value="\u200B", inline=True)
        embed.add_field(name="🎷 JazzRadio", value="\u200B", inline=True)
        embed.add_field(name="\u200B", value="\u200B", inline=False)  # Invisible separator
        embed.add_field(name="🟡 In development", value="\u200B", inline=False)
        embed.add_field(name="🎷 DiscoBot", value="\u200B", inline=False)
        embed.add_field(name="\u200B", value="\u200B", inline=False)  # Invisible separator
        embed.add_field(name="👤 Author", value="<@403667971089760257>", inline=False)

        # Create a View for 'Invite' buttons for other bots
        other_bots_view = discord.ui.View()
        other_bots_view.add_item(
            discord.ui.Button(label="Invite HitRadio", url=OTHER_BOT_1, style=discord.ButtonStyle.link))
        other_bots_view.add_item(
            discord.ui.Button(label="Invite JazzRadio", url=OTHER_BOT_2, style=discord.ButtonStyle.link))

        # Try sending the embed as a DM and handle possible exceptions
        try:
            await interaction.user.send(embed=embed, view=other_bots_view)
            confirmation_embed = discord.Embed(title="DM Sent", description="✅ Check your DMs for more information!",
                                               color=0x00ff00)
            await interaction.response.send_message(embed=confirmation_embed, ephemeral=True)
        except discord.Forbidden:
            error_embed = discord.Embed(title="DM Error",
                                        description="⚠️ I couldn't send you a DM. Please check your privacy settings!",
                                        color=0xff0000)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
        except discord.HTTPException as e:
            logging.error(f"Failed to send DM: {e}")
            http_error_embed = discord.Embed(title="Error", description="⚠️ An error occurred while sending a DM.",
                                             color=0xff0000)
            await interaction.response.send_message(embed=http_error_embed, ephemeral=True)


# Cog for handling the /info command
class SlashInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.basicConfig(level=logging.INFO)

    # Slash command to display bot information
    @command(name="info", description="Display some information about the Bot.")
    async def info(self, interaction: discord.Interaction):
        view = SlashInfoUI()
        embed = discord.Embed(title="🤖 Bot Information", color=0xFB401B)
        embed.description = ("🎵 **Name**: HitRadio\n"
                             "🎼 **Description**: Playing 100% Hits for you.\n"
                             "🐍 **Coded with**: Python.\n"
                             "🌍 **Host**: EU / France\n\n"
                             f"❤️ **Made by**: <@{BOT_OWNER_ID}>.")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(SlashInfo(bot))
