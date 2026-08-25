import datetime
import discord
from discord import app_commands
from discord.ext import commands

import config

class InfoView(discord.ui.View):
    """Interactive button menu for bot links and cross-promotion."""

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Invite Bot", url=config.BOT_INVITE, emoji="➕", style=discord.ButtonStyle.link))
        self.add_item(discord.ui.Button(label="Support Server", url=config.SUPPORT_INVITE, emoji="💬", style=discord.ButtonStyle.link))
        self.add_item(discord.ui.Button(label="Vote Top.gg", url=config.VOTE_URL, emoji="💖", style=discord.ButtonStyle.link))

        if config.OTHER_BOTS_ENABLED:
            other_bots_btn = discord.ui.Button(
                label="Other Bots",
                custom_id="hitradio_other_bots",
                emoji="🤖",
                style=discord.ButtonStyle.secondary
            )
            other_bots_btn.callback = self.other_bots_callback
            self.add_item(other_bots_btn)

    async def other_bots_callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Other Discord Bots by Author",
            description="Explore our sister music radio bots:",
            color=config.EMBED_COLOR
        )
        embed.add_field(name="📻 HitRadio", value="Playing 100% Moroccan & International Hits 24/7", inline=False)
        embed.add_field(name="🎷 JazzRadio", value="Smooth Jazz & Relaxing Lounge 24/7", inline=False)
        embed.add_field(name="🕺 DiscoBot", value="*In active development*", inline=False)

        sub_view = discord.ui.View()
        sub_view.add_item(discord.ui.Button(label="Invite HitRadio", url=config.OTHER_BOT_1, style=discord.ButtonStyle.link))
        sub_view.add_item(discord.ui.Button(label="Invite JazzRadio", url=config.OTHER_BOT_2, style=discord.ButtonStyle.link))

        await interaction.response.send_message(embed=embed, view=sub_view, ephemeral=True)

class VoteView(discord.ui.View):
    """Button menu for voting."""
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Vote on Top.gg", url=config.VOTE_URL, emoji="💖", style=discord.ButtonStyle.link))
        self.add_item(discord.ui.Button(label="Invite Bot", url=config.BOT_INVITE, emoji="➕", style=discord.ButtonStyle.link))

class General(commands.Cog):
    """Cog handling informational, utility, and interactive UI commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's WebSocket latency.")
    async def ping(self, interaction: discord.Interaction):
        """Displays bot latency in milliseconds."""
        latency_ms = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot Latency: **{latency_ms} ms**",
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="uptime", description="Check how long the bot has been running.")
    async def uptime(self, interaction: discord.Interaction):
        """Shows total elapsed uptime since startup."""
        launch_time = getattr(self.bot, "launch_time", None)
        if not launch_time:
            delta = datetime.timedelta(seconds=0)
        else:
            delta = discord.utils.utcnow() - launch_time

        total_seconds = int(delta.total_seconds())
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        embed = discord.Embed(
            title="⏰ HitRadio Uptime",
            description=f"Running continuously for **{uptime_str}**",
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="info", description="Display bot details, statistics, and invite links.")
    async def info(self, interaction: discord.Interaction):
        """Shows bot info embed with interactive buttons."""
        embed = discord.Embed(
            title="📻 HitRadio — 100% Hits 24/7",
            description=(
                "**HitRadio** brings the best Moroccan and International hits directly to your Discord server.\n\n"
                f"• **Servers:** `{len(self.bot.guilds):,}`\n"
                f"• **Author:** <@{config.BOT_OWNER_ID}>\n"
                f"• **Library:** `discord.py`\n"
                f"• **Audio Engine:** `FFmpeg + Opus`\n"
                f"• **Stream Quality:** `128 kbps Stereo`\n"
            ),
            color=config.EMBED_COLOR
        )
        if self.bot.user and self.bot.user.display_avatar:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.set_footer(text="Thank you for supporting HitRadio!")
        await interaction.response.send_message(embed=embed, view=InfoView(), ephemeral=False)

    @app_commands.command(name="vote", description="Support HitRadio by voting on Top.gg.")
    async def vote(self, interaction: discord.Interaction):
        """Displays voting and support links."""
        embed = discord.Embed(
            title="💖 Vote for HitRadio",
            description="Voting helps more music lovers discover **HitRadio**! Click below to vote on Top.gg.",
            color=config.EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed, view=VoteView(), ephemeral=True)

    @app_commands.command(name="help", description="List all available HitRadio slash commands.")
    async def help(self, interaction: discord.Interaction):
        """Dynamic slash command menu."""
        embed = discord.Embed(
            title="🛠️ HitRadio Commands Menu",
            description="Here are all available slash commands:",
            color=config.EMBED_COLOR
        )
        if self.bot.user and self.bot.user.display_avatar:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        emojis = {
            "play": "🎵",
            "pause": "⏸️",
            "resume": "▶️",
            "volume": "🔊",
            "leave": "🚪",
            "info": "ℹ️",
            "ping": "🏓",
            "uptime": "⏰",
            "vote": "💖",
            "help": "❓"
        }

        # Retrieve all registered application commands
        for cmd in self.bot.tree.get_commands():
            emoji = emojis.get(cmd.name, "🔹")
            embed.add_field(
                name=f"{emoji} /{cmd.name}",
                value=f"{cmd.description or 'No description provided.'}\n`/{cmd.name}`",
                inline=False
            )

        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        embed.timestamp = discord.utils.utcnow()
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
