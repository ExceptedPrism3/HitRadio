from discord.ext import commands
import os

# Import Bot Token
from private.essentials import BOT_PREFIX, BOT_TOKEN

bot = commands.Bot(command_prefix = BOT_PREFIX, help_command = None)

initial_extenions = []

# Cycle through the events folder that's located in the cogs folder and look for any file that ends with .py, once found add it to the initial_extenions ArrayList
for filename1 in os.listdir('./cogs/events'):
    if filename1.endswith('.py'):
        initial_extenions.append("cogs.events." + filename1[:-3])

# Cycle through the slashcommands folder that's located in the cogs folder and look for any file that ends with .py, once found add it to the initial_extenions ArrayList
for filename1 in os.listdir('./cogs/slashcommands'):
    if filename1.endswith('.py'):
        initial_extenions.append("cogs.slashcommands." + filename1[:-3])

# Import whatever in the initial_extenions ArrayList into the main class
if __name__ == '__main__':
    for extension in initial_extenions:
        bot.load_extension(extension)


bot.run(BOT_TOKEN, reconnect = True)
