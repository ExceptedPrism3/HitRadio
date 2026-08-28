# Changelog

All notable changes to the **HitRadio** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [4.1.0] - 2026-08-28

### Added
- **Intelligent Permission Validation & Backoff**: Added pre-connection permission checks (`CONNECT`, `SPEAK`, `VIEW_CHANNEL`) in `utils/stream_check.py` with exponential backoff on restricted channels, preventing continuous 20-second timeout loops.
- **Optimized FFmpeg Streaming Headers**: Added `-headers "User-Agent: HitRadioDiscordBot/4.0\r\n"`, `-analyzeduration 0`, and `-probesize 32768` to eliminate stream buffering delays and prevent Icecast edge servers from dropping audio buffers.
- **Automated Memory Cleanup**: Integrated periodic garbage collection (`gc.collect()`) in the watchdog loop to keep long-running memory usage consistently below ~50MB.

### Changed
- **Non-Disruptive Audio Restarts**: Stream health recovery now restarts only the audio player (`restart_audio_stream`) without disconnecting from the Discord voice channel, preserving continuous call duration and voice session stability.

### Fixed
- **Voice Handshake Collision Prevention**: Upgraded `connect_to_voice` to clean up half-open/stale voice connections before opening new sockets, eliminating `The voice handshake is being terminated` collision errors during Discord voice server migrations.

---

## [4.0.0] - 2026-08-25


### Added
- **Dynamic Configuration System**: Created `config.py` with typed `.env` variables and fallback defaults via `python-dotenv`.
- **Modular Cog Architecture**: Organized codebase into clean domain cogs (`cogs/music.py`, `cogs/general.py`, `cogs/events.py`, `cogs/errors.py`).
- **Interactive Discord UI Views**: Added buttons for Invite, Support Server, Top.gg Vote, and Sister Bots cross-promotion (`JazzRadio`, `DiscoBot`).
- **Global Error Handling**: Introduced `cogs/errors.py` with user-friendly ephemeral embeds for missing permissions, cooldowns, and check failures.
- **Proactive 24/7 Auto-Recovery Watchdog**: Upgraded `utils/stream_check.py` to continuously inspect all saved guild voice states and automatically reconnect the bot if Discord drops the voice connection (e.g. server maintenance, RTC region shifts, or inactivity).
- **Persistent Channel State Protection**: Prevented premature state deletion on transient voice disconnects; channel state is now strictly retained until explicit `/leave` invocation or channel deletion.
- **Opus & FFmpeg Optimization**: Added auto-reconnect parameters (`-nostdin -reconnect 1 -reconnect_streamed 1 -reconnect_at_eof 1 -reconnect_delay_max 5`) and Opus voice verification.
- **Security & Git Hygiene**: Added `.gitignore` and `.env.example` to prevent committing secrets, databases, or local virtual environments.
- **Automated Verification Suite**: Added test suite validating configuration, database CRUD, stream health probe, and dynamic cog registration.

### Changed
- Refactored `bot.py` using asynchronous `setup_hook()` for loading cogs dynamically.
- Modernized command registration using `discord.app_commands` slash commands with rich parameter constraints.
- Updated `db/database.py` to use asynchronous SQLite (`aiosqlite`) for persisting voice channel states across restarts.

### Fixed
- Fixed runtime `AttributeError` on `self.bot.mp3_link` in `/play` command.
- Fixed hardcoded stream URLs and duplicate interaction responses in slash commands.

---

## [3.0.0] - 2024

### Added
- Auto-rejoin feature to reconnect the bot to active voice channels after restarts or crashes using SQLite.
- Background task to check stream connectivity periodically.

### Changed
- Major bot code refactoring to improve modularity and performance.
- Switched audio engine from LavaLink to native FFmpeg audio streaming.

### Fixed
- Resolved frequent audio interruption and stuttering issues.

### Removed
- Removed legacy `on_prefix` event listener.

---

## [2.1.0]

### Fixed
- Minor bug fixes and stability improvements.

---

## [2.0.0]

### Added
- `/volume` command with dynamic audio level adjustment.
- 24/7 continuous online streaming stability enhancements.

### Fixed
- Resolved edge cases causing bot crashes during long voice sessions.

---

## [1.5.0]

### Added
- Embed messages on commands providing helpful migration and support notices.

### Removed
- Removed legacy admin command modules.

---

## [1.4.1]

### Added
- `/info` command displaying bot information, hosting details, and developer credits.
- Enhanced `on_ready` startup logging messages.

### Fixed
- Fixed uptime calculation bugs in `/uptime`.

---

## [1.4.0]

### Added
- Rotational rich presence status messages showcasing Moroccan artists and radio shows.
- Mention listener replying with `/help` whenever the bot is tagged in text channels.

### Removed
- Removed legacy prefix commands in favor of Discord Slash Commands.

---

## [1.3.1]

### Fixed
- Fixed issue with Join, Leave, Pause, and Resume slash command interactions.

---

## [1.3.0]

### Added
- Initial implementation of Discord Slash Commands.
- `/uptime` command tracking elapsed session time.
- Enhanced `on_ready` startup sequence.

---

## [1.2.3]

### Added
- Invalid command warnings for unrecognized commands.

### Changed
- Permission and administrator check improvements.

---

## [1.2.2]

### Added
- `hr!stop` command.

### Changed
- Reorganized utility helpers and file structure.

---

## [1.2.1]

### Fixed
- Fixed Top.gg voting command response issues.

---

## [1.2.0]

### Added
- `hr!vote` command for Top.gg support.
- New status messages in rich presence.

### Fixed
- Fixed `hr!leave`, `hr!resume`, `hr!pause` commands.
