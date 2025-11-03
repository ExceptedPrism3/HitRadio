require('./utils/logger');

// Initialize encryption library for voice connections
try {
  require('sodium');
  console.log('Loaded sodium for voice encryption');
} catch (error) {
  try {
    require('libsodium-wrappers');
    console.log('Loaded libsodium-wrappers for voice encryption');
  } catch (err) {
    console.warn('Warning: No encryption library found. Voice connections may fail. Please install "sodium" or "libsodium-wrappers"');
  }
}

require('dotenv').config();
const { Client, GatewayIntentBits, Collection, PermissionsBitField } = require('discord.js');
const { loadEvents } = require('./loaders/eventLoader');

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

client.login(process.env.DISCORD_TOKEN);
