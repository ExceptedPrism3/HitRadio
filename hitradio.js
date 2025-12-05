require('./utils/logger');
require('dotenv').config();

// CRITICAL: Initialize encryption library BEFORE requiring @discordjs/voice
// @discordjs/voice checks for encryption libraries when it's first required
let encryptionReady = false;

try {
  // Try sodium-native first (preferred, native bindings)
  const sodium = require('sodium-native');
  encryptionReady = true;
  console.log('Loaded sodium-native for voice encryption');
  // Explicitly verify sodium-native is working
  if (typeof sodium.crypto_aead_xchacha20poly1305_ietf_encrypt === 'function') {
    console.log('sodium-native encryption functions verified');
  }
  // Check for the specific encryption modes Discord requires
  console.log('Checking for required encryption modes...');
  console.log('crypto_aead_aes256gcm_encrypt:', typeof sodium.crypto_aead_aes256gcm_encrypt);
  console.log('crypto_aead_xchacha20poly1305_ietf_encrypt:', typeof sodium.crypto_aead_xchacha20poly1305_ietf_encrypt);
  console.log('crypto_aead_chacha20poly1305_ietf_encrypt:', typeof sodium.crypto_aead_chacha20poly1305_ietf_encrypt);
} catch (error) {
  try {
    // Try sodium (native package)
    require('sodium');
    encryptionReady = true;
    console.log('Loaded sodium for voice encryption');
  } catch (error2) {
    try {
      // Try libsodium-wrappers (pure JS, slower but works)
      const libsodium = require('libsodium-wrappers');
      encryptionReady = true;
      console.log('Loaded libsodium-wrappers for voice encryption');
      // Initialize libsodium-wrappers asynchronously
      libsodium.ready.then(() => {
        console.log('libsodium-wrappers initialized and ready');
      }).catch((err) => {
        console.warn('Failed to initialize libsodium-wrappers:', err.message);
      });
    } catch (err) {
      console.warn('Warning: No encryption library found. Voice connections may fail.');
      console.warn('Please install one of: "sodium-native", "sodium", or "libsodium-wrappers"');
      console.warn('Error:', err.message);
    }
  }
}

// Now we can safely require @discordjs/voice
const { Client, GatewayIntentBits, Collection, PermissionsBitField } = require('discord.js');
const { loadEvents } = require('./loaders/eventLoader');
const { generateDependencyReport } = require('@discordjs/voice');
const { Player } = require('./utils/player');

// Log dependency report for debugging - this will show what encryption libraries are detected
console.log('Voice dependency report:');
console.log(generateDependencyReport());

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildVoiceStates] });

client.commands = new Collection();

loadEvents(client);

client.on('interactionCreate', async interaction => {

  if (interaction.isButton()) {
    if (interaction.customId === 'stop_radio') {
      const player = new Player(interaction);
      player.leaveChannel();
      return;
    }
  }

  if (!interaction.isCommand()) return;

  const command = client.commands.get(interaction.commandName);

  if (!command) return;

  const requiredPermissions = [
    PermissionsBitField.Flags.Connect,
    PermissionsBitField.Flags.Speak,
    PermissionsBitField.Flags.SendMessages
  ];

  if (interaction.guild && interaction.member.voice.channel) {
    const botPermissions = interaction.member.voice.channel.permissionsFor(client.user);
    if (!botPermissions.has(requiredPermissions)) {
      return interaction.reply({ content: 'I do not have the required permissions (Connect, Speak, Send Messages) in this voice channel!', ephemeral: true });
    }
  }

  try {
    await command.execute(interaction);
  } catch (error) {
    console.error(error);
    await interaction.reply({ content: 'There was an error executing that command!', ephemeral: true });
  }
});

// Start the bot
client.login(process.env.DISCORD_TOKEN);
