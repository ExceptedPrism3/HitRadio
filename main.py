import nextcord
from nextcord.ext import commands
import os

# Import Bot Token
from essentials import BOT_PREFIX, BOT_TOKEN


intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = BOT_PREFIX, intents = intents, help_command = None)

@bot.event
async def on_application_command_error(ctx, error):
        
    if isinstance(error, nextcord.ApplicationCheckFailure):
        embed = nextcord.Embed(description= "Only the bot devs can execute that command!", color = 0xFB401B)
        await ctx.send(embed = embed)

initial_extenions = []

# Cycle through the errors folder that's located in the cogs folder and look for any file that ends with .py, once found add it to the initial_extenions ArrayList
for filename1 in os.listdir('./cogs/errors'):
    if filename1.endswith('.py'):
        initial_extenions.append("cogs.errors." + filename1[:-3])

# Cycle through the events folder that's located in the cogs folder and look for any file that ends with .py, once found add it to the initial_extenions ArrayList
for filename1 in os.listdir('./cogs/events'):
    if filename1.endswith('.py'):
        initial_extenions.append("cogs.events." + filename1[:-3])

# Cycle through the slashcommands folder that's located in the cogs folder and look for any file that ends with .py, once found add it to the initial_extenions ArrayList
for filename1 in os.listdir('./cogs/slashcommands'):
    if filename1.endswith('.py'):
        initial_extenions.append("cogs.slashcommands." + filename1[:-3])

# Cycle through the admin folder that's located in the cogs slashcommands and cogs folders and look for any file that ends with .py, once found add it to the initial_extenions ArrayList
for filename1 in os.listdir('./cogs/slashcommands/admin'):
    if filename1.endswith('.py'):
        initial_extenions.append("cogs.slashcommands.admin." + filename1[:-3])

# Import whatever in the initial_extenions ArrayList into the main class
if __name__ == '__main__':
    for extension in initial_extenions:
        bot.load_extension(extension)


bot.run(BOT_TOKEN)
