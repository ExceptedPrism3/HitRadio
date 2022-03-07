from itertools import cycle
import nextcord
from nextcord.ext import commands
from itertools import cycle
import os

# Import Bot Token
from bottoken import BOT_TOKEN


intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = 'hr!', intents = intents, help_command = None)

@bot.event
async def on_ready():
    # await bot.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.listening, name = "HitRadio Hits"))
    print("The Bot has Started")
    print("-------------------")


initial_extenions = []


# Cycle through the cogs folder and look for any file that ends with .py, once found add it to the initial_extenions ArrayList
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extenions.append("cogs." + filename[:-3])


# Import whatever in the initial_extenions ArrayList into the main class
if __name__ == '__main__':
    for extension in initial_extenions:
        bot.load_extension(extension)


bot.run(BOT_TOKEN)
