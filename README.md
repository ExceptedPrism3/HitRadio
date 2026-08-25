# 📻 HitRadio Discord Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/discord.py-v2.3+-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="discord.py" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

A dedicated 24/7 Moroccan Discord Radio Bot streaming live **Hit Radio** with crystal-clear audio quality, automatic crash recovery, volume controls, and modern slash commands.

---

## 🌟 Key Features

* 🎶 **24/7 Uninterrupted Streaming**: Connects directly to Hit Radio's high-bitrate live audio stream.
* 🔄 **Auto-Recovery & Persistence**: Remembers connected channels across restarts/crashes with SQLite and auto-reconnects.
* 🔍 **Stream Watchdog**: Periodically checks stream health and self-heals in case of stream dropouts.
* 🔊 **Dynamic Volume Control**: Real-time volume scaling (1% – 100%) via PCM transformation.
* ⚡ **Full Slash Command Suite**: Seamless user experience with Discord Application Commands and interactive UI buttons.
* 🛡️ **Global Error Handling**: Clear, user-friendly responses for missing permissions or connection errors.

---

## 🛠️ Slash Commands

| Command | Description |
| :--- | :--- |
| `/play` | Join your voice channel and stream Hit Radio live |
| `/pause` | Pause radio playback |
| `/resume` | Resume paused playback |
| `/volume <1-100>` | Adjust the radio volume in your channel |
| `/leave` | Disconnect the bot from the voice channel |
| `/info` | View bot statistics, invite link, and sister bots |
| `/vote` | Support HitRadio with a vote on Top.gg |
| `/ping` | Check WebSocket gateway latency |
| `/uptime` | Display elapsed bot uptime |
| `/help` | Interactive command menu and usage guide |

---

## 🚀 Quick Setup & Installation

### 1. Prerequisites
* Python **3.10** or higher
* [FFmpeg](https://ffmpeg.org/download.html) installed on your system PATH:
  ```bash
  # macOS
  brew install ffmpeg

  # Ubuntu/Debian
  sudo apt-get install ffmpeg
  ```

### 2. Clone the Repository
```bash
git clone https://github.com/ExceptedPrism3/HitRadio.git
cd HitRadio
```

### 3. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure Environment
Copy the `.env.example` template:
```bash
cp .env.example .env
```
Edit `.env` and provide your **Discord Bot Token**:
```env
DISCORD_TOKEN=your_actual_discord_token_here
STREAM_URL=https://hitradio-maroc.ice.infomaniak.ch/hitradio-maroc-128.mp3
```

### 5. Launch the Bot
```bash
python3 bot.py
```

---

## 📁 Architecture Overview

```
HitRadio/
├── bot.py                     # Bot initialization, intent configuration & cog loader
├── config.py                  # Typed environment configuration
├── requirements.txt           # Python dependencies
├── .env.example               # Configuration template
├── cogs/
│   ├── music.py               # Playback controls (/play, /pause, /resume, /volume, /leave)
│   ├── general.py             # Informational commands (/info, /help, /ping, /uptime, /vote)
│   ├── events.py              # Startup, presence rotation, reconnects & stream watchdog
│   └── errors.py              # Application command error handling
├── db/
│   └── database.py            # SQLite asynchronous voice state storage
└── utils/
    ├── voice.py               # FFmpeg stream generation & voice connection logic
    └── stream_check.py        # Stream health watchdog
```

---

## 📜 Changelog
See [CHANGELOG.md](CHANGELOG.md) for detailed release notes and version history.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).

