import discord
from discord.app_commands import command
from discord.ext import commands


class SlashHelp(commands.Cog):
    # Initialize the SlashHelp cog with the bot instance
    def __init__(self, bot):
        self.bot = bot

    # Define a slash command for displaying the help menu
    @command(name="help", description="Display the help menu.")
    async def help(self, interaction: discord.Interaction):
        # Create an embed with a title and description
        embed = discord.Embed(title="🛠️ Help Commands", description="List of available commands:", color=0xFB401B)
        # Set the bot's avatar as the thumbnail for the embed
        embed.set_thumbnail(url=self.bot.user.avatar.url)

        # A dictionary mapping commands to emojis for visual representation
        command_emojis = {
            "play": "🎶",
            "pause": "⏸️",
            "resume": "▶️",
            "leave": "🚪",
            "volume": "🔊",
            "info": "ℹ️",
            "vote": "🗳️",
            "help": "❓",
            "ping": "🏓",
            "uptime": "⏰"
        }

        # Loop through each command in the bot's command tree
        for cmd in self.bot.tree.get_commands():
            # Get the emoji for the command, use a default emoji if not found
            emoji = command_emojis.get(cmd.name, "❓")
            # Add a field to the embed for each command with its emoji, name, description, and usage
            embed.add_field(name=f"{emoji} {cmd.name.capitalize()}", value=f"{cmd.description}\nUsage: `/{cmd.name}`",
                            inline=False)

        # Set the footer of the embed with the requester's information
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
        # Add a timestamp to the embed
        embed.timestamp = discord.utils.utcnow()

        # Send the embed as a response to the interaction
        await interaction.response.send_message(embed=embed, ephemeral=True)


# Function to add this cog to the bot
async def setup(bot):
    await bot.add_cog(SlashHelp(bot))
