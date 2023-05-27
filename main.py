import os
from pathlib import Path
from discord.ext import commands

# Import Bot Token
from private.essentials import BOT_PREFIX, BOT_TOKEN

bot = commands.Bot(command_prefix=BOT_PREFIX, help_command=None)

initial_extensions = []

# Cycle through the events folder that's located in the cogs folder and look for any file that ends with .py, once found add it to the initial_extensions list
for events_path in Path('./cogs/events').rglob('*.py'):
    initial_extensions.append('.'.join(events_path.parts)[:-3].replace(os.sep, '.'))

for commands_path in Path('./cogs/commands').rglob('*.py'):
    initial_extensions.append('.'.join(commands_path.parts)[:-3].replace(os.sep, '.'))

for errors_path in Path('./cogs/errors').rglob('*.py'):
    initial_extensions.append('.'.join(errors_path.parts)[:-3].replace(os.sep, '.'))

# Import whatever is in the initial_extensions list into the main class
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

bot.run(BOT_TOKEN, reconnect=True)
