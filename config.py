import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord Bot Credentials & Core Config
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
STREAM_URL = os.getenv("STREAM_URL") or os.getenv("MP3_LINK") or "https://hitradio-maroc.ice.infomaniak.ch/hitradio-maroc-128.mp3"
BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID", 403667971089760257))
DATABASE_PATH = os.getenv("DATABASE_PATH", "bot.db")

# Branding & Appearance
EMBED_COLOR = 0xFB401B  # Hit Radio Brand Orange-Red

# Links
BOT_INVITE = os.getenv(
    "BOT_INVITE",
    "https://discord.com/api/oauth2/authorize?client_id=967845086471815248&permissions=277062450240&scope=bot%20applications.commands"
)
SUPPORT_INVITE = os.getenv("SUPPORT_INVITE", "https://discord.com/invite/MfR5mcpVfX")
VOTE_URL = os.getenv("VOTE_URL", "https://top.gg/bot/949629320110944256/vote")

# Cross-Promotion
OTHER_BOTS_ENABLED = os.getenv("OTHER_BOTS_ENABLED", "true").lower() in ("true", "1", "yes")
OTHER_BOT_1 = os.getenv(
    "OTHER_BOT_1",
    "https://discord.com/api/oauth2/authorize?client_id=1086030727650476153&permissions=277062450240&scope=bot%20applications.commands"
)
OTHER_BOT_2 = os.getenv(
    "OTHER_BOT_2",
    "https://discord.com/api/oauth2/authorize?client_id=1086218627436511303&permissions=277062450240&scope=bot%20applications.commands"
)

# Presence Status Rotation Pool
BOT_STATUS = [
    "HitRadio 100% Hits",
    "MoMo Morning Show",
    "Shakira",
    "DJ Hmida",
    "Martin Garrix",
    "David Guetta",
    "Pitbull",
    "Snore",
    "Don BIGG",
    "ElGrandeToto",
    "7liwa",
    "Nass El Ghiwane",
    "Nancy Ajram"
]
