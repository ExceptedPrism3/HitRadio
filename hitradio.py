from discord import Intents
from discord.ext import commands
import os

# Import Bot Token
from private.essentials import BOT_PREFIX, BOT_TOKEN

intents = Intents().all()

bot = commands.Bot(command_prefix=BOT_PREFIX, help_command=None, intents=intents)

initial_extensions = []

# Cycle through the events folder that's located in the cogs folder and look for any file that ends with .py,
# once found add it to the initial_extensions ArrayList
for filename1 in os.listdir('./cogs/events'):
    if filename1.endswith('.py'):
        initial_extensions.append("cogs.events." + filename1[:-3])

for filename1 in os.listdir('./cogs/slashcommands'):
    if filename1.endswith('.py'):
        initial_extensions.append("cogs.slashcommands." + filename1[:-3])

# Import whatever in the initial_extensions ArrayList into the main class
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

bot.run(BOT_TOKEN, reconnect=True)
