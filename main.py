import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import os

# Import Bot Token
from bottoken import BOTTOKEN


intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!', intents = intents)


@client.event
async def on_ready():
    await client.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.listening, name = "HitRadio"))
    print("The Bot has Started")
    print("-------------------")


testServerID = 934424188582780968

@client.slash_command(name = "testw", description = "Chi 7aja", guild_ids = [testServerID])
async def testw(interaction: Interaction):
    await interaction.response.send_message("Hello, hooman")



# initial_extenions = []


# # Cycle through the cogs folder and look for any file that ends with .py, once found add it to the initial_extenions ArrayList
# for filename in os.listdir('./cogs'):
#     if filename.endswith('.py'):
#         initial_extenions.append("cogs." + filename[:-3])


# # Once finished cycling through the cogs folder, import whatever in the initial_extenions ArrayList into the main class
# if __name__ == '__main__':
#     for extension in initial_extenions:
#         client.load_extension(extension)


client.run(BOTTOKEN)
