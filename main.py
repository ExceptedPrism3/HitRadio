import asyncio
import os

from discord import Intents
from discord.ext import commands

from private.essentials import BOT_TOKEN


# Main function to run the bot
async def main():
    intents = Intents().default()
    bot = commands.Bot(command_prefix='hr!', help_command=None, intents=intents)

    initial_extensions = []

    # Load extensions from cogs folders
    for event in os.listdir('./cogs/events'):
        if event.endswith('.py'):
            initial_extensions.append("cogs.events." + event[:-3])
    for command in os.listdir('./cogs/slashcommands'):
        if command.endswith('.py'):
            initial_extensions.append("cogs.slashcommands." + command[:-3])

    # Load each extension
    for extension in initial_extensions:
        await bot.load_extension(extension)

    await bot.start(BOT_TOKEN, reconnect=True)


if __name__ == '__main__':
    asyncio.run(main())
