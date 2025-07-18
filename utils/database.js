const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const dbPath = path.resolve(__dirname, '../data/channels.db');
const dataDir = path.dirname(dbPath);

if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

const db = new Database(dbPath);

db.pragma('journal_mode = WAL');

db.exec(`
  CREATE TABLE IF NOT EXISTS channels (
    guildId TEXT PRIMARY KEY,
    channelId TEXT NOT NULL
  )
`);

function saveChannel(guildId, channelId) {
  const stmt = db.prepare('INSERT OR REPLACE INTO channels (guildId, channelId) VALUES (?, ?)');
  stmt.run(guildId, channelId);
}

function removeChannel(guildId) {
  const stmt = db.prepare('DELETE FROM channels WHERE guildId = ?');
  stmt.run(guildId);
}

function getAllChannels() {
  const stmt = db.prepare('SELECT * FROM channels');
  return stmt.all();
}

module.exports = {
  saveChannel,
  removeChannel,
  getAllChannels
};