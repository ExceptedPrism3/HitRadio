import asyncio
import logging
import os
import sys

import discord
from discord.ext import commands

import config

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)-8s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("HitRadio")

# Initialize Discord Intents
intents = discord.Intents.default()
intents.message_content = True  # Used for detecting bot mention replies

class HitRadioBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="hr!",
            intents=intents,
            help_command=None
        )
        self.launch_time = None

    async def setup_hook(self):
        self.launch_time = discord.utils.utcnow()

        # Check Opus audio library status
        if not discord.opus.is_loaded():
            logger.info("Checking Opus voice library...")
            try:
                discord.opus._load_default()
            except Exception as e:
                logger.warning(f"Could not load default Opus library: {e}")

        # Dynamically load all extension cogs
        cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
        for filename in sorted(os.listdir(cogs_dir)):
            if filename.endswith(".py") and not filename.startswith("__"):
                cog_name = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(cog_name)
                    logger.info(f"Loaded extension: {cog_name}")
                except Exception as e:
                    logger.error(f"Failed to load extension {cog_name}: {e}", exc_info=True)

bot = HitRadioBot()

def main():
    if not config.DISCORD_TOKEN:
        logger.critical("DISCORD_TOKEN is missing! Please configure it in .env or environment variables.")
        sys.exit(1)

    logger.info("Starting HitRadio Discord Bot...")
    try:
        bot.run(config.DISCORD_TOKEN, log_handler=None)
    except discord.LoginFailure:
        logger.critical("Invalid Discord token provided. Please verify your DISCORD_TOKEN in .env.")
    except Exception as e:
        logger.critical(f"Fatal error running bot: {e}", exc_info=True)

if __name__ == "__main__":
    main()
