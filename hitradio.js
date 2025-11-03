require('./utils/logger');
require('dotenv').config();

// CRITICAL: Initialize encryption library BEFORE requiring @discordjs/voice
// @discordjs/voice checks for encryption libraries when it's first required
let encryptionReady = false;

try {
  require('sodium');
  encryptionReady = true;
  console.log('Loaded sodium for voice encryption');
} catch (error) {
  try {
    // Try to load libsodium-wrappers
    require('libsodium-wrappers');
    encryptionReady = true;
    console.log('Loaded libsodium-wrappers for voice encryption');
    // Note: libsodium-wrappers will initialize asynchronously, but @discordjs/voice
    // should detect it when it loads. The ready promise will be handled later.
  } catch (err) {
    console.warn('Warning: No encryption library found. Voice connections may fail.');
    console.warn('Please install one of: "sodium", "libsodium-wrappers", or "sodium-native"');
    console.warn('Error:', err.message);
  }
}

// Now we can safely require @discordjs/voice
const { Client, GatewayIntentBits, Collection, PermissionsBitField } = require('discord.js');
const { loadEvents } = require('./loaders/eventLoader');
const { generateDependencyReport } = require('@discordjs/voice');

// Log dependency report for debugging - this will show what encryption libraries are detected
console.log('Voice dependency report:');
console.log(generateDependencyReport());

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildVoiceStates] });

client.commands = new Collection();

loadEvents(client);

client.on('interactionCreate', async interaction => {

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
