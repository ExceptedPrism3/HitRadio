const { REST, Routes } = require('discord.js');
const fs = require('fs');
const path = require('path');

async function loadCommands(client) {

    const commands = [];
    const commandsPath = path.join(__dirname, '../commands');
    const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

    for (const file of commandFiles) {
        const command = require(path.join(commandsPath, file));
        client.commands.set(command.data.name, command);
        commands.push(command.data.toJSON());
    }

    if (commands.length > 0) {
        await registerCommands(client, commands);
    }
}

async function registerCommands(client, commands) {

    const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN);

    try {
        const clientId = client.user.id;

        await rest.put(
            Routes.applicationCommands(clientId),
            { body: commands },
        );

    } catch (error) {
        console.error('Failed to reload application (/) commands:', error);
    }
}

module.exports = { loadCommands };
