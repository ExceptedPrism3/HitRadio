
# 🎵 HitRadio

![Banner](previews/HitRadio.gif)

HitRadio is a Discord bot that plays non-stop Hits from the HitRadio Radio Station. The bot is built using JavaScript and leverages the Discord.js library to deliver a seamless music streaming experience.

## 🚀 Features

- **24/7 Streaming**: Continuous Hits from HitRadio.
- **High Quality Audio**: Uses `sodium-native` for optimal performance.
- **Easy Control**: Interactive **Stop Button** 🛑 and slash commands.
- **Auto Reconnection**: Automatically rejoins if the stream or connection drops.
- **Custom Status**: Rotates through artist names and updates.

## 🛠️ Installation

### Prerequisites

- **Node.js v20.0.0** or higher
- **npm** (Node Package Manager)
- **FFmpeg** (Required for audio processing)

### Linux (Ubuntu/Debian) Requirements
If running on Linux, you must install build tools for the encryption libraries:
```bash
sudo apt-get update
sudo apt-get install -y build-essential python3 libtool automake autoconf ffmpeg
```

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ExceptedPrism3/HitRadio.git
   cd HitRadio
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create a `.env` file:**
   ```env
   DISCORD_TOKEN=your_bot_token
   ```

4. **Configure the bot (Optional):**
   Edit `config.json` to customize the status messages or radio URL.

5. **Run the bot:**
   ```bash
   # For development
   node hitradio.js

   # For production (recommended)
   pm2 start hitradio.js --name hitradio
   ```

## 🎮 Commands

- **/play** - 🎶 Start playing the radio in your voice channel.
- **/stop** - 🛑 Stop the radio and leave the channel.
- **/ping** - 🏓 Check the bot's latency.
- **/uptime** - ⏱️ Check how long the bot has been running.
- **/info** - ℹ️ Get information about the bot.
- **/vote** - 🗳️ Get voting and invite links.
- **/help** - ❓ List all available commands.

## 🤝 Contribution

We welcome contributions! Feel free to fork this project, submit issues, or create pull requests.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes.
4. Push to the branch.
5. Create a new Pull Request.

## 📜 License

This project is licensed under the **GNU AGPL v3** License - see the **[LICENSE](LICENSE)** file for details.

## 🛠️ Support

If you encounter any issues or have questions, feel free to join our **[Support Discord Server](https://discord.gg/MfR5mcpVfX)** or open an issue on GitHub.

---

Made with ❤️ by **Prism3**
